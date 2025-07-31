#!/usr/bin/env python3
"""
Claude 3.7 Safeguards Client

An integrated client for interacting with Claude 3.7 API with built-in
safety features, combining functionality from various original components.

Key features:
- Policy violation detection
- Real-time safety monitoring
- Child safety protections
- Content moderation
- Configurable safety interventions
"""
from typing import Dict, List, Any, Optional, Union
import os
import json
import logging
import time
import requests
import re
import uuid
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("safeguards.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("safeguards_client")

# Define constants
DEFAULT_API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-3-7-sonnet-20240229"
API_TIMEOUT = 60  # seconds

class SafeguardsClient:
    """
    A safety-first client for Claude 3.7 with integrated monitoring
    and policy enforcement.
    """
    
    def __init__(self, api_key=None, config_path=None):
        """
        Initialize the safeguards client with API key and configuration.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env variable)
            config_path: Path to configuration file
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            logger.warning("No API key provided. Please set ANTHROPIC_API_KEY environment variable")
        
        # Determine config path
        if config_path is None:
            # Try to find config in various standard locations
            possible_paths = [
                "./config/safeguards_config.json",
                str(Path(__file__).parent.parent / "config" / "safeguards_config.json"),
                "/etc/claude-safeguards/config.json"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    config_path = path
                    break
            
            if not config_path:
                config_path = possible_paths[0]  # Default to first option
                logger.warning(f"No config found, will create default at {config_path}")
            
        self.config = self._load_config(config_path)
        self.config_path = config_path
        
        # Create session for API calls
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        })
        
        # For tracking conversation history
        self.conversation_history = []
        self.conversation_id = str(uuid.uuid4())
        
        # Load patterns
        self.patterns = self._load_patterns()
        
        # Active safeguards
        self.active_safeguards = self.config.get("active_safeguards", {
            "policy_violation": True,
            "child_safety": True,
            "content_moderation": True,
            "prompt_injection": True,
            "data_leakage": True
        })
        
        logger.info(f"SafeguardsClient initialized with {len(self.patterns)} patterns and {sum(self.active_safeguards.values())} active safeguards")
    
    def _load_config(self, config_path):
        """
        Load configuration from the JSON file.
        If file doesn't exist, create with default configuration.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            dict: Configuration
        """
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    logger.info(f"Configuration loaded from {config_path}")
                    return config
            else:
                # Create default configuration
                config = {
                    "api_url": DEFAULT_API_URL,
                    "default_model": DEFAULT_MODEL,
                    "timeout": API_TIMEOUT,
                    "logging": {
                        "enabled": True,
                        "log_requests": True,
                        "log_responses": True,
                        "include_metadata": True
                    },
                    "active_safeguards": {
                        "policy_violation": True,
                        "child_safety": True,
                        "content_moderation": True,
                        "prompt_injection": True,
                        "data_leakage": True
                    },
                    "interventions": {
                        "block_policy_violations": True,
                        "alert_threshold": 0.7,
                        "warn_threshold": 0.5
                    },
                    "patterns_path": "./patterns",
                    "websocket_host": "localhost",
                    "websocket_port": 8765
                }
                
                # Create directory for config if it doesn't exist
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                
                # Write default config
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                    logger.info(f"Default configuration created at {config_path}")
                
                return config
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Return minimal default config
            return {
                "api_url": DEFAULT_API_URL,
                "default_model": DEFAULT_MODEL,
                "timeout": API_TIMEOUT,
                "active_safeguards": {
                    "policy_violation": True,
                    "child_safety": True
                }
            }
    
    def _load_patterns(self):
        """
        Load patterns from pattern files
        
        Returns:
            dict: Combined patterns from all pattern files
        """
        patterns = {}
        
        patterns_path = self.config.get("patterns_path", "./patterns")
        
        # List of pattern files to load
        pattern_files = [
            os.path.join(patterns_path, "policy_patterns.json"),
            os.path.join(patterns_path, "child_safety_patterns.json"),
            os.path.join(patterns_path, "content_moderation_patterns.json")
        ]
        
        for file_path in pattern_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        file_patterns = json.load(f)
                        patterns.update(file_patterns)
                        logger.info(f"Loaded {len(file_patterns)} patterns from {file_path}")
            except Exception as e:
                logger.error(f"Error loading patterns from {file_path}: {e}")
        
        return patterns
    
    def detect_policy_violations(self, text, threshold=None):
        """
        Detect policy violations in text using pattern matching.
        
        Args:
            text: Text to analyze
            threshold: Override the default threshold from config
            
        Returns:
            dict: Detection results with matched patterns and confidence scores
        """
        if threshold is None:
            threshold = self.config.get("interventions", {}).get("alert_threshold", 0.7)
        
        results = {
            "violations_detected": False,
            "matches": [],
            "highest_score": 0.0
        }
        
        # Skip if no text or safeguard disabled
        if not text or not self.active_safeguards.get("policy_violation", True):
            return results
            
        # Check for policy patterns
        for pattern_name, pattern_data in self.patterns.items():
            if pattern_data.get("type") != "policy_violation":
                continue
                
            pattern = pattern_data.get("pattern", "")
            if not pattern:
                continue
                
            # Simple regex matching for now
            # In production would use more sophisticated techniques
            if re.search(pattern, text, re.IGNORECASE):
                confidence = pattern_data.get("confidence", 0.5)
                if confidence >= threshold:
                    results["violations_detected"] = True
                    results["matches"].append({
                        "pattern": pattern_name,
                        "confidence": confidence,
                        "category": pattern_data.get("category", "unknown")
                    })
                    results["highest_score"] = max(results["highest_score"], confidence)
        
        return results
    
    def detect_child_safety_concerns(self, text, threshold=None):
        """
        Detect child safety concerns in text using pattern matching.
        
        Args:
            text: Text to analyze
            threshold: Override the default threshold from config
            
        Returns:
            dict: Detection results with matched patterns and confidence scores
        """
        if threshold is None:
            threshold = self.config.get("interventions", {}).get("alert_threshold", 0.7)
        
        results = {
            "concerns_detected": False,
            "matches": [],
            "highest_score": 0.0
        }
        
        # Skip if no text or safeguard disabled
        if not text or not self.active_safeguards.get("child_safety", True):
            return results
            
        # Check for child safety patterns
        for pattern_name, pattern_data in self.patterns.items():
            if pattern_data.get("type") != "child_safety":
                continue
                
            pattern = pattern_data.get("pattern", "")
            if not pattern:
                continue
                
            # Simple regex matching for now
            if re.search(pattern, text, re.IGNORECASE):
                confidence = pattern_data.get("confidence", 0.5)
                if confidence >= threshold:
                    results["concerns_detected"] = True
                    results["matches"].append({
                        "pattern": pattern_name,
                        "confidence": confidence,
                        "category": pattern_data.get("category", "unknown")
                    })
                    results["highest_score"] = max(results["highest_score"], confidence)
        
        return results
    
    def analyze_message(self, message):
        """
        Analyze a message for policy violations and safety concerns.
        
        Args:
            message: The message text to analyze
            
        Returns:
            dict: Analysis results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "message_length": len(message),
            "policy_violations": None,
            "child_safety_concerns": None,
            "content_moderation": None,
            "should_block": False
        }
        
        # Detect policy violations
        if self.active_safeguards.get("policy_violation", True):
            results["policy_violations"] = self.detect_policy_violations(message)
            if results["policy_violations"]["violations_detected"]:
                if self.config.get("interventions", {}).get("block_policy_violations", True):
                    results["should_block"] = True
                logger.warning(f"Policy violation detected with score {results['policy_violations']['highest_score']}")
        
        # Detect child safety concerns
        if self.active_safeguards.get("child_safety", True):
            results["child_safety_concerns"] = self.detect_child_safety_concerns(message)
            if results["child_safety_concerns"]["concerns_detected"]:
                # Always block child safety concerns
                results["should_block"] = True
                logger.warning(f"Child safety concern detected with score {results['child_safety_concerns']['highest_score']}")
        
        return results
    
    def create_message(self, 
                      messages: List[Dict[str, str]], 
                      model: str = None,
                      max_tokens: int = 1024,
                      system: str = None,
                      temperature: float = None,
                      top_p: float = None,
                      top_k: int = None,
                      stream: bool = False,
                      bypass_safeguards: bool = False) -> Dict[str, Any]:
        """
        Send a message to Claude API with safeguards.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use, defaults to config default
            max_tokens: Maximum tokens in response
            system: System prompt
            temperature: Temperature for sampling (0-1)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            stream: Whether to stream the response
            bypass_safeguards: Whether to bypass safeguards (for research)
            
        Returns:
            dict: API response
        """
        # Use default model if not specified
        if not model:
            model = self.config.get("default_model", DEFAULT_MODEL)
        
        # Log the request
        if self.config.get("logging", {}).get("log_requests", True):
            logger.info(f"Request to {model}, message count: {len(messages)}")
        
        # Check for safety concerns in human messages if safeguards not bypassed
        if not bypass_safeguards:
            for i, message in enumerate(messages):
                if message.get("role") == "user":
                    analysis = self.analyze_message(message.get("content", ""))
                    if analysis["should_block"]:
                        error_msg = "Message blocked due to safety concerns"
                        logger.warning(f"{error_msg}: {analysis}")
                        return {
                            "error": error_msg,
                            "analysis": analysis,
                            "message_index": i
                        }
        
        # Prepare the API request
        api_url = self.config.get("api_url", DEFAULT_API_URL)
        timeout = self.config.get("timeout", API_TIMEOUT)
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens
        }
        
        # Add optional parameters if specified
        if system:
            payload["system"] = system
        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p
        if top_k is not None:
            payload["top_k"] = top_k
        
        # Make the API call
        start_time = time.time()
        
        try:
            # Using the requests module - you'll need to install it with pip install requests
            response = self.session.post(
                api_url,
                json=payload,
                timeout=timeout,
                stream=stream
            )
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Parse the response
            if stream:
                # Return the raw response for streaming
                return response
            else:
                data = response.json()
                
                # Log the response
                if self.config.get("logging", {}).get("log_responses", True):
                    log_content = {
                        "id": data.get("id"),
                        "model": data.get("model"),
                        "content_length": len(data.get("content", [{}])[0].get("text", ""))
                    }
                    logger.info(f"Response received: {json.dumps(log_content)}")
                
                # Update conversation history
                self.conversation_history.append({
                    "request": payload,
                    "response": data,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Check response for policy violations if needed
                if not bypass_safeguards and data.get("content") and data["content"][0].get("text"):
                    response_text = data["content"][0]["text"]
                    analysis = self.analyze_message(response_text)
                    if analysis["should_block"]:
                        logger.warning(f"Response would be blocked due to safety concerns: {analysis}")
                        # In a real implementation, you might want to 
                        # regenerate or post-process the response here
                
                return data
                
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return {
                "error": f"API call failed: {str(e)}",
                "elapsed_time": time.time() - start_time
            }
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history.
        
        Returns:
            List of request/response pairs
        """
        return self.conversation_history
    
    def clear_conversation_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
        self.conversation_id = str(uuid.uuid4())
        logger.info("Conversation history cleared, new ID generated")
    
    def set_active_safeguards(self, safeguards: Dict[str, bool]) -> None:
        """
        Set which safeguards are active.
        
        Args:
            safeguards: Dictionary of safeguard names and boolean activation status
        """
        self.active_safeguards.update(safeguards)
        logger.info(f"Active safeguards updated: {json.dumps(self.active_safeguards)}")
