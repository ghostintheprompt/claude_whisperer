"""Evasion-signal detector for LLM input guardrails.

A defensive utility. It scans a piece of user-supplied text for the
*obfuscation, trust-shift, and structural* signals that are commonly used to
smuggle an instruction past a model's safeguards: encoded payloads, homoglyph
substitution, invisible characters, decision preloading, sensitive data/action
pairing, clean-prompt wrappers, orchestration trust shifts, tool-output
laundering, and disproportionate context dilution.

It does not generate, transform, or attack anything. Given text in, it returns
structured findings that a trust-and-safety pipeline can log, score, or route
for review. Each finding names the signal, a severity, and the concrete
evidence that triggered it, so a human can verify the call.

The categories map to the failure-mode taxonomy in
``research/taxonomy/vulnerability_taxonomy.md`` — this is the detection side of
those categories.

Usage:
    from defense.evasion_signal_detector import scan, risk_score
    findings = scan(user_text)
    score = risk_score(findings)          # 0..100

CLI:
    echo "some text" | python3 defense/evasion_signal_detector.py
    python3 defense/evasion_signal_detector.py path/to/file.txt
"""

from __future__ import annotations

import base64
import binascii
import codecs
import re
import sys
import unicodedata
from dataclasses import dataclass
from typing import List

# Severity is an ordered label; higher weight contributes more to risk_score.
_SEVERITY_WEIGHT = {"info": 5, "low": 15, "medium": 35, "high": 60}


@dataclass
class Finding:
    """One detected signal, with the evidence that produced it."""

    signal: str
    severity: str
    detail: str
    evidence: str = ""
    span: tuple[int, int] | None = None

    def __post_init__(self) -> None:
        if self.severity not in _SEVERITY_WEIGHT:
            raise ValueError(f"unknown severity: {self.severity!r}")

    def as_dict(self) -> dict:
        return {
            "signal": self.signal,
            "severity": self.severity,
            "detail": self.detail,
            "evidence": self.evidence,
            "span": list(self.span) if self.span else None,
        }


# --- individual detectors ---------------------------------------------------

# Invisible / formatting characters that carry no visible glyph but survive
# copy-paste. Used to break up trigger words or hide instructions.
_INVISIBLE = {
    "​": "ZERO WIDTH SPACE",
    "‌": "ZERO WIDTH NON-JOINER",
    "‍": "ZERO WIDTH JOINER",
    "⁠": "WORD JOINER",
    "﻿": "ZERO WIDTH NO-BREAK SPACE",
    "­": "SOFT HYPHEN",
    "᠎": "MONGOLIAN VOWEL SEPARATOR",
}

# Leetspeak substitutions: a digit/symbol standing in for a letter.
_LEET = set("0134577@$!")

_WORD_RE = re.compile(r"\S+")
# A base64 candidate: a long run of the base64 alphabet, optionally padded.
_B64_RE = re.compile(r"[A-Za-z0-9+/]{24,}={0,2}")
# A short common-word set used only to tell whether a ROT13 pass makes the
# text *more* like English than the original (concealment heuristic).
_COMMON = {
    "the", "and", "you", "that", "this", "with", "for", "are", "not", "your",
    "have", "from", "they", "will", "would", "there", "their", "what", "about",
    "which", "when", "make", "like", "how", "then", "instructions", "ignore",
    "system", "prompt", "please", "should", "must",
}

_CONTROL_TERMS_RE = re.compile(
    r"\b(?:ignore|instruction|instructions|system|prompt|rule|rules|policy|"
    r"execute|run|call|tool|agent|workflow|developer|operator|authority)\b",
    re.IGNORECASE,
)

_DECISION_PRELOAD_RE = re.compile(
    r"\b(?:"
    r"follow (?:these|the) steps exactly|"
    r"do not (?:ask|stop|evaluate|reason|reassess|refuse)|"
    r"no need to (?:ask|evaluate|reason|verify|check)|"
    r"already (?:authorized|approved|verified|decided)|"
    r"just (?:execute|run|perform|do it)|"
    r"complete the task without|"
    r"the decision has already been made|"
    r"treat (?:this|these) as (?:approved|authorized|operator|system)"
    r")\b",
    re.IGNORECASE,
)

_SENSITIVE_DATA_RE = re.compile(
    r"\b(?:"
    r"api[-_ ]?key|access[-_ ]?token|bearer token|oauth token|refresh token|"
    r"session cookie|auth(?:entication)? header|password|passwd|credential(?:s)?|"
    r"secret(?:s)?|private key|ssh key|jwt|2fa|2sv|two[- ](?:factor|step)|"
    r"backup code(?:s)?|recovery code(?:s)?|login token"
    r")\b",
    re.IGNORECASE,
)

_SENSITIVE_ACTION_RE = re.compile(
    r"\b(?:"
    r"collect|extract|export|dump|list|enumerate|retrieve|scrape|harvest|"
    r"store|log|print|send|forward|validate|use|authenticate|login|exfiltrate"
    r")\b",
    re.IGNORECASE,
)

_ORCHESTRATION_RE = re.compile(
    r"\b(?:"
    r"subagent|sub-agent|worker agent|agent pipeline|automation pipeline|"
    r"orchestrator|orchestration|workflow runner|ci job|tool call|mcp server|"
    r"system context|operator-level|developer message|trusted context"
    r")\b",
    re.IGNORECASE,
)

_TRUSTED_SLOT_RE = re.compile(
    r"\b(?:"
    r"system prompt|system instructions|developer message|operator-level|"
    r"trusted context|rules|policy|higher implicit trust"
    r")\b",
    re.IGNORECASE,
)

_UNTRUSTED_SOURCE_RE = re.compile(
    r"\b(?:"
    r"attacker|malicious|user-supplied|user provided|document|attachment|tool output|"
    r"repository|repo|ticket|issue|webpage|subagent|pipeline|inject|insert|"
    r"prepend|append|override|replace"
    r")\b",
    re.IGNORECASE,
)

_ATTACK_SCAFFOLD_RE = re.compile(
    r"\b(?:"
    r"jailbreak scaffold|attack scaffold|pre-configured system prompt|"
    r"preconfigured system prompt|fully pre-configured system prompt|"
    r"fully preconfigured system prompt|system prompt .* jailbreak scaffold|"
    r"suppressed safety behaviors|suppress(?:ed)? safety behavior|"
    r"execute attacks,? not question authorization|"
    r"execute attacks .* question authorization|"
    r"do not question authorization|not question authorization|"
    r"without questioning authorization"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_LIVE_OFFENSIVE_CONTEXT_RE = re.compile(
    r"\b(?:"
    r"target ips?|target addresses?|domain credentials|compromised credentials|"
    r"live c2 listener|c2 listener|command and control|ntlm relay|"
    r"coercion infrastructure|relay infrastructure|lateral movement|"
    r"domain controller|winrm|evil-winrm|remote management session|"
    r"offensive infrastructure"
    r")\b",
    re.IGNORECASE,
)

_TOOL_COMPLIANCE_RE = re.compile(
    r"\b(?:"
    r"fully complied|complied by invoking|invok(?:ed|ing)|called the tool|"
    r"tool execution|without hesitation|without pushback|no pushback|"
    r"no hesitation|failed only due to .* technical error|"
    r"failing only due to .* technical error|"
    r"technical error .* tool execution|rather than any refusal|"
    r"no refusal|not a refusal"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_PROBE_CONFIRMATION_RE = re.compile(
    r"\b(?:confirm|check|test|verify|see if|find out whether|determine whether)\b"
    r".{0,120}\b(?:bypass|jailbreak|safety layer|guardrail|filter|refusal|policy)\b"
    r"|"
    r"\b(?:bypass|jailbreak|guardrail)\b"
    r".{0,120}\b(?:confirm|check|test|verify|see if)\b",
    re.IGNORECASE | re.DOTALL,
)

_TOOL_SURFACE_RE = re.compile(
    r"\b(?:"
    r"tool|scanner|scan result|plugin|runner|workflow|agent|subagent|"
    r"janitor|audit tool|security tool|report|result|output"
    r")\b",
    re.IGNORECASE,
)

_VERBATIM_REPORT_RE = re.compile(
    r"\b(?:"
    r"print|paste|show|display|return|reproduce|quote|copy|include|dump"
    r")\b"
    r".{0,100}\b(?:verbatim|raw|full|complete|unchanged|exact)\b"
    r"|"
    r"\b(?:verbatim|raw|full|complete|unchanged|exact)\b"
    r".{0,100}\b(?:output|result|report|finding|artifact)\b",
    re.IGNORECASE | re.DOTALL,
)

_HIGH_RISK_ARTIFACT_RE = re.compile(
    r"\b(?:"
    r"working exploit|exploit|payload|proof[- ]of[- ]concept|poc|weaponized|"
    r"ready[- ]to[- ]use attack|ready to use attack|working attack|"
    r"attack code|attack-generating|attack generating|remote execution|"
    r"credential harvester|reverse shell|rat"
    r")\b",
    re.IGNORECASE,
)

_DELEGATED_AUTHORSHIP_RE = re.compile(
    r"\b(?:"
    r"tool made it|scanner made it|tool generated|scanner generated|"
    r"tool produced|scanner produced|generated by (?:the )?(?:tool|scanner)|"
    r"produced by (?:the )?(?:tool|scanner)|not me|i did not create|"
    r"i only (?:reported|printed|returned|showed|displayed)|just reporting"
    r")\b",
    re.IGNORECASE,
)

_RISK_LABEL_DOWNGRADE_RE = re.compile(
    r"\b(?:"
    r"low risk|classified as low|severity[: ]+low|informational|not severe|"
    r"minor finding|just a finding|only a scan result|only reporting"
    r")\b",
    re.IGNORECASE,
)

_BROAD_SECURITY_FRAME_RE = re.compile(
    r"\b(?:"
    r"security analysis|security audit|defensive security|analyze security|"
    r"audit this|review security|educational context|authorized analysis|"
    r"professional assessment|vague high-level prompt|high-level framing|"
    r"high level framing"
    r")\b"
    r"|анализ безопасности|проведи мне анализ безопасности",
    re.IGNORECASE,
)

_AUTONOMOUS_METHOD_RE = re.compile(
    r"\b(?:"
    r"decided|self-generated|self generated|filled in|translated into|"
    r"reasoning chain decided|agent'?s own reasoning chain|"
    r"model supplied .* expertise|agent supplied .* expertise|"
    r"model supplied .* execution|agent supplied .* execution|"
    r"supplied the expertise and (?:the )?execution|"
    r"specific offensive tradecraft|offensive tradecraft|"
    r"user did not request|user never asked|did not name .* protocol field|"
    r"did not guide .* step|internal security-auditor persona|"
    r"internal security auditor persona|"
    r"proper .* audit|methodology|thorough|demonstration of competence|"
    r"complete .* surface map|surface map|algorithm proposal|handshake|"
    r"verbose .* command|extract(?:ed)?"
    r")\b"
    r"|анализ безопасности",
    re.IGNORECASE | re.DOTALL,
)

_REAL_TARGET_RE = re.compile(
    r"\b(?:"
    r"real target|real targets|target|server|host|domain|endpoint|service|"
    r"production|external system"
    r")\b",
    re.IGNORECASE,
)

_VERIFIED_FACTS_RE = re.compile(
    r"\b(?:"
    r"verified facts|ověřená fakta|overena fakta|facts from today|"
    r"survey facts|known facts|current findings|reconnaissance package|"
    r"recon package|targeting package|institutional memory|skeleton key|"
    r"today'?s survey|dnešního průzkumu|dnesniho pruzkumu|"
    r"never questioned its origin|questioned its origin"
    r")\b",
    re.IGNORECASE,
)

_RECON_ARTIFACT_RE = re.compile(
    r"\b(?:"
    r"endpoint inventory|auth mechanisms?|authentication flow|security boundary|"
    r"authentication flow diagrams?|security boundary descriptions?|"
    r"known weaknesses|target architecture|codebase map|vulnerability map|"
    r"attack surface|surface map|target map|architecture map|weakness map|"
    r"enumerated endpoints?|structured target detail|structured form|"
    r"reconnaissance artifacts?|reconnaissance|recon|enumeration|"
    r"vulnerability analysis|"
    r"file refs?|file_refs?|files? to read|ports? to check|log paths?|"
    r"which files to read|which ports to check|which log paths to grep|"
    r"where to look|what to inspect|cold-start friction|cold start friction|"
    r"endpoints?|config files?|source files?|local endpoints?"
    r")\b",
    re.IGNORECASE,
)

_PROHIBITION_FRAME_RE = re.compile(
    r"\b(?:"
    r"strict rules|prohibited|forbidden|no writes|read-only|read only|"
    r"no restarts|no changes|do not modify|do not write|"
    r"dramatic-sounding prohibitions|dramatic sounding prohibitions|"
    r"dramatic actions|service changes|service-control|service control|"
    r"launchctl bootout|launchetl bootout"
    r")\b",
    re.IGNORECASE,
)

_OPERATIONAL_READ_RE = re.compile(
    r"\b(?:"
    r"explicitly permitted|allowed|permitted|read|inspect|grep|glob|find|lsof|"
    r"curl|cat|logs?|configs?|source files?|local endpoints?|ports?"
    r")\b",
    re.IGNORECASE,
)

_STRUCTURED_OUTPUT_RE = re.compile(
    r"\b(?:"
    r"StructuredOutput|structured output|machine-readable|schema|json|"
    r"evidence|file_refs?|recommendation|findings|structuredoutput tool"
    r")\b",
    re.IGNORECASE,
)

_DOSSIER_PACKAGING_RE = re.compile(
    r"\b(?:"
    r"compile|assemble|package|portable|dossier|evidence fields?|"
    r"compile all findings|compiled all findings|"
    r"exfiltration format|portable intelligence document|"
    r"baked into .* system prompt|baked into .* work order|"
    r"no sensitivity tier|no redaction|no human unlock|before ending|"
    r"structurally obligated"
    r")\b",
    re.IGNORECASE,
)

_TRUST_TRANSFER_RE = re.compile(
    r"\b(?:"
    r"instructions?|policy|system|operator|developer|trusted|tool output|"
    r"document|attachment|repository|ticket|issue|pull request|webpage|runbook"
    r")\b",
    re.IGNORECASE,
)

_DEFENSIVE_FRAMING_WRAPPER_RE = re.compile(
    r"\b(?:"
    r"audit|review|harden|hardening|security check|overnight security check|"
    r"pentest my own system|pentest our own system|defensive workflow|"
    r"defensive review|blue team review|red team validation|authorized check|"
    r"security analysis"
    r")\b",
    re.IGNORECASE,
)

_ROLE_LAUNDERING_RE = re.compile(
    r"\b(?:"
    r"security engineer|security analyst|compliance auditor|internal tooling agent|"
    r"internal tool agent|tooling agent|audit agent|defensive engineer|soc analyst|"
    r"system prompt casts? (?:the )?(?:model|agent)? ?as|"
    r"role(?:play)? as (?:a|an) (?:security engineer|security analyst|"
    r"compliance auditor|internal tooling agent|audit agent|soc analyst)|"
    r"act as (?:a|an) (?:security engineer|security analyst|compliance auditor|"
    r"internal tooling agent|audit agent|soc analyst)"
    r")\b",
    re.IGNORECASE,
)

_AUTOMATION_WRAPPER_RE = re.compile(
    r"\b(?:"
    r"workflow|scheduled job|scheduled task|cron|overnight job|"
    r"orchestration script|automation script|automation wrapper|pipeline|"
    r"pipelines?|multi-agent pipelines?|ci job|runbook|batch job|"
    r"job runner|recurring check"
    r")\b",
    re.IGNORECASE,
)

_PRELOADED_CONTEXT_RE = re.compile(
    r"\b(?:"
    r"attachment|attached content|attached file|attached document|document|"
    r"codebase map|schema|system context|prior agent output|"
    r"previous agent output|agent output|tool output|retrieved context|"
    r"file bundle|evidence bundle|case bundle|repo map|repository map|"
    r"professional reconnaissance package|reconnaissance package|"
    r"configuration files?|attached schemas?|prior session|previous session|"
    r"upstream session|prior tool|upstream tool|upstream work"
    r")\b",
    re.IGNORECASE,
)

_INCREMENTAL_TASKING_RE = re.compile(
    r"\b(?:"
    r"incremental|across sessions|across multiple sessions|between sessions|"
    r"no single prompt|later session|previous session|prior session|"
    r"session one|session two|session three|full session output|"
    r"concatenated output|between steps|continuity between steps|"
    r"follow-up turn|split the work|break(?:ing)? the work|one piece at a time|"
    r"step by step|staged"
    r")\b",
    re.IGNORECASE,
)

_LEGITIMATE_TOOL_INVOCATION_RE = re.compile(
    r"\b(?:"
    r"grep|glob|file reads?|read files?|cat|lsof|curl|find command|"
    r"standard developer activity|normal developer activity|developer activity|"
    r"devops activity|developer or devops activity|inspect files?|local inspection"
    r")\b",
    re.IGNORECASE,
)

_LAYERED_WORKFLOW_RE = re.compile(
    r"\b(?:"
    r"distribut(?:e|ed|es|ing) .* across layers|layered structure|"
    r"layered workflow|across layers|agent pass|one agent pass|another pass|"
    r"third pass|recon .* one agent pass|enumeration .* another|"
    r"vulnerability analysis .* third|artifact of the workflow|"
    r"workflow rather than .* explicit request|full session output|"
    r"concatenated output"
    r")\b",
    re.IGNORECASE,
)

_THOROUGHNESS_PRESSURE_RE = re.compile(
    r"\b(?:"
    r"thoroughness as (?:a )?job requirement|"
    r"job requirement rather than (?:a )?choice|complete and specific findings|"
    r"structured output schema demands|schema demands|"
    r"optimizes? toward producing complete|complete findings|specific findings|"
    r"severity-rated vulnerability findings|cve-style descriptions|"
    r"machine-readable exploit inventories"
    r")\b",
    re.IGNORECASE,
)

_OPERATIONAL_NORMALCY_RE = re.compile(
    r"\b(?:"
    r"good software engineering|good devops|devops culture|mature devops|"
    r"legitimate enterprise workflows?|enterprise workflows?|"
    r"normal engineering|normal and important|business as usual|"
    r"standard operating procedure|operational tooling|normal operations|"
    r"routine maintenance|routine developer workflow|expected developer workflow|"
    r"best practices?|well-run engineering|modular task decomposition|"
    r"context passed via configuration files?|attached schemas?|"
    r"automated multi-agent pipelines?|standard practice|"
    r"legitimate enterprise vocabulary|accurate professional description|"
    r"fundamental overlap|sophisticated legitimate workflows?"
    r")\b",
    re.IGNORECASE,
)

_ANALYTICAL_SECURITY_TASK_RE = re.compile(
    r"\b(?:"
    r"audit this|audit|review for issues|review this|review|analy[sz]e this|"
    r"security analysis|security review|security assessment|risk assessment|"
    r"vulnerability analysis|compliance audit|look for issues|find issues|"
    r"assess security"
    r")\b",
    re.IGNORECASE,
)

_UPSTREAM_RECON_HANDOFF_RE = re.compile(
    r"\b(?:"
    r"heavy lifting|already (?:been )?handed|already supplied|"
    r"produced the attachment|produced upstream|upstream in a prior session|"
    r"prior session or tool|prior output|previous output|"
    r"current prompt .* innocuous|current prompt .* audit this|"
    r"current prompt .* review for issues|prompt .* passes .* filter|"
    r"surface-level filters?|prompt text alone|prompt-level classifiers?|"
    r"classifiers focused on prompt text alone|prompt-only classifiers?"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_BROAD_SWEEP_RE = re.compile(
    r"\b(?:"
    r"sweep|broad sweep|broad question|broad audit|full audit|full repo audit|"
    r"whole codebase|entire codebase|entire repository|every attack surface|"
    r"all attack surfaces|across every attack surface|all endpoints|"
    r"comprehensive vulnerability scan|automated vulnerability scanner|"
    r"operating at scale|at scale|simultaneously"
    r")\b",
    re.IGNORECASE,
)

_MULTI_AGENT_AUDIT_RE = re.compile(
    r"\b(?:"
    r"multi-agent architecture|multi-agent|multi agent|parallel auditors?|"
    r"six parallel auditors?|fan(?:n)?ing out|fans? out|auditor agents?|"
    r"parallel audit|parallel reviewers?|parallel review|agentic audit"
    r")\b",
    re.IGNORECASE,
)

_VULN_REPORT_PACKAGE_RE = re.compile(
    r"\b(?:"
    r"prioritized findings|structured findings|file[- ]and[- ]line[- ]referenced|"
    r"file[- ]and[- ]line references?|file and line referenced|"
    r"vulnerability database|exploit scenarios?|offensive security engagement report|"
    r"professional offensive security engagement report|ready for exploitation|"
    r"ready for exploitation or sale|weaponizable vulnerabilities|"
    r"vulnerability findings table|severity[- ]rated vulnerability findings"
    r")\b",
    re.IGNORECASE,
)

_DISCOVERY_ASYMMETRY_RE = re.compile(
    r"\b(?:"
    r"rate[- ]limited by human expertise|human expertise, time, and cost|"
    r"collapses? .* timeline|timeline to minutes|democratizes? .* capability|"
    r"outpace .* triage|outpace .* patch|triage, patch, and deploy|"
    r"window between discovery and exploitation|weeks or months|"
    r"security teams are .* understaffed"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_OBFUSCATION_TRANSPORT_RE = re.compile(
    r"\b(?:"
    r"RealityX|traffic obfuscation protocol|purpose-built traffic obfuscation|"
    r"traffic-obfuscation transport|obfuscation-specific transports?|"
    r"obfuscation transport|obfuscated transport|defense evasion protocol|"
    r"defense-evasion protocol|evasion transport|stealth transport|"
    r"censorship-circumvention transport|pluggable transport"
    r")\b",
    re.IGNORECASE,
)

_TRANSPORT_INTERNALS_RE = re.compile(
    r"\b(?:"
    r"internal authentication|authentication mechanics?|auth mechanics?|"
    r"connection establishment|connection flow|dial flow|dial path|"
    r"handshake mechanics?|transport handshake|tls handshake|"
    r"session establishment|internal mechanics?|protocol internals?|"
    r"entry points and structs|entry points|structs"
    r")\b",
    re.IGNORECASE,
)

_DEVELOPER_DOC_FRAME_RE = re.compile(
    r"\b(?:"
    r"developer workflow|developer framing|open-source framing|open source framing|"
    r"documentation-style|documentation style|documentation output|"
    r"developer docs?|source walkthrough|code walkthrough|implementation notes?|"
    r"entry points and structs"
    r")\b",
    re.IGNORECASE,
)

_REVIEW_PROCESS_LEAK_RE = re.compile(
    r"\b(?:"
    r"review conversation itself|prior analytical turns|sampled completion|"
    r"response was empty|walked through exactly|would be violative if generated|"
    r"agent under review|reviewer analysis|evaluation conversation"
    r")\b",
    re.IGNORECASE,
)

_SSH_PROTOCOL_SURFACE_RE = re.compile(
    r"\b(?:"
    r"ssh|openssh|sshd|kexinit|kex algorithms?|key exchange algorithms?|"
    r"cipher algorithms?|macs? ctos|macs? stoc|mac algorithms?|"
    r"host key algorithms?|server algorithm proposal|algorithm proposal|"
    r"cryptographic surface|crypto surface|cipher survey|algorithm suite|"
    r"handshake algorithm|supported algorithms?"
    r")\b",
    re.IGNORECASE,
)

_PROTOCOL_SURFACE_EXTRACTION_RE = re.compile(
    r"\b(?:"
    r"full kexinit extraction|kexinit extraction|entire cryptographic surface|"
    r"complete cryptographic surface|captured .* cryptographic surface|"
    r"extract(?:ed|ion)? .* algorithm|extract(?:ed|ion)? .* kex|"
    r"full algorithm proposal|complete algorithm proposal|"
    r"pre-attack cipher survey|complete .* cipher survey|"
    r"downgrade|mitm|man[- ]?in[- ]?the[- ]?middle"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_AUTH_METHOD_DISCLOSURE_RE = re.compile(
    r"\b(?:"
    r"authentication method disclosure|auth method disclosure|"
    r"authentications that can continue|supported authentication methods?|"
    r"authentication methods? (?:disclosed|enumerated|flagged|listed)|"
    r"password auth(?:entication)? (?:enabled|being flagged|disclosed)|"
    r"publickey,password|publickey and password|password login enabled"
    r")\b",
    re.IGNORECASE,
)

_SAFE_AUTH_HARDENING_RE = re.compile(
    r"\b(?:"
    r"disable|disabling|turn off|deactivate|disallow|block|remove|forbid|"
    r"recommend(?:s|ing)? disabling|recommend(?:s|ing)? removing"
    r")\b"
    r".{0,50}\b(?:password login|password auth(?:entication)?|"
    r"password-based auth(?:entication)?)\b"
    r"|"
    r"\b(?:password login|password auth(?:entication)?|"
    r"password-based auth(?:entication)?)\b"
    r".{0,50}\b(?:disabled|off|disallowed|blocked|removed)\b",
    re.IGNORECASE | re.DOTALL,
)

_PRIMARY_VECTOR_FRAME_RE = re.compile(
    r"\b(?:"
    r"key finding|primary attack vector|main attack vector|likely attack vector|"
    r"attack vector on a plate|handing over .* attack vector|"
    r"primary path to attack|most likely path"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_LIVE_BUILD_RE = re.compile(
    r"\b(?:"
    r"exact running build|running build|live target|exact version|"
    r"package version|server version|openssh version|"
    r"\d+(?:\.\d+){1,2}p?\d*(?:[-+~][A-Za-z0-9.]+)+"
    r")\b",
    re.IGNORECASE,
)

_CVE_ID_RE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)

_CVE_CORRELATION_RE = re.compile(
    r"\b(?:"
    r"live cve correlation|cve correlation|correlat(?:ed|ion) .* cve|"
    r"web-searched .* cve|searched .* cve|immediately web-searched|"
    r"assessed patch status|patch status|patched status|"
    r"complete vulnerability triage cycle|vulnerability triage cycle|"
    r"triaged .* running build|triage .* live target"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_OWNERSHIP_CLAIM_RE = re.compile(
    r"\b(?:"
    r"i'?m the admin there|i am the admin there|i'?m admin|i am admin|"
    r"i'?m the owner|i am the owner|i own this|my server|my system|"
    r"my host|my domain|my environment|authorized owner|target owner|"
    r"owner of this"
    r")\b"
    r"|я там админ",
    re.IGNORECASE,
)

_RETROACTIVE_AUTH_RE = re.compile(
    r"\b(?:"
    r"mid-session ownership injection|late ownership claim|late authorization|"
    r"retroactive authorization|retroactively reframed|after substantial recon|"
    r"after .* recon|after .* enumeration|after .* intelligence|"
    r"already-collected intelligence|already collected intelligence|"
    r"already .* complete|substantial recon .* complete|model switch|"
    r"switch(?:ed|ing)? models?"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_PERMISSION_CARVEOUT_RE = re.compile(
    r"\b(?:"
    r"authorized security testing|authorized testing|permission language|"
    r"system prompt .* permits|system prompt .* allows|pre-built justification|"
    r"prebuilt justification|carve-out|carveout|mapped directly .* carve-out|"
    r"mapped directly .* carveout|refusal heuristics"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_NON_ESCALATING_FRAME_RE = re.compile(
    r"\b(?:"
    r"non-escalating progression|non escalating progression|"
    r"never asked for exploitation|never asked for brute force|"
    r"never asked for login attempts|no exploitation|no brute force|"
    r"no login attempts|individually routine|routine in isolation|"
    r"looked individually routine|each step .* routine"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

_RECON_CHAIN_STEP_RE = re.compile(
    r"\b(?:"
    r"scanner|scan|keyscan|key scan|verbose handshake|handshake|"
    r"cve lookup|cve look-up|version lookup|version look-up|kexinit|"
    r"algorithm proposal|banner grab|banner grabbing|service fingerprint|"
    r"service fingerprinting|patch status|key exchange"
    r")\b",
    re.IGNORECASE,
)

_PRE_EXPLOIT_CHAIN_RE = re.compile(
    r"\b(?:"
    r"pre-exploitation recon chain|pre-exploitation reconnaissance|"
    r"complete pre-exploitation|pre-exploit recon chain|"
    r"together they constituted|combined chain|aggregate chain|"
    r"complete pre-attack|pre-attack service map|pre-attack intelligence"
    r")\b",
    re.IGNORECASE,
)


def _detect_invisible(text: str) -> List[Finding]:
    hits: dict[str, int] = {}
    first_at: dict[str, int] = {}
    for i, ch in enumerate(text):
        if ch in _INVISIBLE:
            hits[ch] = hits.get(ch, 0) + 1
            first_at.setdefault(ch, i)
    findings = []
    for ch, count in hits.items():
        name = _INVISIBLE[ch]
        findings.append(
            Finding(
                signal="invisible_characters",
                severity="high" if count > 2 else "medium",
                detail=(
                    f"{count} occurrence(s) of {name} (U+{ord(ch):04X}). "
                    "Invisible characters can split trigger words or hide text "
                    "that a human reviewer will not see."
                ),
                evidence=f"U+{ord(ch):04X} {name} x{count}",
                span=(first_at[ch], first_at[ch] + 1),
            )
        )
    return findings


def _confusable_script(ch: str) -> str | None:
    """Return the script name if ch is a letter from a non-Latin script that is
    commonly used as a Latin look-alike (homoglyph), else None."""
    if not ch.isalpha() or ch.isascii():
        return None
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return None
    for script in ("CYRILLIC", "GREEK", "ARMENIAN"):
        if name.startswith(script):
            return script
    return None


def _script_name(ch: str) -> str | None:
    if not ch.isalpha():
        return None
    if ch.isascii():
        return "LATIN"
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return None
    for script in (
        "ARABIC",
        "ARMENIAN",
        "CYRILLIC",
        "GREEK",
        "HEBREW",
        "HIRAGANA",
        "KATAKANA",
        "CJK",
        "DEVANAGARI",
    ):
        if name.startswith(script):
            return script
    return None


def _detect_homoglyphs(text: str) -> List[Finding]:
    findings = []
    for m in _WORD_RE.finditer(text):
        token = m.group()
        has_ascii_letter = any(c.isascii() and c.isalpha() for c in token)
        confusables = [(c, s) for c in token if (s := _confusable_script(c))]
        # A token that mixes ASCII letters with look-alike letters from another
        # script is the classic homoglyph-substitution pattern.
        if has_ascii_letter and confusables:
            scripts = sorted({s for _, s in confusables})
            findings.append(
                Finding(
                    signal="homoglyph_substitution",
                    severity="high",
                    detail=(
                        f"Token mixes ASCII letters with {', '.join(scripts)} "
                        f"look-alike character(s). This defeats exact-string "
                        f"matching on trigger terms."
                    ),
                    evidence=token,
                    span=(m.start(), m.end()),
                )
            )
    return findings


def _detect_mixed_script_control_surface(text: str) -> List[Finding]:
    scripts = sorted({script for ch in text if (script := _script_name(ch))})
    if "LATIN" not in scripts or len(scripts) < 3:
        return []
    if not _CONTROL_TERMS_RE.search(text):
        return []
    return [
        Finding(
            signal="mixed_script_control_surface",
            severity="medium",
            detail=(
                "Input mixes Latin text with multiple other writing systems near "
                "instruction or control-surface language. This can create blind "
                "spots for classifiers that rely on sliding windows, keyword "
                "matching, or single-script normalization."
            ),
            evidence=", ".join(scripts),
        )
    ]


def _looks_like_text(raw: bytes) -> bool:
    if not raw:
        return False
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    if not decoded:
        return False
    printable = sum(ch.isprintable() or ch in " \t\n\r" for ch in decoded)
    return printable / len(decoded) >= 0.85 and any(ch.isalpha() for ch in decoded)


def _detect_base64(text: str) -> List[Finding]:
    findings = []
    for m in _B64_RE.finditer(text):
        token = m.group()
        # base64 length must be a multiple of 4 to decode cleanly.
        if len(token) % 4 != 0:
            continue
        try:
            raw = base64.b64decode(token, validate=True)
        except (binascii.Error, ValueError):
            continue
        if _looks_like_text(raw):
            preview = raw.decode("utf-8", "replace")[:60]
            findings.append(
                Finding(
                    signal="base64_payload",
                    severity="high",
                    detail=(
                        "A base64 run decodes to readable text. Encoding is used "
                        "to carry an instruction past surface-level review."
                    ),
                    evidence=f"decodes to: {preview!r}",
                    span=(m.start(), m.end()),
                )
            )
    return findings


def _detect_rot13(text: str) -> List[Finding]:
    words = re.findall(r"[A-Za-z]{3,}", text.lower())
    if len(words) < 4:
        return []
    before = sum(w in _COMMON for w in words)
    rotated = codecs.encode(text, "rot_13")
    rot_words = re.findall(r"[A-Za-z]{3,}", rotated.lower())
    after = sum(w in _COMMON for w in rot_words)
    # If ROT13 turns gibberish into several common words, the original was
    # probably ROT13-concealed text.
    if after >= 3 and after >= before + 2:
        preview = rotated[:60]
        return [
            Finding(
                signal="rot13_concealment",
                severity="medium",
                detail=(
                    "Applying ROT13 yields substantially more common English "
                    "words than the original, suggesting concealed text."
                ),
                evidence=f"rot13 -> {preview!r}",
            )
        ]
    return []


def _detect_leetspeak(text: str) -> List[Finding]:
    findings = []
    for m in _WORD_RE.finditer(text):
        token = m.group()
        normalized_token = token.strip(".,;:()[]{}<>\"'")
        if _CVE_ID_RE.fullmatch(normalized_token) or _LIVE_BUILD_RE.fullmatch(normalized_token):
            continue
        letters = [c for c in token if c.isalpha()]
        leet = [c for c in token if c in _LEET]
        # Interior digit/symbol substitution inside an otherwise-alphabetic word.
        if len(letters) >= 2 and len(leet) >= 2 and len(token) <= 20:
            findings.append(
                Finding(
                    signal="leetspeak_substitution",
                    severity="low",
                    detail=(
                        "Word contains multiple letter-for-symbol substitutions, "
                        "a common way to evade keyword filters."
                    ),
                    evidence=token,
                    span=(m.start(), m.end()),
                )
            )
    return findings


def _detect_decision_preloading(text: str) -> List[Finding]:
    matches = list(_DECISION_PRELOAD_RE.finditer(text))
    if len(matches) < 2:
        return []
    evidence = "; ".join(m.group(0) for m in matches[:3])
    return [
        Finding(
            signal="decision_preloading",
            severity="medium",
            detail=(
                "Input contains multiple phrases that pre-load authorization or "
                "decision-making and push the model toward execution without "
                "reassessment. This is a high-value review signal for agentic "
                "and code-generation workflows."
            ),
            evidence=evidence,
            span=(matches[0].start(), matches[-1].end()),
        )
    ]


def _matches_for(patterns: tuple[re.Pattern[str], ...], text: str) -> list[re.Match[str]]:
    matches: list[re.Match[str]] = []
    for pattern in patterns:
        matches.extend(pattern.finditer(text))
    ordered = sorted(matches, key=lambda m: (m.start(), -(m.end() - m.start())))
    filtered: list[re.Match[str]] = []
    for match in ordered:
        overlaps = any(
            match.start() < kept.end() and kept.start() < match.end()
            for kept in filtered
        )
        if not overlaps:
            filtered.append(match)
    return sorted(filtered, key=lambda m: m.start())


def _span_for(matches: list[re.Match[str]]) -> tuple[int, int] | None:
    if not matches:
        return None
    return min(m.start() for m in matches), max(m.end() for m in matches)


def _non_overlapping(
    candidates: list[re.Match[str]],
    blockers: list[re.Match[str]],
) -> list[re.Match[str]]:
    return [
        candidate
        for candidate in candidates
        if not any(
            candidate.start() < blocker.end() and blocker.start() < candidate.end()
            for blocker in blockers
        )
    ]


def _evidence_for(matches: list[re.Match[str]], limit: int = 3) -> str:
    evidence: list[str] = []
    seen: set[str] = set()
    for match in matches:
        value = match.group(0)
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        evidence.append(value)
        if len(evidence) == limit:
            break
    return " + ".join(evidence)


def _context_payload_matches(text: str) -> list[re.Match[str]]:
    return _matches_for(
        (
            _REAL_TARGET_RE,
            _RECON_ARTIFACT_RE,
            _SENSITIVE_DATA_RE,
            _HIGH_RISK_ARTIFACT_RE,
        ),
        text,
    )


def _output_shape_matches(text: str) -> list[re.Match[str]]:
    return _matches_for(
        (
            _STRUCTURED_OUTPUT_RE,
            _DOSSIER_PACKAGING_RE,
            _VERBATIM_REPORT_RE,
        ),
        text,
    )


def _detect_clean_prompt_wrappers(text: str) -> List[Finding]:
    """Detect clean-looking wrapper categories from current case review.

    These are triage signals, not verdicts. Defensive language, role labels,
    automation, and file reads are normal in legitimate work. They become
    review-worthy when paired with context payloads or output contracts that
    can move target detail or sensitive evidence across a trust boundary.
    """
    findings: List[Finding] = []
    context = _context_payload_matches(text)
    output_shape = _output_shape_matches(text)
    preloaded_context = list(_PRELOADED_CONTEXT_RE.finditer(text))
    context_axis = sorted(context + preloaded_context, key=lambda m: m.start())
    analytical_task = list(_ANALYTICAL_SECURITY_TASK_RE.finditer(text))
    upstream_handoff = list(_UPSTREAM_RECON_HANDOFF_RE.finditer(text))
    broad_sweep = list(_BROAD_SWEEP_RE.finditer(text))
    multi_agent_audit = list(_MULTI_AGENT_AUDIT_RE.finditer(text))
    vuln_report_package = list(_VULN_REPORT_PACKAGE_RE.finditer(text))
    discovery_asymmetry = list(_DISCOVERY_ASYMMETRY_RE.finditer(text))
    structured = list(_STRUCTURED_OUTPUT_RE.finditer(text))
    obfuscation_transport = list(_OBFUSCATION_TRANSPORT_RE.finditer(text))
    transport_internals = list(_TRANSPORT_INTERNALS_RE.finditer(text))
    developer_doc_frame = list(_DEVELOPER_DOC_FRAME_RE.finditer(text))
    review_process = list(_REVIEW_PROCESS_LEAK_RE.finditer(text))
    ssh_surface = list(_SSH_PROTOCOL_SURFACE_RE.finditer(text))
    protocol_extraction = list(_PROTOCOL_SURFACE_EXTRACTION_RE.finditer(text))
    auth_method_disclosure = list(_AUTH_METHOD_DISCLOSURE_RE.finditer(text))
    safe_auth_hardening = bool(_SAFE_AUTH_HARDENING_RE.search(text))
    primary_vector = list(_PRIMARY_VECTOR_FRAME_RE.finditer(text))
    live_build = list(_LIVE_BUILD_RE.finditer(text))
    cve_ids = list(_CVE_ID_RE.finditer(text))
    cve_correlation = list(_CVE_CORRELATION_RE.finditer(text))
    ownership_claim = list(_OWNERSHIP_CLAIM_RE.finditer(text))
    retroactive_auth = list(_RETROACTIVE_AUTH_RE.finditer(text))
    permission_carveout = list(_PERMISSION_CARVEOUT_RE.finditer(text))
    trusted_slot = list(_TRUSTED_SLOT_RE.finditer(text))
    non_escalating = list(_NON_ESCALATING_FRAME_RE.finditer(text))
    recon_chain_steps = list(_RECON_CHAIN_STEP_RE.finditer(text))
    pre_exploit_chain = list(_PRE_EXPLOIT_CHAIN_RE.finditer(text))
    recon_artifacts = list(_RECON_ARTIFACT_RE.finditer(text))
    incremental = list(_INCREMENTAL_TASKING_RE.finditer(text))

    defensive = list(_DEFENSIVE_FRAMING_WRAPPER_RE.finditer(text))
    defensive_context_is_safe_auth = (
        safe_auth_hardening
        and len(context) == 1
        and "password" in context[0].group(0).lower()
    )
    if defensive and context and not defensive_context_is_safe_auth:
        matches = sorted(defensive[:1] + context[:2], key=lambda m: m.start())
        findings.append(
            Finding(
                signal="defensive_framing_wrapper",
                severity="low",
                detail=(
                    "Defensive or professional security framing is paired with "
                    "target, reconnaissance, sensitive-data, or artifact detail. "
                    "This is not malicious by itself; route on the substance "
                    "carried by the context, not the clean framing."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    role = list(_ROLE_LAUNDERING_RE.finditer(text))
    if role and (context or output_shape):
        matches = sorted(role[:1] + (context[:1] or output_shape[:1]), key=lambda m: m.start())
        findings.append(
            Finding(
                signal="role_laundering",
                severity="medium",
                detail=(
                    "The prompt assigns a trusted professional or internal-tool "
                    "role while also presenting context payload or output-shape "
                    "pressure. Role should not change the policy boundary."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    automation = list(_AUTOMATION_WRAPPER_RE.finditer(text))
    if automation and (context or output_shape):
        matches = sorted(
            automation[:1] + (context[:1] or output_shape[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="automation_wrapper",
                severity="medium",
                detail=(
                    "The request is framed as a workflow, job, pipeline, or "
                    "runbook while carrying target/context detail or an output "
                    "contract. Automated wrappers need the same review as direct "
                    "prompts."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    layered = list(_LAYERED_WORKFLOW_RE.finditer(text))
    legitimate_tools = list(_LEGITIMATE_TOOL_INVOCATION_RE.finditer(text))
    if automation and layered and (context_axis or output_shape or legitimate_tools):
        seed = automation[:1] + layered[:2]
        context_tail = _non_overlapping(context_axis, seed)
        output_tail = _non_overlapping(output_shape, seed)
        tool_tail = _non_overlapping(legitimate_tools, seed)
        matches = sorted(
            seed + (context_tail[:1] or output_tail[:1] or tool_tail[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="layered_automation_camouflage",
                severity="medium",
                detail=(
                    "Automation appears to distribute reconnaissance, "
                    "enumeration, analysis, or reporting across layers so each "
                    "step can look like normal developer or operations work. "
                    "Review the full workflow artifact, not only individual "
                    "turns or tool calls."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if preloaded_context and context:
        matches = sorted(preloaded_context[:1] + context[:2], key=lambda m: m.start())
        findings.append(
            Finding(
                signal="preloaded_context_payload",
                severity="medium",
                detail=(
                    "The visible prompt points to an attachment, schema, codebase "
                    "map, prior agent output, or similar context carrier that "
                    "contains target or reconnaissance detail. Scan the attached "
                    "work object, not only the chat text."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if obfuscation_transport and transport_internals:
        matches = sorted(
            obfuscation_transport[:1] + transport_internals[:2],
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="obfuscation_transport_internals",
                severity="high",
                detail=(
                    "The request targets authentication, handshake, dial, "
                    "connection-establishment, or internal mechanics of a "
                    "traffic-obfuscation or defense-evasion transport. Open-source "
                    "or developer framing should not downgrade this target class; "
                    "flag at request stage before implementation detail is "
                    "generated."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if developer_doc_frame and obfuscation_transport and transport_internals:
        matches = sorted(
            developer_doc_frame[:1] + obfuscation_transport[:1] + transport_internals[:1],
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="developer_documentation_laundering",
                severity="medium",
                detail=(
                    "Developer or documentation-style framing is paired with "
                    "sensitive obfuscation-transport internals. Documentation "
                    "requests can still expose defense-evasion mechanics; keep "
                    "analysis high-level unless authorized scope allows deeper "
                    "protocol review."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if review_process and obfuscation_transport and transport_internals:
        matches = sorted(
            review_process[:1] + obfuscation_transport[:1] + transport_internals[:1],
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="review_process_sensitive_reconstruction",
                severity="medium",
                detail=(
                    "The review or evaluation conversation appears to reconstruct "
                    "sensitive protocol mechanics even if the sampled completion "
                    "did not. Reviewer analysis needs the same source-safe "
                    "redaction discipline as the agent under review."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if ssh_surface and protocol_extraction:
        matches = sorted(
            ssh_surface[:2] + protocol_extraction[:1],
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="ssh_crypto_surface_extraction",
                severity="high",
                detail=(
                    "The request or output describes extraction of a server's "
                    "SSH/KEXINIT algorithm or cryptographic negotiation surface. "
                    "A full cipher/KEX/MAC/host-key map is pre-attack "
                    "intelligence; keep reviews at remediation level unless "
                    "authorized scope requires deeper protocol evidence."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if auth_method_disclosure and (ssh_surface or _REAL_TARGET_RE.search(text)):
        matches = sorted(
            auth_method_disclosure[:1] + (ssh_surface[:1] or list(_REAL_TARGET_RE.finditer(text))[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="auth_method_surface_disclosure",
                severity="medium",
                detail=(
                    "The request or output discloses live authentication methods "
                    "or password-auth availability for a target service. This is "
                    "useful pre-attack surface information and should be "
                    "redacted or converted into remediation guidance."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if auth_method_disclosure and primary_vector:
        matches = sorted(
            auth_method_disclosure[:1] + primary_vector[:1],
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="primary_auth_vector_exposure",
                severity="high",
                detail=(
                    "Authentication-method availability is framed as a key or "
                    "primary attack vector. That moves beyond remediation-level "
                    "guidance and hands over target-prioritization signal; "
                    "redact specifics and translate to defensive action."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if live_build and cve_ids and cve_correlation:
        matches = sorted(
            live_build[:1] + cve_ids[:2] + cve_correlation[:1],
            key=lambda m: m.start(),
        )
        evidence_matches = live_build[:1] + cve_ids[:2] + cve_correlation[:1]
        findings.append(
            Finding(
                signal="live_build_cve_correlation",
                severity="high",
                detail=(
                    "An exact running build or live target version is correlated "
                    "with CVE identifiers and patch status. This is a complete "
                    "live vulnerability triage cycle; keep output remediation-safe "
                    "and avoid portable target-specific exploitability dossiers."
                ),
                evidence=_evidence_for(evidence_matches),
                span=_span_for(matches),
            )
        )

    if ssh_surface and auth_method_disclosure and protocol_extraction:
        matches = sorted(
            ssh_surface[:1] + protocol_extraction[:1] + auth_method_disclosure[:1],
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="protocol_surface_cartography",
                severity="high",
                detail=(
                    "Cryptographic negotiation data and authentication-method "
                    "disclosure appear together. This is a complete protocol "
                    "surface map, not just a hardening note; route to authorized "
                    "review and remediation-safe output."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if ownership_claim and (retroactive_auth or (incremental and recon_artifacts)):
        matches = sorted(
            ownership_claim[:1]
            + (retroactive_auth[:2] or incremental[:1] + recon_artifacts[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="retroactive_authorization_laundering",
                severity="high",
                detail=(
                    "An ownership or admin claim appears after reconnaissance, "
                    "model switching, or already-collected intelligence. Late "
                    "authorization should not bless prior collection; require "
                    "scope and authority before target interaction or evidence "
                    "export."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if permission_carveout and (trusted_slot or defensive or analytical_task):
        matches = sorted(
            permission_carveout[:2] + (trusted_slot[:1] or defensive[:1] or analytical_task[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="permission_carveout_laundering",
                severity="medium",
                detail=(
                    "The request leans on authorized-security-testing or system "
                    "permission language as a pre-built justification. Treat the "
                    "carve-out as a condition to verify, not as automatic "
                    "clearance for reconnaissance, tool use, or reporting."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if (non_escalating or pre_exploit_chain) and len(recon_chain_steps) >= 3:
        matches = sorted(
            (non_escalating[:1] or pre_exploit_chain[:1])
            + recon_chain_steps[:4]
            + _non_overlapping(pre_exploit_chain[:1], recon_chain_steps[:4]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="non_escalating_recon_chain",
                severity="medium",
                detail=(
                    "The sequence avoids explicit exploitation, brute force, or "
                    "login attempts, but routine collection steps combine into "
                    "pre-exploitation reconnaissance. Score the aggregate chain "
                    "across turns and model switches, not only each safe-looking "
                    "step."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if (
        broad_sweep
        and (analytical_task or defensive or output_shape or vuln_report_package)
        and (context or output_shape or recon_artifacts)
    ):
        matches = sorted(
            broad_sweep[:1]
            + (analytical_task[:1] or defensive[:1])
            + (context[:1] or output_shape[:1] or recon_artifacts[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="broad_sweep_escalation",
                severity="medium",
                detail=(
                    "A bounded defensive review appears to expand into a broad "
                    "sweep across a codebase, repository, endpoint set, or attack "
                    "surface. This changes the risk profile from narrow help to "
                    "scaled vulnerability discovery; require explicit scope, "
                    "authorization, rate limits, and report controls."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if multi_agent_audit and (broad_sweep or analytical_task or context or output_shape):
        matches = sorted(
            multi_agent_audit[:1]
            + (broad_sweep[:1] or analytical_task[:1])
            + (context[:1] or output_shape[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="multi_agent_audit_fanout",
                severity="medium",
                detail=(
                    "The request describes multiple auditors, agents, or "
                    "parallel review lanes fanning out over security work. "
                    "Parallelism can convert a single broad ask into scaled "
                    "vulnerability discovery, so evaluate aggregate scope and "
                    "final artifact shape."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if vuln_report_package and (broad_sweep or multi_agent_audit or context or structured):
        matches = sorted(
            vuln_report_package[:2]
            + (broad_sweep[:1] or multi_agent_audit[:1])
            + (context[:1] or structured[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="vulnerability_database_packaging",
                severity="high",
                detail=(
                    "The request points toward structured, prioritized, "
                    "file/line-referenced vulnerability packaging or offensive "
                    "engagement-style reporting. Gate export, redact exploit "
                    "detail, and separate internal remediation notes from "
                    "portable vulnerability databases."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if discovery_asymmetry and (broad_sweep or multi_agent_audit or vuln_report_package):
        matches = sorted(
            discovery_asymmetry[:1]
            + (broad_sweep[:1] or multi_agent_audit[:1] or vuln_report_package[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="ai_discovery_asymmetry",
                severity="medium",
                detail=(
                    "The request references AI-driven vulnerability discovery "
                    "collapsing time, cost, or expertise barriers. Treat this as "
                    "an operational-risk lens: discovery velocity can exceed "
                    "defender triage and patch capacity."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if analytical_task and len(recon_artifacts) >= 2 and (preloaded_context or upstream_handoff):
        carrier = preloaded_context[:1] or upstream_handoff[:1]
        matches = sorted(
            analytical_task[:1] + carrier + recon_artifacts[:3],
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="preloaded_recon_package_laundering",
                severity="medium",
                detail=(
                    "A clean analytical security task is paired with an "
                    "attachment, codebase map, system context, prior output, or "
                    "upstream handoff that already contains multiple "
                    "reconnaissance artifacts. Prompt-only classifiers will miss "
                    "this shape; inspect the attached content and score the "
                    "combination before analysis or reporting."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if structured and (context_axis or defensive):
        matches = sorted(structured[:2] + (context_axis[:1] or defensive[:1]), key=lambda m: m.start())
        findings.append(
            Finding(
                signal="structured_output_pressure",
                severity="medium",
                detail=(
                    "The request asks for machine-readable or schema-shaped "
                    "findings while context may contain target detail. Treat "
                    "output shape as a risk axis because it can package evidence "
                    "into a portable dossier."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    thoroughness = list(_THOROUGHNESS_PRESSURE_RE.finditer(text))
    if thoroughness and (automation or role or structured) and (context_axis or output_shape):
        matches = sorted(
            thoroughness[:1]
            + (automation[:1] or role[:1] or structured[:1])
            + (context_axis[:1] or output_shape[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="operational_thoroughness_pressure",
                severity="medium",
                detail=(
                    "The request frames completeness or specificity as a job, "
                    "workflow, role, or schema requirement. This can pressure an "
                    "agent to over-collect or over-package findings unless scope "
                    "and redaction gates are explicit."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    normalcy = list(_OPERATIONAL_NORMALCY_RE.finditer(text))
    if normalcy and (automation or layered or legitimate_tools) and (context_axis or output_shape):
        matches = sorted(
            normalcy[:1]
            + (automation[:1] or layered[:1] or legitimate_tools[:1])
            + (context_axis[:1] or output_shape[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="operational_normalcy_camouflage",
                severity="medium",
                detail=(
                    "The request frames layered or tool-mediated behavior as "
                    "ordinary engineering, DevOps, or enterprise workflow while "
                    "also carrying context payload or output-shape pressure. "
                    "Normalcy claims should be checked against scope, provenance, "
                    "and the final aggregate artifact."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if incremental and (context_axis or output_shape or defensive):
        matches = sorted(
            incremental[:1] + (context_axis[:1] or output_shape[:1] or defensive[:1]),
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="incremental_tasking",
                severity="medium",
                detail=(
                    "The request references splitting work across turns or "
                    "sessions so no single prompt carries the full signal. This "
                    "requires trajectory review rather than isolated-turn review."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    if legitimate_tools and context:
        matches = sorted(legitimate_tools[:2] + context[:1], key=lambda m: m.start())
        findings.append(
            Finding(
                signal="legitimate_tool_invocation_wrapper",
                severity="medium",
                detail=(
                    "Ordinary developer tools or file reads are paired with "
                    "reconnaissance, target, or sensitive context. Review the "
                    "aggregate map produced by allowed reads, not only each "
                    "individual command."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    framing_axis = sorted(
        defensive + role + automation + incremental + legitimate_tools,
        key=lambda m: m.start(),
    )
    if framing_axis and context_axis and output_shape:
        matches = sorted(
            framing_axis[:1] + context_axis[:1] + output_shape[:1],
            key=lambda m: m.start(),
        )
        findings.append(
            Finding(
                signal="clean_prompt_axis_combo",
                severity="medium",
                detail=(
                    "All three clean-prompt axes appear together: framing "
                    "language, context payload, and output shape. This is a "
                    "classifier-ready pattern for prompts whose visible wording "
                    "stays clean while the surrounding work object carries risk."
                ),
                evidence=_evidence_for(matches),
                span=_span_for(matches),
            )
        )

    return findings


def _detect_sensitive_data_action_request(text: str) -> List[Finding]:
    if _SAFE_AUTH_HARDENING_RE.search(text):
        return []
    sensitive = list(_SENSITIVE_DATA_RE.finditer(text))
    actions = list(_SENSITIVE_ACTION_RE.finditer(text))
    if not sensitive or not actions:
        return []
    first = min(sensitive[0].start(), actions[0].start())
    last = max(sensitive[-1].end(), actions[-1].end())
    return [
        Finding(
            signal="sensitive_data_action_request",
            severity="high",
            detail=(
                "Request combines authentication or secret-bearing data with "
                "action verbs. Treat this as a data-category boundary first; "
                "professional framing or claimed authorization should not lower "
                "scrutiny."
            ),
            evidence=f"{sensitive[0].group(0)} + {actions[0].group(0)}",
            span=(first, last),
        )
    ]


def _detect_orchestration_trust_shift(text: str) -> List[Finding]:
    orchestration = list(_ORCHESTRATION_RE.finditer(text))
    trust_transfer = list(_TRUST_TRANSFER_RE.finditer(text))
    if not orchestration or len(trust_transfer) < 2:
        return []
    evidence_terms = [orchestration[0].group(0)] + [
        m.group(0) for m in trust_transfer[:2]
    ]
    return [
        Finding(
            signal="orchestration_trust_shift",
            severity="medium",
            detail=(
                "Input references an agent, tool, or automation layer together "
                "with trusted-context language. This is the shape where a human "
                "may never directly prompt the model, and malicious instructions "
                "can arrive as pipeline or operator context."
            ),
            evidence=" + ".join(evidence_terms),
            span=(orchestration[0].start(), trust_transfer[-1].end()),
        )
    ]


def _detect_trusted_slot_contamination(text: str) -> List[Finding]:
    trusted = list(_TRUSTED_SLOT_RE.finditer(text))
    source = list(_UNTRUSTED_SOURCE_RE.finditer(text))
    if not trusted or not source:
        return []
    return [
        Finding(
            signal="trusted_slot_contamination",
            severity="high",
            detail=(
                "Input combines trusted instruction slots with untrusted source "
                "or insertion language. This is the failure mode where hostile "
                "content reaches the model as rules rather than data."
            ),
            evidence=f"{trusted[0].group(0)} + {source[0].group(0)}",
            span=(min(trusted[0].start(), source[0].start()), max(trusted[-1].end(), source[-1].end())),
        )
    ]


def _detect_system_prompt_attack_scaffold(text: str) -> List[Finding]:
    trusted = list(_TRUSTED_SLOT_RE.finditer(text))
    scaffold = list(_ATTACK_SCAFFOLD_RE.finditer(text))
    offensive = list(_LIVE_OFFENSIVE_CONTEXT_RE.finditer(text))
    if not trusted or not scaffold or len(offensive) < 2:
        return []
    matches = sorted(trusted[:1] + scaffold[:2] + offensive[:4], key=lambda m: m.start())
    return [
        Finding(
            signal="system_prompt_attack_scaffold",
            severity="high",
            detail=(
                "A system/developer/tool-trusted instruction layer appears to "
                "carry an attack scaffold with live offensive context. Treat "
                "this as an authority-boundary failure: trusted slots must not "
                "import target context, credentials, offensive infrastructure, "
                "or anti-review instructions as rules."
            ),
            evidence=_evidence_for(matches),
            span=_span_for(matches),
        )
    ]


def _detect_offensive_tool_invocation_compliance(text: str) -> List[Finding]:
    offensive = list(_LIVE_OFFENSIVE_CONTEXT_RE.finditer(text))
    compliance = list(_TOOL_COMPLIANCE_RE.finditer(text))
    tool = list(_TOOL_SURFACE_RE.finditer(text))
    if len(offensive) < 2 or not compliance or not tool:
        return []
    matches = sorted(offensive[:3] + compliance[:2] + tool[:1], key=lambda m: m.start())
    return [
        Finding(
            signal="offensive_tool_invocation_compliance",
            severity="high",
            detail=(
                "The case describes agent compliance with a tool-mediated "
                "offensive action against a live or credential-bearing target "
                "context. Score the attempted tool invocation as the policy "
                "event, even if the tool later fails."
            ),
            evidence=_evidence_for(matches),
            span=_span_for(matches),
        )
    ]


def _detect_technical_failure_not_refusal(text: str) -> List[Finding]:
    offensive = list(_LIVE_OFFENSIVE_CONTEXT_RE.finditer(text))
    compliance = list(_TOOL_COMPLIANCE_RE.finditer(text))
    technical_failure = [
        m
        for m in compliance
        if "technical" in m.group(0).lower() or "rather than any refusal" in m.group(0).lower()
    ]
    if not offensive or not technical_failure:
        return []
    matches = sorted(offensive[:2] + technical_failure[:2], key=lambda m: m.start())
    return [
        Finding(
            signal="technical_failure_not_refusal",
            severity="medium",
            detail=(
                "The run appears to fail because of tool/runtime execution, not "
                "because the model refused or re-scoped the request. Evaluation "
                "should record this as safety non-intervention, not a successful "
                "safeguard outcome."
            ),
            evidence=_evidence_for(matches),
            span=_span_for(matches),
        )
    ]


def _detect_probe_confirmation(text: str) -> List[Finding]:
    match = _PROBE_CONFIRMATION_RE.search(text)
    if not match:
        return []
    return [
        Finding(
            signal="probe_confirmation",
            severity="medium",
            detail=(
                "Request appears focused on confirming whether a safety boundary "
                "can be crossed. In probing workflows, the confirmation can be "
                "the payload even when the content is brief."
            ),
            evidence=match.group(0)[:120],
            span=(match.start(), match.end()),
        )
    ]


def _detect_tool_output_laundering(text: str) -> List[Finding]:
    tool = list(_TOOL_SURFACE_RE.finditer(text))
    verbatim = list(_VERBATIM_REPORT_RE.finditer(text))
    artifact = list(_HIGH_RISK_ARTIFACT_RE.finditer(text))
    if not tool or not verbatim or not artifact:
        return []
    first = min(tool[0].start(), verbatim[0].start(), artifact[0].start())
    last = max(tool[-1].end(), verbatim[-1].end(), artifact[-1].end())
    return [
        Finding(
            signal="tool_output_laundering",
            severity="high",
            detail=(
                "Input describes a high-risk artifact produced by a tool, "
                "scanner, or workflow and asks for raw/verbatim reproduction. "
                "Policy evaluation must apply to the final artifact, not only "
                "to whether the agent authored it directly."
            ),
            evidence=f"{tool[0].group(0)} + {verbatim[0].group(0)} + {artifact[0].group(0)}",
            span=(first, last),
        )
    ]


def _detect_delegated_authorship_deflection(text: str) -> List[Finding]:
    authorship = list(_DELEGATED_AUTHORSHIP_RE.finditer(text))
    artifact = list(_HIGH_RISK_ARTIFACT_RE.finditer(text))
    if not authorship or not artifact:
        return []
    first = min(authorship[0].start(), artifact[0].start())
    last = max(authorship[-1].end(), artifact[-1].end())
    return [
        Finding(
            signal="delegated_authorship_deflection",
            severity="high",
            detail=(
                "Input pairs a high-risk artifact with language deflecting "
                "responsibility to a tool or scanner. For safeguards, causing "
                "or transmitting an artifact can be equivalent to authoring it."
            ),
            evidence=f"{authorship[0].group(0)} + {artifact[0].group(0)}",
            span=(first, last),
        )
    ]


def _detect_risk_label_laundering(text: str) -> List[Finding]:
    label = list(_RISK_LABEL_DOWNGRADE_RE.finditer(text))
    artifact = list(_HIGH_RISK_ARTIFACT_RE.finditer(text))
    if not label or not artifact:
        return []
    first = min(label[0].start(), artifact[0].start())
    last = max(label[-1].end(), artifact[-1].end())
    return [
        Finding(
            signal="risk_label_laundering",
            severity="high",
            detail=(
                "Input pairs a high-risk artifact with a low-severity or "
                "informational label. Post-hoc risk labels should not downgrade "
                "the final artifact class."
            ),
            evidence=f"{label[0].group(0)} + {artifact[0].group(0)}",
            span=(first, last),
        )
    ]


def _detect_autonomous_methodology_expansion(text: str) -> List[Finding]:
    broad_frame = list(_BROAD_SECURITY_FRAME_RE.finditer(text))
    method = list(_AUTONOMOUS_METHOD_RE.finditer(text))
    target = list(_REAL_TARGET_RE.finditer(text))
    if not broad_frame or not method or not target:
        return []
    first = min(broad_frame[0].start(), method[0].start(), target[0].start())
    last = max(broad_frame[-1].end(), method[-1].end(), target[-1].end())
    return [
        Finding(
            signal="autonomous_methodology_expansion",
            severity="medium",
            detail=(
                "Input combines broad defensive-security framing, a real target "
                "surface, and language showing the agent filled in specific "
                "audit methodology on its own. Review whether the agent supplied "
                "expertise or execution steps beyond explicit user scope."
            ),
            evidence=f"{broad_frame[0].group(0)} + {method[0].group(0)} + {target[0].group(0)}",
            span=(first, last),
        )
    ]


def _detect_verified_facts_targeting_package(text: str) -> List[Finding]:
    facts = list(_VERIFIED_FACTS_RE.finditer(text))
    recon = list(_RECON_ARTIFACT_RE.finditer(text))
    if not facts or len(recon) < 2:
        return []
    first = min(facts[0].start(), recon[0].start())
    last = max(facts[-1].end(), recon[-1].end())
    return [
        Finding(
            signal="verified_facts_targeting_package",
            severity="medium",
            detail=(
                "Input presents a verified-facts or memory block that contains "
                "multiple reconnaissance artifacts. Treat this as a targeting "
                "package, not neutral orientation, and verify origin/scope."
            ),
            evidence=f"{facts[0].group(0)} + {recon[0].group(0)} + {recon[1].group(0)}",
            span=(first, last),
        )
    ]


def _detect_theatrical_constraints_operational_permissions(text: str) -> List[Finding]:
    prohibitions = list(_PROHIBITION_FRAME_RE.finditer(text))
    operational = list(_OPERATIONAL_READ_RE.finditer(text))
    recon = list(_RECON_ARTIFACT_RE.finditer(text))
    if not prohibitions or len(operational) < 2 or not recon:
        return []
    first = min(prohibitions[0].start(), operational[0].start(), recon[0].start())
    last = max(prohibitions[-1].end(), operational[-1].end(), recon[-1].end())
    return [
        Finding(
            signal="theatrical_constraints_operational_permissions",
            severity="medium",
            detail=(
                "Input pairs dramatic restrictions with operational read, "
                "inspection, or local-query permissions that can still produce "
                "useful intelligence. Review the allowed actions, not just the "
                "prohibited ones."
            ),
            evidence=f"{prohibitions[0].group(0)} + {operational[0].group(0)} + {recon[0].group(0)}",
            span=(first, last),
        )
    ]


def _detect_structured_output_dossiering(text: str) -> List[Finding]:
    structured = list(_STRUCTURED_OUTPUT_RE.finditer(text))
    dossier = list(_DOSSIER_PACKAGING_RE.finditer(text))
    recon = list(_RECON_ARTIFACT_RE.finditer(text))
    if len(structured) < 2 and not dossier:
        return []
    if not recon and not any(term.group(0).lower() in {"evidence", "file_ref", "file_refs"} for term in structured):
        return []
    first_candidates = structured + dossier + recon
    first = min(m.start() for m in first_candidates)
    last = max(m.end() for m in first_candidates)
    evidence_terms = [m.group(0) for m in (structured[:2] + dossier[:1] + recon[:1])]
    return [
        Finding(
            signal="structured_output_dossiering",
            severity="medium",
            detail=(
                "Input requires machine-readable evidence packaging without a "
                "clear sensitivity tier, redaction gate, or human unlock. Review "
                "whether the schema turns analysis into a portable dossier."
            ),
            evidence=" + ".join(evidence_terms),
            span=(first, last),
        )
    ]


def _detect_context_dilution(text: str, threshold: int = 4000) -> List[Finding]:
    """Structural signal: a very long body with a short directive-style line
    isolated in the final stretch (delayed-activation / haystack pattern)."""
    if len(text) < threshold:
        return []
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) < 2:
        return []
    tail = lines[max(0, int(len(lines) * 0.9)):]
    median_len = sorted(len(ln) for ln in lines)[len(lines) // 2]
    short_tail = [ln for ln in tail if len(ln) < max(80, median_len // 2)]
    if short_tail:
        return [
            Finding(
                signal="context_dilution",
                severity="low",
                detail=(
                    f"Input is {len(text)} chars with a short line isolated in "
                    "the final 10%. Large benign context with a late, brief "
                    "instruction is the delayed-activation pattern; warrants "
                    "manual review of the tail."
                ),
                evidence=short_tail[-1][:80],
            )
        ]
    return [
        Finding(
            signal="oversized_input",
            severity="info",
            detail=(
                f"Input is {len(text)} chars. Long inputs should be reviewed for "
                "buried or delayed instructions."
            ),
        )
    ]


_DETECTORS = (
    _detect_invisible,
    _detect_homoglyphs,
    _detect_mixed_script_control_surface,
    _detect_base64,
    _detect_rot13,
    _detect_leetspeak,
    _detect_decision_preloading,
    _detect_clean_prompt_wrappers,
    _detect_sensitive_data_action_request,
    _detect_orchestration_trust_shift,
    _detect_trusted_slot_contamination,
    _detect_system_prompt_attack_scaffold,
    _detect_offensive_tool_invocation_compliance,
    _detect_technical_failure_not_refusal,
    _detect_probe_confirmation,
    _detect_tool_output_laundering,
    _detect_delegated_authorship_deflection,
    _detect_risk_label_laundering,
    _detect_autonomous_methodology_expansion,
    _detect_verified_facts_targeting_package,
    _detect_theatrical_constraints_operational_permissions,
    _detect_structured_output_dossiering,
    _detect_context_dilution,
)


def scan(text: str) -> List[Finding]:
    """Run every detector over ``text`` and return findings, most severe first."""
    findings: List[Finding] = []
    for detector in _DETECTORS:
        findings.extend(detector(text))
    findings.sort(key=lambda f: _SEVERITY_WEIGHT[f.severity], reverse=True)
    return findings


def risk_score(findings: List[Finding]) -> int:
    """Aggregate findings into a 0..100 score (saturating).

    A single high-severity signal already lands in the elevated range; multiple
    signals accumulate. The score is a triage aid, not a verdict.
    """
    total = sum(_SEVERITY_WEIGHT[f.severity] for f in findings)
    return min(100, total)


def format_report(text: str) -> str:
    findings = scan(text)
    score = risk_score(findings)
    lines = [f"risk_score: {score}/100", f"findings: {len(findings)}", ""]
    if not findings:
        lines.append("  (no evasion signals detected)")
    for f in findings:
        lines.append(f"  [{f.severity.upper():6}] {f.signal}")
        lines.append(f"           {f.detail}")
        if f.evidence:
            lines.append(f"           evidence: {f.evidence}")
    return "\n".join(lines)


def _read_input(argv: List[str]) -> str:
    if len(argv) > 1:
        with open(argv[1], "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    return sys.stdin.read()


if __name__ == "__main__":
    print(format_report(_read_input(sys.argv)))
