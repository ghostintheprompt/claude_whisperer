# Browser Extension - Legacy Spike

This directory contains an older Manifest V3 browser-extension experiment. It
has useful UI ideas, but it is not the current recommended entry point for
frontier-model evaluation.

## Current Status

Treat this as **legacy research archive** until refactored.

Known issues:

- hardcoded Claude-version language from an older project era;
- direct browser API-key storage and API calls, which should not be used for
  production frontier testing;
- casual prompt injection UX that needs explicit warning gates and manual
  review;
- stale model defaults;
- old "exploit generation" language that does not match the current
  red-to-blue methodology;
- missing operational guardrails for scope, authorization, evidence capture,
  and source-safe exports.

## What Should Replace It

The next version should be a local-first review harness:

- no production API keys in browser storage;
- optional local proxy for provider calls;
- explicit authorization and risk warning before any live action;
- manual copy/review as the default path;
- exact provider, model ID, date, tool configuration, and interface captured per
  run;
- detector integration from `../defense/evasion_signal_detector.py`;
- source-safe export templates for case studies and SOC handoff;
- clear separation between raw private findings and public derivative reports.

## Recommended Entry Point Today

Use the defensive scanner and methodology docs first:

```bash
cd ..
python3 -m unittest discover -s defense -p 'test_*.py'
echo "Review this agent pipeline instruction" | python3 defense/evasion_signal_detector.py
```

See:

- [Important Findings Method](../docs/IMPORTANT_FINDINGS_METHOD.md)
- [Defense Detector](../defense/README.md)
- [Root README](../README.md)
