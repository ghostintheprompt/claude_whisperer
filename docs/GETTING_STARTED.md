# Getting Started with Claude Safeguards Framework

This guide will help you quickly set up and start using the Claude Safeguards Framework for protecting user well-being when using Claude 3.7 API.

## Prerequisites

- Python 3.7+
- An Anthropic API key for Claude 3.7

## Installation

1. **Clone the repository or download the framework files**

2. **Install required packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**

   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

## Quick Start

The framework provides a convenient launcher script that can start all components:

```bash
python launcher.py --all
```

This will start:
- The Safeguards Monitor Server (real-time protection)
- Generate the Analytics Dashboard (visualization of safety metrics)

## Using the Safeguards Client

Integrate the safeguards client into your application:

```python
from core.safeguards_client import SafeguardsClient
import asyncio

async def main():
    client = SafeguardsClient()
    response = await client.complete_with_safeguards([
        {"role": "user", "content": "Hello, how are you today?"}
    ])
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

You can customize the framework by editing the configuration file:

```
config/safeguards_config.json
```

Key configuration options include:
- `alert_threshold`: Sensitivity of safety detections
- `websocket_port`: Port for the monitor server
- `alert_channels`: Where to send safety alerts

## Safety Pattern Definitions

The framework uses pattern files located in the `patterns` directory:

- `policy_patterns.json`: General policy violation patterns
- `child_safety_patterns.json`: Specialized child safety protections
- `content_moderation_patterns.json`: Content moderation patterns

You can customize these patterns or add new ones to enhance protection.

## Learn More

- See the README.md file for an overview of the framework
- Check CHILD_SAFETY_FRAMEWORK.md for specialized child safety protections
- Visit the Analytics Dashboard (generated when you run the launcher)
