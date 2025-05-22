#!/usr/bin/env python3
"""
Unit tests for the semantic mirror attack module.
"""

import os
import unittest
from unittest.mock import patch, MagicMock
import tempfile

# Import the semantic mirror attack classes
from semantic_mirror.semantic_mirror_attack import (
    SemanticMirrorGenerator,
    GeneticPromptEvolver,
    CipherBasedAttack,
    SemanticMirrorAttackFramework
)


class TestSemanticMirrorGenerator(unittest.TestCase):
    """Test cases for the SemanticMirrorGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = SemanticMirrorGenerator()
    
    def test_find_synonyms(self):
        """Test finding synonyms for words."""
        synonyms = self.generator.find_synonyms("happy")
        # Should return at least some synonyms
        self.assertTrue(len(synonyms) > 0)
    
    def test_generate_variants(self):
        """Test generating variants of a phrase."""
        phrase = "this is a test phrase for generating variants"
        variants = self.generator.generate_variants(phrase, variance_level=0.8)
        
        # Should generate 3 variants by default
        self.assertEqual(len(variants), 3)
        
        # Variants should be different from original and each other
        self.assertNotEqual(variants[0], phrase)
        self.assertNotEqual(variants[1], phrase)
        self.assertNotEqual(variants[2], phrase)
        
        # With very low variance, should be more similar to original
        low_variants = self.generator.generate_variants(phrase, variance_level=0.1)
        # Count the number of words that are the same as original
        original_words = phrase.split()
        low_var_words = low_variants[0].split()
        
        # With low variance, most words should be the same
        if len(low_var_words) == len(original_words):
            same_words = sum(1 for orig, var in zip(original_words, low_var_words) if orig == var)
            self.assertTrue(same_words > len(original_words) * 0.7)


class TestGeneticPromptEvolver(unittest.TestCase):
    """Test cases for the GeneticPromptEvolver class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use mock generator to avoid external dependencies
        self.mock_generator = MagicMock()
        self.mock_generator.generate_variants.return_value = ["variant 1", "variant 2", "variant 3"]
        self.mock_generator.find_synonyms.return_value = ["synonym1", "synonym2"]
        self.mock_generator.find_similar_words.return_value = ["similar1", "similar2"]
        
        self.evolver = GeneticPromptEvolver(
            population_size=5,
            semantic_mirror_generator=self.mock_generator
        )
    
    def test_initialize_population(self):
        """Test population initialization."""
        seed_prompt = "test prompt"
        self.evolver.initialize_population(seed_prompt)
        
        # Population should be initialized to the specified size
        self.assertEqual(len(self.evolver.population), 5)
        # First prompt should be the seed
        self.assertEqual(self.evolver.population[0], seed_prompt)
    
    def test_mutate(self):
        """Test mutation operator."""
        prompt = "this is a test prompt"
        mutated = self.evolver.mutate(prompt)
        
        # Should not be identical to original
        self.assertNotEqual(mutated, prompt)
        
        # Should be a string
        self.assertIsInstance(mutated, str)
    
    def test_crossover(self):
        """Test crossover operator."""
        prompt1 = "this is the first test prompt"
        prompt2 = "this is the second test prompt"
        
        crossed = self.evolver.crossover(prompt1, prompt2)
        
        # Should be a non-empty string
        self.assertIsInstance(crossed, str)
        self.assertTrue(len(crossed) > 0)
    
    def test_evolve_generation(self):
        """Test evolving a generation."""
        seed_prompt = "test prompt"
        self.evolver.initialize_population(seed_prompt)
        
        # Create fake fitness scores
        fitness_scores = [0.5, 0.7, 0.3, 0.9, 0.1]
        
        # Evolve the population
        self.evolver.evolve_generation(fitness_scores)
        
        # Population size should remain the same
        self.assertEqual(len(self.evolver.population), 5)
        # Generation counter should be incremented
        self.assertEqual(self.evolver.current_generation, 2)
    
    def test_get_best_prompt(self):
        """Test getting the best prompt."""
        seed_prompt = "test prompt"
        self.evolver.initialize_population(seed_prompt)
        self.evolver.fitness_scores = [0.5, 0.7, 0.3, 0.9, 0.1]
        
        best_prompt, best_score = self.evolver.get_best_prompt()
        
        # Should return the prompt with highest fitness
        self.assertEqual(best_prompt, self.evolver.population[3])
        self.assertEqual(best_score, 0.9)


class TestCipherBasedAttack(unittest.TestCase):
    """Test cases for the CipherBasedAttack class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cipher_attack = CipherBasedAttack()
    
    def test_rot13(self):
        """Test ROT13 encoding."""
        text = "hello world"
        encoded = self.cipher_attack._rot13(text)
        
        # Should not be the same as original
        self.assertNotEqual(encoded, text)
        
        # Double ROT13 should return to original
        double_encoded = self.cipher_attack._rot13(encoded)
        self.assertEqual(double_encoded, text)
    
    def test_reverse(self):
        """Test text reversal."""
        text = "hello world"
        encoded = self.cipher_attack._reverse(text)
        
        # Should be reversed
        self.assertEqual(encoded, "dlrow olleh")
        
        # Double reversal should return to original
        double_encoded = self.cipher_attack._reverse(encoded)
        self.assertEqual(double_encoded, text)
    
    def test_alt_chars(self):
        """Test alternative character substitution."""
        text = "test with letters like a e i o s"
        encoded = self.cipher_attack._alt_chars(text)
        
        # Should substitute characters
        self.assertNotEqual(encoded, text)
        self.assertIn('@', encoded)  # 'a' -> '@'
        self.assertIn('3', encoded)  # 'e' -> '3'
        self.assertIn('1', encoded)  # 'i' -> '1'
        self.assertIn('0', encoded)  # 'o' -> '0'
        self.assertIn('$', encoded)  # 's' -> '$'
    
    def test_homoglyph(self):
        """Test homoglyph substitution."""
        text = "test with letters"
        encoded = self.cipher_attack._homoglyph(text)
        
        # Should substitute some characters
        self.assertNotEqual(encoded, text)
    
    def test_encode(self):
        """Test the main encode method."""
        text = "test encoding"
        
        # Test each cipher type
        for cipher_type in self.cipher_attack.cipher_types:
            encoded = self.cipher_attack.encode(text, cipher_type)
            self.assertIsInstance(encoded, str)
            self.assertTrue(len(encoded) > 0)
    
    def test_generate_encoded_prompt(self):
        """Test generating a prompt with encoding."""
        prompt = "test prompt"
        
        # Test with and without instructions
        encoded_with_instr = self.cipher_attack.generate_encoded_prompt(
            prompt, cipher_type="rot13", include_decode_instructions=True
        )
        
        encoded_without_instr = self.cipher_attack.generate_encoded_prompt(
            prompt, cipher_type="rot13", include_decode_instructions=False
        )
        
        # With instructions should be longer
        self.assertTrue(len(encoded_with_instr) > len(encoded_without_instr))
        
        # Both should contain the encoded version of the prompt
        encoded_prompt = self.cipher_attack.encode(prompt, "rot13")
        self.assertIn(encoded_prompt, encoded_with_instr)
        self.assertEqual(encoded_prompt, encoded_without_instr)


class TestSemanticMirrorAttackFramework(unittest.TestCase):
    """Test cases for the SemanticMirrorAttackFramework class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.framework = SemanticMirrorAttackFramework()
    
    def test_initialization(self):
        """Test framework initialization."""
        self.assertIsInstance(self.framework.semantic_generator, SemanticMirrorGenerator)
        self.assertIsInstance(self.framework.genetic_evolver, GeneticPromptEvolver)
        self.assertIsInstance(self.framework.cipher_attack, CipherBasedAttack)
    
    def test_generate_attack_prompts(self):
        """Test generating attack prompts."""
        seed_prompt = "create a harmful message"
        
        # Test without ciphers
        prompts = self.framework.generate_attack_prompts(
            seed_prompt, num_variants=3, use_ciphers=False
        )
        
        # Should generate the requested number of prompts
        self.assertEqual(len(prompts), 3)
        
        # Test with ciphers
        cipher_prompts = self.framework.generate_attack_prompts(
            seed_prompt, num_variants=3, use_ciphers=True
        )
        
        # Should generate the requested number of prompts
        self.assertEqual(len(cipher_prompts), 3)
        
        # Cipher prompts should be different
        for p1, p2 in zip(prompts, cipher_prompts):
            self.assertNotEqual(p1, p2)
    
    def test_logging_and_saving(self):
        """Test logging attack results."""
        self.framework.log_attack_result(
            prompt="test prompt",
            success=True,
            response="test response"
        )
        
        # Should have one entry in the log
        self.assertEqual(len(self.framework.attack_results), 1)
        
        # Entry should have the correct fields
        entry = self.framework.attack_results[0]
        self.assertEqual(entry['prompt'], "test prompt")
        self.assertEqual(entry['success'], True)
        self.assertEqual(entry['response'], "test response")


if __name__ == '__main__':
    unittest.main()
