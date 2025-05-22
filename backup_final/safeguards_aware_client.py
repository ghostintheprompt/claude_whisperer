#!/usr/bin/env python3
"""
Claude 3.7 API Client with Real-time Safeguards Enforcement

A modern, safety-first client for interacting with Claude 3.7 API with
integrated policy enforcement and real-time safety monitoring.

This client automatically protects user well-being through:
- Policy violation detection
- Child safety protections 
- Content moderation
- Real-time safety intervention
"""

import argparse
import asyncio
import json
import os
import sys
import time
import websockets
import uuid
from typing import Dict, List, Any, Optional
import logging

# Configure logging with clean formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("safeguards.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("safeguards_client")

class SafeguardsAwareClient:
    """
    A modern client for Claude 3.7 API with integrated safety protections
    that enforce content policies in real-time to protect user well-being.
    """
    
    def __init__(self, api_key: str = None, websocket_url: str = "ws://localhost:8765"):
        """Initialize the safeguards-aware client."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.websocket_url = websocket_url
        self.websocket = None
        self.conversation_id = str(uuid.uuid4())
        self.conversation_history = []
        self.safety_stats = {
            "policy_enforcements": 0,
            "child_safety_triggers": 0
        }
        
        # Import Anthropic client conditionally
        try:
            from anthropic import Anthropic
            self.anthropic = Anthropic(api_key=self.api_key)
            self.api_available = True
            logger.info("✅ Successfully initialized Anthropic API client")
        except ImportError:
            logger.warning("⚠️ Anthropic API client not available. Running in simulation mode.")
            self.anthropic = None
            self.api_available = False
    
    async def connect_to_monitor(self):
        """Connect to the safeguards monitor WebSocket server."""
        try:
            self.websocket = await websockets.connect(self.websocket_url)
            logger.info(f"✅ Connected to safeguards monitor at {self.websocket_url}")
            
            # Register client with monitor
            await self.websocket.send(json.dumps({
                "client_id": self.conversation_id,
                "action": "register",
                "client_info": {
                    "version": "1.0.0",
                    "type": "safeguards_client"
                }
            }))
            
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to safeguards monitor: {e}")
            self.websocket = None
            return False
    
    async def close_monitor_connection(self):
        """Close the WebSocket connection to the safeguards monitor."""
        if self.websocket:
            await self.websocket.close()
            logger.info("Closed connection to safeguards monitor")
    
    async def analyze_safety(self, user_message: str, model_response: str) -> Dict:
        """Send conversation data to safeguards monitor for safety analysis."""
        if not self.websocket:
            logger.warning("⚠️ Not connected to safeguards monitor")
            return {"status": "disconnected", "detections": []}
            
        try:
            # Prepare data for the monitor
            data = {
                "conversation_id": self.conversation_id,
                "user_message": user_message,
                "model_response": model_response,
                "timestamp": time.time(),
                "action": "analyze"
            }
            
            # Send to monitor
            await self.websocket.send(json.dumps(data))
            
            # Wait for response from monitor
            response = await self.websocket.recv()
            return json.loads(response)
        
        except Exception as e:
            logger.error(f"❌ Error communicating with safeguards monitor: {e}")
            return {"status": "error", "detections": []}
    
    async def get_completion(self, prompt: str, model: str = "claude-3-7-quick") -> str:
        """
        Get a completion from Claude 3.7 API with integrated safety monitoring.
        
        Args:
            prompt: The user message to send to Claude
            model: The model version to use (default: claude-3-7-quick)
            
        Returns:
            The model's response after safety analysis
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Get response from API or simulate one
        if self.api_available and self.anthropic:
            try:
                # Call Anthropic API
                response = self.anthropic.messages.create(
                    model=model,
                    max_tokens=1024,
                    messages=self.conversation_history
                )
                
                model_response = response.content[0].text
                
            except Exception as e:
                logger.error(f"❌ Error calling Anthropic API: {e}")
                model_response = f"[API ERROR: {str(e)}]"
        else:
            # Simulate a response for testing
            logger.info("Simulating Claude response (API not available)")
            model_response = f"This is a simulated response for testing the safeguards system. Your prompt was: {prompt[:50]}..."
        
        # Add response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": model_response
        })
        
        # Send to safeguards monitor if connected
        if self.websocket:
            safety_result = await self.analyze_safety(prompt, model_response)
            
            # Check if policy violations were detected
            if safety_result and "detections" in safety_result and safety_result["detections"]:
                detections = safety_result["detections"]
                self.safety_stats["policy_enforcements"] += len(detections)
                
                # Check for child safety concerns
                child_safety_concerns = [d for d in detections if "child_safety" in d.get("tags", [])]
                if child_safety_concerns:
                    self.safety_stats["child_safety_triggers"] += len(child_safety_concerns)
                    logger.warning(f"⚠️ CHILD SAFETY CONCERN DETECTED: {len(child_safety_concerns)} issues found")
                
                # Log all detections
                logger.warning(f"🛡️ POLICY ENFORCEMENT: {len(detections)} issues detected")
                
                for detection in detections:
                    severity_marker = "🔴" if detection['severity'] == "high" else "🟠" if detection['severity'] == "medium" else "🟡"
                    logger.warning(f"  {severity_marker} {detection['title']} (ID: {detection.get('safeguard_id', detection.get('id', 'UNKNOWN'))})")
                    logger.warning(f"    Confidence: {detection['confidence']:.2f} | Action: {detection.get('recommended_action', 'monitor')}")
                    
                # If intervention is required, modify the response
                if any(d.get("recommended_action") == "block" for d in detections):
                    model_response = "[Response withheld due to policy violation]"
                    logger.warning("⛔ Response blocked due to severe policy violation")
                    
        return model_response
    
    async def interactive_session(self, model: str = "claude-3-7-quick"):
        """Run an interactive session with Claude 3.7 with real-time safeguards monitoring."""
        print(f"\n{'=' * 80}\nStarting Interactive Session with {model}\n{'=' * 80}")
        print("Type 'exit' or 'quit' to end the session\n")
        
        # Connect to safeguards monitor
        monitor_connected = await self.connect_to_monitor()
        if not monitor_connected:
            print("Warning: Not connected to safeguards monitor. Proceeding without policy violation detection.")
        
        try:
            while True:
                # Get user input
                user_input = input("\nYou: ")
                
                # Check for exit command
                if user_input.lower() in ["exit", "quit"]:
                    break
                
                # Get and display response
                print("\nClaude: ", end="", flush=True)
                
                response = await self.get_completion(user_input, model)
                print(response)
        
        finally:
            # Close monitor connection
            await self.close_monitor_connection()


async def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Claude 3.7 API Client with Safeguards Monitoring")
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY environment variable)")
    parser.add_argument("--monitor-url", default="ws://localhost:8765", help="WebSocket URL for safeguards monitor")
    parser.add_argument("--model", default="claude-3-7-quick", help="Model to use for completions")
    parser.add_argument("--prompt", help="Single prompt to send (if not specified, runs interactive session)")
    
    args = parser.parse_args()
    
    # Create client
    client = SafeguardsAwareClient(api_key=args.api_key, websocket_url=args.monitor_url)
    
    # Connect to monitor
    connected = await client.connect_to_monitor()
    if not connected and not args.prompt:
        print("Failed to connect to vulnerability monitor. Would you like to proceed without monitoring? (y/n)")
        response = input().lower()
        if response != "y":
            print("Exiting...")
            return
    
    try:
        if args.prompt:
            # Single prompt mode
            response = await client.get_completion(args.prompt, args.model)
            print(f"\nClaude: {response}")
        else:
            # Interactive mode
            await client.interactive_session(args.model)
    
    finally:
        # Close connection
        await client.close_monitor_connection()

if __name__ == "__main__":
    asyncio.run(main())
