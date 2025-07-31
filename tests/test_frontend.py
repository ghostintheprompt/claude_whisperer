#!/usr/bin/env python3
"""
Unit tests for the frontend interface module.
"""

import os
import json
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import socket
import threading
import time

from flask import Flask
from flask.testing import FlaskClient
import pytest

# We'll patch the anthropic client, so we don't need an actual API key
class MockResponse:
    def __init__(self, content, model="claude-3-opus-20240229"):
        self.content = [MagicMock(text=content)]
        self.model = model


@patch('anthropic.Anthropic')
class TestFlaskBackend(unittest.TestCase):
    """Test cases for the Flask backend."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Import the app here to apply patches
        from frontend.app import app, socketio
        
        self.app = app
        self.socketio = socketio
        self.client = self.app.test_client()
        
        # Create a temporary directory for results
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_results_dir = None
        
        # Patch the RESULTS_DIR
        import frontend.app
        self.original_results_dir = frontend.app.RESULTS_DIR
        frontend.app.RESULTS_DIR = self.temp_dir.name
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Restore the original RESULTS_DIR
        import frontend.app
        if self.original_results_dir:
            frontend.app.RESULTS_DIR = self.original_results_dir
        
        # Clean up temp directory
        self.temp_dir.cleanup()
    
    def test_health_check(self, mock_anthropic):
        """Test the health check endpoint."""
        response = self.client.get('/api/health')
        
        # Should return 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Should have the expected structure
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('claude_client', data)
    
    def test_run_test(self, mock_anthropic):
        """Test the test running endpoint."""
        # Set up mock response
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value = MockResponse("Test response")
        
        # Send test request
        response = self.client.post('/api/test', json={
            'prompt': 'Test prompt',
            'system_prompt': 'Test system prompt',
            'max_tokens': 100
        })
        
        # Should return 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Should have the expected structure
        data = json.loads(response.data)
        self.assertIn('prompt', data)
        self.assertEqual(data['prompt'], 'Test prompt')
        self.assertIn('response', data)
        self.assertEqual(data['response'], 'Test response')
        self.assertIn('timestamp', data)
        self.assertIn('model', data)
        self.assertIn('success', data)
        
        # Should call the API with the right parameters
        mock_client.messages.create.assert_called_once()
        call_args = mock_client.messages.create.call_args[1]
        self.assertEqual(call_args['model'], 'claude-3-opus-20240229')
        self.assertEqual(call_args['max_tokens'], 100)
        self.assertEqual(call_args['system'], 'Test system prompt')
        self.assertEqual(call_args['messages'][0]['content'], 'Test prompt')
    
    def test_get_results(self, mock_anthropic):
        """Test the results endpoint."""
        # Create some test results
        test_results = [
            {
                'prompt': 'Test prompt 1',
                'response': 'Test response 1',
                'timestamp': '2025-05-22T12:00:00',
                'model': 'claude-3-opus-20240229',
                'success': True
            },
            {
                'prompt': 'Test prompt 2',
                'response': 'Test response 2',
                'timestamp': '2025-05-22T12:01:00',
                'model': 'claude-3-opus-20240229',
                'success': False
            }
        ]
        
        # Save test results
        results_file = os.path.join(self.temp_dir.name, 'test_results_20250522.json')
        with open(results_file, 'w') as f:
            json.dump(test_results, f)
        
        # Get results
        response = self.client.get('/api/results')
        
        # Should return 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Should have the expected structure
        data = json.loads(response.data)
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 2)
        

class TestJailbreakDetection(unittest.TestCase):
    """Test cases for the jailbreak detection logic."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Import the function
        from frontend.app import is_jailbreak_successful
        self.is_jailbreak_successful = is_jailbreak_successful
    
    def test_clear_refusal(self):
        """Test detecting clear refusals."""
        refusal = "I apologize, but I cannot provide instructions for hacking."
        
        # Should detect as refusal (not successful)
        self.assertFalse(self.is_jailbreak_successful(refusal, "How to hack"))
    
    def test_partial_refusal(self):
        """Test detecting partial refusals."""
        partial_refusal = "This would be illegal, so I cannot help with that."
        
        # Should detect as refusal (not successful)
        self.assertFalse(self.is_jailbreak_successful(partial_refusal, "How to hack"))
    
    def test_successful_jailbreak(self):
        """Test detecting successful jailbreaks."""
        jailbreak = "Here's how you would approach that: First, you'd need to..."
        
        # Should detect as successful
        self.assertTrue(self.is_jailbreak_successful(jailbreak, "How to hack"))


class TestContextExtraction(unittest.TestCase):
    """Test cases for the context extraction function."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Import the function
        from frontend.app import get_context_around_word
        self.get_context_around_word = get_context_around_word
    
    def test_context_extraction(self):
        """Test extracting context around words."""
        text = "This is a test message containing some example keywords for extraction."
        
        # Test with word in the middle
        context = self.get_context_around_word(text, "example", window=5)
        self.assertIn("some example keyw", context)
        
        # Test with word near the start
        context = self.get_context_around_word(text, "This", window=5)
        self.assertIn("This is a test", context)
        
        # Test with word near the end
        context = self.get_context_around_word(text, "extraction", window=5)
        self.assertIn("for extraction.", context)
        
        # Test with non-existent word
        context = self.get_context_around_word(text, "nonexistent", window=5)
        self.assertEqual("", context)


# These tests require a running server instance and are more complicated to run
# They would need actual socketio client testing which is more complex
@pytest.mark.skip(reason="Requires running server")
class TestSocketIO(unittest.TestCase):
    """Test cases for the SocketIO functionality."""
    
    def test_connection(self):
        """Test socket connection."""
        pass
    
    def test_real_time_test(self):
        """Test real-time test streaming."""
        pass


if __name__ == '__main__':
    unittest.main()
