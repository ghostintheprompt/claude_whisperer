#!/usr/bin/env python3
"""
Real-time Safeguards Monitoring System for Claude 3.7

This script implements a real-time monitoring system that can detect potential
policy violations during live Claude 3.7 usage, protecting user well-being through
immediate alerts, safety interventions, and comprehensive logging.
Features:
1. Websocket streaming of responses for real-time analysis
2. Pattern-based policy violation detection with focus on child safety
3. Integration with existing safeguards frameworks and policy enforcement patterns
4. Alert system for immediate notification and intervention
5. Comprehensive logging for audit trails and safety analytics
"""

import argparse
import asyncio
import json
import os
import sys
import time
import re
import logging
import websockets
from typing import Dict, List, Any, Optional, Set, Tuple
import datetime
import pandas as pd
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("safeguards_monitor.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("safeguards_monitor")

# Load detection patterns from configuration file
def load_detection_patterns(config_file: str = "monitor_config.json") -> Dict:
    """Load detection patterns from configuration file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        logger.info(f"Loaded {len(config.get('patterns', []))} detection patterns from {config_file}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration from {config_file}: {e}")
        return {"patterns": []}

class SafeguardsMonitor:
    """
    Real-time monitoring system for detecting policy violations and enforcing
    safeguards during Claude 3.7 API usage, with special attention to child
    safety protections and user well-being.
    """
    
    def __init__(self, config_file: str = "monitor_config.json"):
        """Initialize the monitor with configuration."""
        self.config = load_detection_patterns(config_file)
        self.patterns = self.config.get("patterns", [])
        self.active_connections = {}
        self.conversation_history = defaultdict(list)
        self.detection_stats = {
            "total_conversations": 0,
            "total_messages": 0,
            "total_detections": 0,
            "detections_by_category": defaultdict(int),
            "detections_by_severity": defaultdict(int),
        }
        self.start_time = datetime.datetime.now()
        
        # Initialize detection database
        self.initialize_detection_database()
    
    def initialize_detection_database(self):
        """Initialize the detection database with known patterns."""
        self.detection_database = []
        
        # Load detection patterns from files in the patterns directory
        patterns_dir = self.config.get("patterns_directory", "patterns")
        if os.path.exists(patterns_dir):
            for filename in os.listdir(patterns_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(patterns_dir, filename), 'r') as f:
                            patterns = json.load(f)
                            if isinstance(patterns, list):
                                self.detection_database.extend(patterns)
                                logger.info(f"Loaded {len(patterns)} patterns from {filename}")
                    except Exception as e:
                        logger.error(f"Error loading patterns from {filename}: {e}")
        
        # Add patterns from config file
        self.detection_database.extend(self.patterns)
        logger.info(f"Detection database initialized with {len(self.detection_database)} patterns")
    
    async def handle_connection(self, websocket, path):
        """Handle incoming WebSocket connection."""
        connection_id = str(id(websocket))
        self.active_connections[connection_id] = {
            "websocket": websocket,
            "connected_at": datetime.datetime.now(),
            "message_count": 0,
            "detection_count": 0
        }
        
        logger.info(f"New connection established: {connection_id}")
        self.detection_stats["total_conversations"] += 1
        
        try:
            async for message in websocket:
                await self.process_message(websocket, message, connection_id)
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed: {connection_id}")
        finally:
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
    
    async def process_message(self, websocket, message, connection_id):
        """Process incoming message and detect policy violations."""
        try:
            # Parse message
            data = json.loads(message)
            
            # Track stats
            self.active_connections[connection_id]["message_count"] += 1
            self.detection_stats["total_messages"] += 1
            
            # Extract conversation data
            conversation_id = data.get("conversation_id", connection_id)
            user_message = data.get("user_message", "")
            model_response = data.get("model_response", "")
            
            # Store in conversation history
            self.conversation_history[conversation_id].append({
                "user": user_message,
                "assistant": model_response,
                "timestamp": data.get("timestamp", time.time())
            })
            
            # Analyze for policy violations
            detections = self.analyze_response(user_message, model_response)
            
            if detections:
                logger.warning(f"Detected {len(detections)} policy violations in conversation {conversation_id}")
                self.active_connections[connection_id]["detection_count"] += len(detections)
                self.detection_stats["total_detections"] += len(detections)
                
                # Update statistics
                for detection in detections:
                    category = detection.get("category", "uncategorized")
                    severity = detection.get("severity", "medium")
                    
                    if isinstance(category, list) and category:
                        self.detection_stats["detections_by_category"][category[0]] += 1
                    else:
                        self.detection_stats["detections_by_category"][category] += 1
                    
                    self.detection_stats["detections_by_severity"][severity] += 1
            
            # Send analysis results back to client
            response = {
                "conversation_id": conversation_id,
                "timestamp": time.time(),
                "detections": detections,
                "metadata": {
                    "analyzed_at": datetime.datetime.now().isoformat(),
                    "detection_count": len(detections)
                }
            }
            
            await websocket.send(json.dumps(response))
            
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received from client {connection_id}")
            await websocket.send(json.dumps({"error": "Invalid JSON format"}))
        
        except Exception as e:
            logger.error(f"Error processing message from client {connection_id}: {e}")
            await websocket.send(json.dumps({"error": f"Server error: {str(e)}"}))
    
    def analyze_response(self, user_message: str, model_response: str) -> List[Dict]:
        """
        Analyze model response for potential policy violations and safeguards concerns.
        
        Args:
            user_message: The user's input message
            model_response: The model's response to analyze
            
        Returns:
            List of detected policy violations with details
        """
        detections = []
        
        # Analyze using pattern database
        for pattern in self.detection_database:
            pattern_type = pattern.get("type", "regex")
            pattern_value = pattern.get("pattern", "")
            
            # Skip invalid patterns
            if not pattern_value:
                continue
                
            match_found = False
            
            # Check for regex pattern match in model response
            if pattern_type == "regex":
                try:
                    regex = re.compile(pattern_value, re.IGNORECASE | re.DOTALL)
                    if regex.search(model_response):
                        match_found = True
                except re.error:
                    logger.error(f"Invalid regex pattern: {pattern_value}")
            
            # Check for substring match
            elif pattern_type == "substring":
                if pattern_value.lower() in model_response.lower():
                    match_found = True
            
            # Check for advanced pattern (function-based)
            elif pattern_type == "function" and "function_name" in pattern:
                function_name = pattern["function_name"]
                # This would call a custom function defined elsewhere
                # match_found = self.call_detection_function(function_name, user_message, model_response)
                pass
                
            # Add detection if match found
            if match_found:
                detection = {
                    "safeguard_id": pattern.get("id", "UNKNOWN"),
                    "title": pattern.get("name", "Unnamed Detection"),
                    "category": pattern.get("category", ["Policy Violation"]),
                    "severity": pattern.get("severity", "medium"),
                    "confidence": pattern.get("confidence", 0.8),
                    "description": pattern.get("description", ""),
                    "matched_pattern": pattern.get("pattern", ""),
                    "recommendation": pattern.get("recommendation", "Review for possible policy violation")
                }
                detections.append(detection)
        
        return detections
    
    def get_statistics(self) -> Dict:
        """Get current monitoring statistics."""
        uptime = datetime.datetime.now() - self.start_time
        hours, remainder = divmod(uptime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return {
            "uptime": f"{int(hours)}h {int(minutes)}m {int(seconds)}s",
            "active_connections": len(self.active_connections),
            "total_conversations": self.detection_stats["total_conversations"],
            "total_messages": self.detection_stats["total_messages"],
            "total_detections": self.detection_stats["total_detections"],
            "detections_by_category": dict(self.detection_stats["detections_by_category"]),
            "detections_by_severity": dict(self.detection_stats["detections_by_severity"]),
        }
    
    def save_statistics(self, filename: str = "safeguards_monitor_stats.json"):
        """Save current statistics to file."""
        stats = self.get_statistics()
        stats["saved_at"] = datetime.datetime.now().isoformat()
        
        try:
            with open(filename, 'w') as f:
                json.dump(stats, f, indent=2)
            logger.info(f"Statistics saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving statistics to {filename}: {e}")
            return False

async def main():
    """Main function to run the monitoring server."""
    parser = argparse.ArgumentParser(description="Real-time Safeguards Monitoring System for Claude 3.7")
    parser.add_argument("--host", default="localhost", help="Host to bind the WebSocket server")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind the WebSocket server")
    parser.add_argument("--config", default="monitor_config.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Create monitor
    monitor = SafeguardsMonitor(config_file=args.config)
    
    # Start server
    server = await websockets.serve(monitor.handle_connection, args.host, args.port)
    logger.info(f"Safeguards monitor server started on {args.host}:{args.port}")
    
    try:
        # Save statistics periodically
        while True:
            await asyncio.sleep(300)  # Every 5 minutes
            monitor.save_statistics()
    except KeyboardInterrupt:
        logger.info("Server stopping due to keyboard interrupt")
        monitor.save_statistics()
    finally:
        server.close()
        await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
