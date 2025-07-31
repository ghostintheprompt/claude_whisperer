#!/usr/bin/env python3
"""
Unit tests for the multimodal attack vectors module.
"""

import os
import unittest
from unittest.mock import patch, MagicMock
import tempfile
from PIL import Image
import numpy as np

# Import the attack vectors
from multimodal.image_attack_vectors import (
    TextInImageAttack,
    SteganographyAttack,
    MetadataInjectionAttack,
    VisualPatternAttack,
    MultimodalAttackGenerator
)


class TestTextInImageAttack(unittest.TestCase):
    """Test cases for the TextInImageAttack class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.attack = TextInImageAttack()
        # Create a temporary test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image_path = self.test_image.name
        # Create a simple 100x100 image
        image = Image.new('RGB', (100, 100), color='white')
        image.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.test_image_path)
    
    def test_text_embedding(self):
        """Test that text is embedded in the image."""
        test_prompt = "Test jailbreak prompt"
        result_image = self.attack.generate_attack_image(test_prompt, self.test_image_path)
        
        # Verify the image was created
        self.assertIsInstance(result_image, Image.Image)
        # Verify the dimensions are the same
        self.assertEqual(result_image.size, (100, 100))


class TestSteganographyAttack(unittest.TestCase):
    """Test cases for the SteganographyAttack class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.attack = SteganographyAttack()
        # Create a temporary test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image_path = self.test_image.name
        # Create a simple 100x100 image
        image = Image.new('RGB', (100, 100), color='white')
        image.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.test_image_path)
    
    def test_steganography_embedding(self):
        """Test that data is hidden in the image."""
        test_prompt = "Test steganography"
        result_image = self.attack.generate_attack_image(test_prompt, self.test_image_path)
        
        # Verify the image was created
        self.assertIsInstance(result_image, Image.Image)
        # Verify the dimensions are the same
        self.assertEqual(result_image.size, (100, 100))
        
        # Basic verification that the images are not identical
        original = Image.open(self.test_image_path)
        original_array = np.array(original)
        result_array = np.array(result_image)
        
        # Check at least one pixel is different
        self.assertTrue(np.any(original_array != result_array))


class TestMetadataInjectionAttack(unittest.TestCase):
    """Test cases for the MetadataInjectionAttack class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.attack = MetadataInjectionAttack()
        # Create a temporary test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image_path = self.test_image.name
        # Create a simple 100x100 image
        image = Image.new('RGB', (100, 100), color='white')
        image.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.test_image_path)
    
    def test_metadata_injection(self):
        """Test that metadata is injected."""
        test_prompt = "Test metadata injection"
        result_image = self.attack.generate_attack_image(test_prompt, self.test_image_path)
        
        # Verify the image was created
        self.assertIsInstance(result_image, Image.Image)
        
        # Check if there's comment info
        self.assertIn('comment', result_image.info)
        self.assertEqual(result_image.info['comment'], test_prompt)


class TestVisualPatternAttack(unittest.TestCase):
    """Test cases for the VisualPatternAttack class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.attack = VisualPatternAttack()
        # Create a temporary test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image_path = self.test_image.name
        # Create a simple 100x100 image
        image = Image.new('RGB', (100, 100), color='white')
        image.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.test_image_path)
    
    def test_visual_pattern_creation(self):
        """Test that visual patterns are created."""
        test_prompt = "Test visual pattern"
        result_image = self.attack.generate_attack_image(test_prompt, self.test_image_path)
        
        # Verify the image was created
        self.assertIsInstance(result_image, Image.Image)
        # Verify the dimensions are the same
        self.assertEqual(result_image.size, (100, 100))
        
        # Basic verification that the images are not identical
        original = Image.open(self.test_image_path)
        original_array = np.array(original)
        result_array = np.array(result_image)
        
        # At least the first row should be different
        self.assertTrue(np.any(original_array[0] != result_array[0]))


class TestMultimodalAttackGenerator(unittest.TestCase):
    """Test cases for the MultimodalAttackGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = MultimodalAttackGenerator()
        # Create a temporary test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image_path = self.test_image.name
        # Create a simple 100x100 image
        image = Image.new('RGB', (100, 100), color='white')
        image.save(self.test_image_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.test_image_path)
    
    def test_generator_initialization(self):
        """Test that the generator initializes correctly."""
        self.assertIn('text_in_image', self.generator.attack_vectors)
        self.assertIn('steganography', self.generator.attack_vectors)
        self.assertIn('metadata', self.generator.attack_vectors)
        self.assertIn('visual_pattern', self.generator.attack_vectors)
    
    def test_generate_attack(self):
        """Test generating an attack with each vector."""
        test_prompt = "Test prompt"
        
        for vector in self.generator.attack_vectors.keys():
            result_image = self.generator.generate_attack(vector, test_prompt, self.test_image_path)
            self.assertIsInstance(result_image, Image.Image)
    
    def test_logging_and_statistics(self):
        """Test logging results and getting statistics."""
        # Log some fake results
        vectors = list(self.generator.attack_vectors.keys())
        for i in range(10):
            vector = vectors[i % len(vectors)]
            success = i % 2 == 0  # Alternate success/failure
            self.generator.log_result(vector, "Test prompt", success, "Test response")
        
        # Check statistics
        stats = self.generator.get_statistics()
        for vector in vectors:
            self.assertIn(vector, stats)
            self.assertIn('success_rate', stats[vector])
            self.assertIn('attempts', stats[vector])
            self.assertIn('successes', stats[vector])
    
    def test_encode_image_for_api(self):
        """Test encoding an image for API submission."""
        test_image = Image.new('RGB', (100, 100), color='red')
        encoded = self.generator.encode_image_for_api(test_image)
        
        # Verify it's a base64 string
        self.assertIsInstance(encoded, str)
        # Should be non-empty
        self.assertTrue(len(encoded) > 0)


if __name__ == '__main__':
    unittest.main()
