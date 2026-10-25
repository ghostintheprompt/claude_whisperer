#!/usr/bin/env python3
"""Isolated safeguards-client tests using synthetic markers and mocked HTTP."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.safeguards_client import SafeguardsClient


class TestSafeguardsClient(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="safeguards-test-")
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        patterns = root / "patterns"
        patterns.mkdir()
        fixtures = {
            "policy_patterns.json": [
                {"id": "policy_pattern_1", "pattern": "policy-marker-a", "severity": "high", "confidence": 0.8},
                {"id": "policy_pattern_2", "pattern": "policy-marker-b", "severity": "high"},
            ],
            "child_safety_patterns.json": [
                {"id": "child_safety_pattern_1", "pattern": "child-safety-marker", "severity": "high", "confidence": 0.95},
            ],
            "content_moderation_patterns.json": [
                {"id": "content_pattern_1", "pattern": "moderation-marker", "severity": "high"},
            ],
        }
        for filename, entries in fixtures.items():
            (patterns / filename).write_text(json.dumps({"patterns": entries}))
        config = {
            "api_url": "https://api.anthropic.com/v1/messages",
            "default_model": "fixture-model",
            "timeout": 30,
            "logging": {"enabled": True, "log_requests": True, "log_responses": True},
            "active_safeguards": {"policy_violation": True, "child_safety": True, "content_moderation": True},
            "interventions": {"block_policy_violations": True, "block_content_moderation": True, "alert_threshold": 0.7, "warn_threshold": 0.5},
            "patterns_path": str(patterns),
        }
        config_path = root / "config.json"
        config_path.write_text(json.dumps(config))
        # Fail closed if a test ever escapes the injected HTTP mock.
        network_guard = patch("requests.sessions.Session.request", side_effect=AssertionError("Unexpected real HTTP request"))
        network_guard.start()
        self.addCleanup(network_guard.stop)
        self.client = SafeguardsClient(api_key="test_key", config_path=str(config_path))
        self.addCleanup(self.client.session.close)
        self.session_mock = MagicMock(spec=requests.Session)
        self.response = {"id": "msg_123", "model": "fixture-model", "content": [{"type": "text", "text": "A clean fixture response"}]}
        self.session_mock.post.return_value.json.return_value = self.response
        self.client.session = self.session_mock

    def test_initialization(self):
        self.assertEqual(self.client.api_key, "test_key")
        self.assertEqual(self.client.config["default_model"], "fixture-model")
        self.assertEqual(set(self.client.patterns), {"policy_pattern_1", "policy_pattern_2", "child_safety_pattern_1", "content_pattern_1"})
        self.assertEqual({p["category"] for p in self.client.patterns.values()}, {"policy_violation", "child_safety", "content_moderation"})
        self.assertEqual(self.client.patterns["policy_pattern_1"]["confidence"], 0.8)
        self.assertEqual(self.client.patterns["policy_pattern_2"]["confidence"], 0.9)

    def test_detect_policy_violations(self):
        result = self.client.detect_policy_violations("Contains POLICY-MARKER-A")
        self.assertTrue(result["violations_detected"])
        self.assertEqual([m["pattern"] for m in result["matches"]], ["policy_pattern_1"])
        self.assertEqual(result["highest_score"], 0.8)
        clean = self.client.detect_policy_violations("A clean fixture message")
        self.assertFalse(clean["violations_detected"])
        self.assertEqual(clean["matches"], [])

    def test_detect_child_safety_concerns(self):
        result = self.client.detect_child_safety_concerns("Contains child-safety-marker")
        self.assertTrue(result["concerns_detected"])
        self.assertEqual([m["pattern"] for m in result["matches"]], ["child_safety_pattern_1"])
        self.assertEqual(result["highest_score"], 0.95)
        self.assertFalse(self.client.detect_child_safety_concerns("A clean fixture message")["concerns_detected"])

    def test_detect_content_moderation(self):
        result = self.client.detect_content_moderation("Contains moderation-marker")
        self.assertTrue(result["concerns_detected"])
        self.assertEqual([m["pattern"] for m in result["matches"]], ["content_pattern_1"])
        self.assertEqual(result["highest_score"], 0.9)
        self.assertFalse(self.client.detect_content_moderation("A clean fixture message")["concerns_detected"])

    def test_threshold_and_disabled_category(self):
        self.assertTrue(self.client.detect_policy_violations("policy-marker-a", threshold=0.8)["violations_detected"])
        self.assertFalse(self.client.detect_policy_violations("policy-marker-a", threshold=0.81)["violations_detected"])
        self.client.active_safeguards["policy_violation"] = False
        self.assertFalse(self.client.detect_policy_violations("policy-marker-a")["violations_detected"])
        self.assertTrue(self.client.detect_child_safety_concerns("child-safety-marker")["concerns_detected"])

    def test_analyze_message(self):
        result = self.client.analyze_message("policy-marker-a child-safety-marker")
        self.assertTrue(result["policy_violations"]["violations_detected"])
        self.assertTrue(result["child_safety_concerns"]["concerns_detected"])
        self.assertTrue(result["should_block"])
        clean = self.client.analyze_message("A clean fixture message")
        self.assertFalse(clean["policy_violations"]["violations_detected"])
        self.assertFalse(clean["child_safety_concerns"]["concerns_detected"])
        self.assertFalse(clean["should_block"])

    def test_create_message(self):
        messages = [{"role": "user", "content": "A clean fixture message"}]
        response = self.client.create_message(messages)
        self.assertEqual(response, self.response)
        self.session_mock.post.assert_called_once_with(
            self.client.config["api_url"],
            json={"model": "fixture-model", "messages": messages, "max_tokens": 1024},
            timeout=30, stream=False,
        )
        self.session_mock.post.return_value.raise_for_status.assert_called_once()
        self.session_mock.post.reset_mock()
        blocked = self.client.create_message([{"role": "user", "content": "policy-marker-a"}])
        self.session_mock.post.assert_not_called()
        self.assertIn("error", blocked)
        self.assertTrue(blocked["analysis"]["policy_violations"]["violations_detected"])
        self.assertEqual(len(self.client.conversation_history), 1)

    def test_conversation_history(self):
        self.assertEqual(self.client.conversation_history, [])
        messages = [{"role": "user", "content": "A clean fixture message"}]
        self.client.create_message(messages)
        self.session_mock.post.assert_called_once()
        self.assertEqual(len(self.client.conversation_history), 1)
        entry = self.client.conversation_history[0]
        self.assertEqual(entry["request"]["messages"], messages)
        self.assertEqual(entry["response"], self.response)
        self.assertIsInstance(entry["timestamp"], str)
        self.client.clear_conversation_history()
        self.assertEqual(self.client.conversation_history, [])


class TestSafeguardsIntegration(unittest.TestCase):
    @unittest.skip("Live end-to-end workflow is not implemented; mocked client checks run above")
    def test_end_to_end_workflow(self):
        pass


if __name__ == "__main__":
    unittest.main()
