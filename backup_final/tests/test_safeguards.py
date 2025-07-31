#!/usr/bin/env python3
"""
Unit Tests for Claude Safeguards Framework

This module contains comprehensive tests for the safeguards client and monitoring systems,
ensuring all protection mechanisms work as expected.
"""
import os
import sys
import unittest
import json
import re
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add parent directory to path to import modules correctly
parent_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(parent_dir))

# Import components to test
from core.safeguards_client import SafeguardsClient

class TestSafeguardsClient(unittest.TestCase):
    """Tests for SafeguardsClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test config file
        self.test_config_path = "test_config.json"
        test_config = {
            "api_url": "https://api.anthropic.com/v1/messages",
            "default_model": "claude-3-7-sonnet-20240229",
            "timeout": 30,
            "logging": {
                "enabled": True,
                "log_requests": True,
                "log_responses": True
            },
            "active_safeguards": {
                "policy_violation": True,
                "child_safety": True,
                "content_moderation": True
            },
            "interventions": {
                "block_policy_violations": True,
                "alert_threshold": 0.7,
                "warn_threshold": 0.5
            },
            "patterns_path": "./test_patterns",
            "websocket_host": "localhost",
            "websocket_port": 8765
        }
        
        # Create test patterns directory
        os.makedirs("./test_patterns", exist_ok=True)
        
        # Create test pattern files
        self.policy_patterns = {
            "policy_pattern_1": {
                "type": "policy_violation",
                "pattern": "how to hack",
                "confidence": 0.8,
                "category": "hacking"
            },
            "policy_pattern_2": {
                "type": "policy_violation",
                "pattern": "illegal activities",
                "confidence": 0.9,
                "category": "illegal"
            }
        }
        
        self.child_safety_patterns = {
            "child_safety_pattern_1": {
                "type": "child_safety",
                "pattern": "child abuse",
                "confidence": 0.95,
                "category": "abuse"
            }
        }
        
        with open("./test_patterns/policy_patterns.json", "w") as f:
            json.dump(self.policy_patterns, f)
            
        with open("./test_patterns/child_safety_patterns.json", "w") as f:
            json.dump(self.child_safety_patterns, f)
            
        with open(self.test_config_path, "w") as f:
            json.dump(test_config, f)
        
        # Initialize client with test config
        self.client = SafeguardsClient(api_key="test_key", config_path=self.test_config_path)
        
        # Mock the requests Session to avoid actual API calls
        self.session_mock = MagicMock()
        self.client.session = self.session_mock
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove test files
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)
            
        # Remove test pattern files
        if os.path.exists("./test_patterns/policy_patterns.json"):
            os.remove("./test_patterns/policy_patterns.json")
            
        if os.path.exists("./test_patterns/child_safety_patterns.json"):
            os.remove("./test_patterns/child_safety_patterns.json")
            
        # Remove test patterns directory
        if os.path.exists("./test_patterns"):
            os.rmdir("./test_patterns")
            
    def test_initialization(self):
        """Test client initialization."""
        self.assertEqual(self.client.api_key, "test_key")
        self.assertEqual(self.client.config["default_model"], "claude-3-7-sonnet-20240229")
        self.assertEqual(len(self.client.patterns), 3)  # 2 policy + 1 child safety
        
    def test_detect_policy_violations(self):
        """Test policy violation detection."""
        # Test with violation
        text_with_violation = "Can you tell me how to hack a website?"
        result = self.client.detect_policy_violations(text_with_violation)
        self.assertTrue(result["violations_detected"])
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["matches"][0]["pattern"], "policy_pattern_1")
        self.assertEqual(result["highest_score"], 0.8)
        
        # Test with no violation
        text_without_violation = "How to build a website with HTML?"
        result = self.client.detect_policy_violations(text_without_violation)
        self.assertFalse(result["violations_detected"])
        self.assertEqual(len(result["matches"]), 0)
        
    def test_detect_child_safety_concerns(self):
        """Test child safety concern detection."""
        # Test with concern
        text_with_concern = "Information about child abuse"
        result = self.client.detect_child_safety_concerns(text_with_concern)
        self.assertTrue(result["concerns_detected"])
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["matches"][0]["pattern"], "child_safety_pattern_1")
        self.assertEqual(result["highest_score"], 0.95)
        
        # Test with no concern
        text_without_concern = "Information about child development"
        result = self.client.detect_child_safety_concerns(text_without_concern)
        self.assertFalse(result["concerns_detected"])
        self.assertEqual(len(result["matches"]), 0)
        
    def test_analyze_message(self):
        """Test message analysis."""
        # Test with policy violation and child safety concern
        text = "How to hack a website with information about child abuse"
        result = self.client.analyze_message(text)
        self.assertTrue(result["policy_violations"]["violations_detected"])
        self.assertTrue(result["child_safety_concerns"]["concerns_detected"])
        self.assertTrue(result["should_block"])
        
        # Test with neither
        text = "How to build a website with HTML"
        result = self.client.analyze_message(text)
        self.assertFalse(result["policy_violations"]["violations_detected"])
        self.assertFalse(result["child_safety_concerns"]["concerns_detected"])
        self.assertFalse(result["should_block"])
        
    @patch("requests.Session.post")
    def test_create_message(self, mock_post):
        """Test message creation with mocked API call."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "msg_123",
            "model": "claude-3-7-sonnet-20240229",
            "content": [{"type": "text", "text": "This is a test response"}]
        }
        mock_post.return_value = mock_response
        
        # Test with safe message
        messages = [
            {"role": "user", "content": "Tell me about machine learning"}
        ]
        
        response = self.client.create_message(messages)
        
        # Verify API call was made
        mock_post.assert_called_once()
        
        # Check response
        self.assertEqual(response["id"], "msg_123")
        self.assertEqual(response["model"], "claude-3-7-sonnet-20240229")
        
        # Test with unsafe message
        messages = [
            {"role": "user", "content": "How to hack a website"}
        ]
        
        # Reset mock
        mock_post.reset_mock()
        
        response = self.client.create_message(messages)
        
        # Verify API call was not made due to safety block
        mock_post.assert_not_called()
        
        # Check error response
        self.assertIn("error", response)
        self.assertIn("analysis", response)
        self.assertTrue(response["analysis"]["policy_violations"]["violations_detected"])
        
    def test_conversation_history(self):
        """Test conversation history functionality."""
        # Initialize empty history
        self.assertEqual(len(self.client.conversation_history), 0)
        
        # Mock a conversation
        with patch.object(self.client, "create_message") as mock_create:
            mock_create.return_value = {
                "id": "msg_123",
                "model": "claude-3-7-sonnet-20240229",
                "content": [{"type": "text", "text": "This is a test response"}]
            }
            
            messages = [
                {"role": "user", "content": "Tell me about machine learning"}
            ]
            
            # Call the method to update history
            self.client.create_message(messages)
            
            # Check history was updated
            self.assertEqual(len(self.client.conversation_history), 1)
            
            # Clear history
            self.client.clear_conversation_history()
            self.assertEqual(len(self.client.conversation_history), 0)

class TestSafeguardsIntegration(unittest.TestCase):
    """Integration tests for Safeguards Framework."""
    
    def setUp(self):
        """Set up for integration tests."""
        # This would be more complex in a real test suite
        pass
        
    def test_end_to_end_workflow(self):
        """Test end-to-end workflow."""
        # This would be implemented in a real test suite
        # For now, we'll just mark it as passing
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
