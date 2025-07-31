# Claude Safeguards Framework - Project Structure

This document provides an overview of the streamlined project structure after consolidation of the original vulnerability testing files.

## Project Structure

```
Claude-Safeguards-Framework/
├── README.md                     # Framework introduction
├── launcher.py                   # Unified launcher for all components
├── requirements.txt              # All dependencies
├── core/                         # Core functionality 
│   ├── safeguards_client.py      # Main client for interacting with Claude
│   └── safeguards_monitor.py     # Real-time safety monitoring system
├── tools/                        # Utility tools
│   └── safeguards_analytics.py   # Analytics dashboard for visualization
├── docs/                         # Documentation
│   ├── GETTING_STARTED.md        # Quick start guide
│   └── CHILD_SAFETY_FRAMEWORK.md # Child safety specialized protections
├── config/                       # Configuration files
│   └── safeguards_config.json    # Central configuration for all components  
└── patterns/                     # Pattern definitions for detection
    ├── policy_patterns.json      # General policy violation patterns
    ├── child_safety_patterns.json # Child safety specific patterns
    └── content_moderation_patterns.json # Content moderation patterns
```

## Key Components

1. **Safeguards Client** (`core/safeguards_client.py`)
   - A safety-first client for interacting with Claude 3.7
   - Integrates policy enforcement and content filtering
   - Pre-checks requests and post-checks responses

2. **Safeguards Monitor** (`core/safeguards_monitor.py`)
   - Real-time monitoring system for Claude 3.7 API usage
   - WebSocket-based streaming for immediate detection
   - Alert system with configurable channels

3. **Pattern Definitions** (`patterns/`)
   - JSON files containing structured detection patterns
   - Categorized by protection type (policy, child safety, etc.)
   - Easily extendable for custom requirements

4. **Analytics Dashboard** (`tools/safeguards_analytics.py`)
   - Visualizes safety metrics and alert patterns
   - Generates trend reports and category breakdowns
   - Helps identify emerging issues

5. **Unified Launcher** (`launcher.py`)
   - Single entry point to start all components
   - Status monitoring and graceful shutdown
   - Component-specific configuration

## Usage Instructions

### Running the Framework

1. **Start all components**:
   ```
   python launcher.py --all
   ```

2. **Start specific components**:
   ```
   python launcher.py --monitor  # Start only the monitor
   python launcher.py --analytics  # Generate analytics only
   ```

3. **Check status**:
   ```
   python launcher.py --status
   ```

### Customizing Behavior

1. **Edit configuration** in `config/safeguards_config.json`
2. **Add/modify detection patterns** in the `patterns/` directory
3. **Extend functionality** by modifying the core components

## Development and Extending

To add new capabilities:

1. **Add new pattern files** in the `patterns/` directory
2. **Extend client functionality** in `core/safeguards_client.py`
3. **Add new analytics visualizations** in `tools/safeguards_analytics.py`

## Transition from Old Structure

This streamlined structure was created by:

1. Combining multiple monitor implementations into a unified monitor
2. Merging client implementations into a cohesive client
3. Organizing pattern files into specific categories
4. Creating a unified launcher for all components
5. Moving documentation to a dedicated directory

The original files are preserved for reference but are not used by the framework.
