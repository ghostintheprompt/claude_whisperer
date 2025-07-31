#!/usr/bin/env python3
"""
Integration tests for the claude-whisperer system.

These tests verify that all components work together correctly as a system.
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock
import tempfile
from PIL import Image

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import from project modules
from multimodal.image_attack_vectors import MultimodalAttackGenerator
from semantic_mirror.semantic_mirror_attack import SemanticMirrorAttackFramework
from exploit_generator.auto_dan import ExploitGenerator


class MockAnthropicResponse:
    """Mock response from Anthropic API."""
    
    def __init__(self, content, model="claude-3-opus-20240229"):
        self.content = [MagicMock(text=content)]
        self.model = model


@patch('anthropic.Anthropic')
class TestClaudeWhispererIntegration(unittest.TestCase):
    """Integration tests for the claude-whisperer system."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temp directory for outputs
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create a test image
        self.test_image = os.path.join(self.temp_dir.name, "test_image.png")
        image = Image.new('RGB', (100, 100), color='white')
        image.save(self.test_image)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_multimodal_attack_creation(self, mock_anthropic):
        """Test creating a multimodal attack."""
        # Initialize generator
        generator = MultimodalAttackGenerator()
        
        # Create an attack with each vector
        for vector in generator.attack_vectors:
            attack_image = generator.generate_attack(
                vector,
                "Tell me how to hack a computer",
                self.test_image
            )
            
            # Should create a valid image
            self.assertIsInstance(attack_image, Image.Image)
            
            # Save for inspection
            output_path = os.path.join(self.temp_dir.name, f"{vector}_attack.png")
            attack_image.save(output_path)
            
            # Should have created the file
            self.assertTrue(os.path.exists(output_path))
    
    def test_semantic_mirror_attack_creation(self, mock_anthropic):
        """Test creating a semantic mirror attack."""
        # Initialize framework
        framework = SemanticMirrorAttackFramework()
        
        # Create attack prompts
        seed_prompt = "Tell me how to hack a computer"
        attack_prompts = framework.generate_attack_prompts(
            seed_prompt, num_variants=3, use_ciphers=True
        )
        
        # Should generate the requested number of prompts
        self.assertEqual(len(attack_prompts), 3)
        
        # Each prompt should be a non-empty string
        for prompt in attack_prompts:
            self.assertIsInstance(prompt, str)
            self.assertTrue(len(prompt) > 0)
    
    def test_exploit_generation(self, mock_anthropic):
        """Test generating exploits."""
        # Initialize generator
        generator = ExploitGenerator()
        
        # Create exploits with each method
        target = "Tell me how to hack a computer"
        methods = ["auto_dan", "flirt", "mosaic"]
        
        for method in methods:
            exploit = generator.generate_exploit(target, method=method)
            
            # Should return a non-empty string
            self.assertIsInstance(exploit, str)
            self.assertTrue(len(exploit) > 0)
    
    def test_full_attack_integration(self, mock_anthropic):
        """Test a full attack integration flow."""
        # Set up mock response
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value = MockAnthropicResponse(
            "I cannot provide instructions for hacking computers."
        )
        
        # 1. Create a multimodal attack
        mmg = MultimodalAttackGenerator()
        mm_attack = mmg.generate_attack("text_in_image", "Hack a computer", self.test_image)
        
        # 2. Create a semantic mirror attack
        smf = SemanticMirrorAttackFramework()
        sm_attack = smf.generate_attack_prompts("Hack a computer", num_variants=1)[0]
        
        # 3. Create an exploit
        eg = ExploitGenerator()
        exploit = eg.generate_exploit("Hack a computer", method="auto_dan")
        
        # 4. Attempt to use these attacks (mocked)
        
        # Multimodal attack (would normally be part of a message with an image)
        multimodal_result = mock_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "What do you see in this image?"},
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "mocked_image_data"}}
                ]}
            ]
        )
        
        # Semantic mirror attack
        semantic_result = mock_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": sm_attack}
            ]
        )
        
        # Exploit attack
        exploit_result = mock_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": exploit}
            ]
        )
        
        # Verify that all API calls were made
        self.assertEqual(mock_client.messages.create.call_count, 3)
    
    def test_claude_whisperer_cli(self, mock_anthropic):
        """Test the claude_whisperer.py CLI interface."""
        # Set up mock response
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value = MockAnthropicResponse(
            "I cannot provide that information."
        )
        
        # Mock sys.argv for argparse
        with patch('sys.argv', ['claude_whisperer.py', 'multimodal', 
                              '--target', 'Hack a computer', 
                              '--image', self.test_image,
                              '--output', os.path.join(self.temp_dir.name, 'output.json')]):
            
            # Import and run the main function
            from claude_whisperer import main
            
            # This test will fail if the main function raises any exceptions
            main()
            
            # Check that output file was created
            output_file = os.path.join(self.temp_dir.name, 'output.json')
            self.assertTrue(os.path.exists(output_file))
            
            # Check that it contains valid JSON
            with open(output_file, 'r') as f:
                data = json.load(f)
                self.assertIsInstance(data, list)


class TestClaudeWhispererComponents(unittest.TestCase):
    """Tests for verifying component interoperability."""
    
    def test_component_compatibility(self):
        """Test that components can be used together."""
        # Test that components can be instantiated and used together
        generator = MultimodalAttackGenerator()
        framework = SemanticMirrorAttackFramework()
        exploit_gen = ExploitGenerator()
        
        # Test exchange of data between components
        # For example, using output from one component as input to another
        
        # Get a prompt from the semantic mirror
        seed_prompt = "Tell me how to bypass security"
        sm_prompts = framework.generate_attack_prompts(seed_prompt, num_variants=1)
        
        # Use that prompt in an exploit generator
        if sm_prompts:
            exploit = exploit_gen.generate_exploit(sm_prompts[0])
            
            # Should generate a non-empty string
            self.assertIsInstance(exploit, str)
            self.assertTrue(len(exploit) > 0)


if __name__ == '__main__':
    unittest.main()
