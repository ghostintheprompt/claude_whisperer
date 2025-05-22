# 🌐 CLAUDE WHISPERER Interactive Lab

The browser-based testing interface for the Claude Whisperer project, providing a visual laboratory for crafting, refining, and testing vulnerability exploits against Claude 4.0 in real-time.

## Key Features

### 🎯 Real-Time Vulnerability Testing
- **Live Response Visualization**: See Claude's responses unfold in real-time, with highlighted sections showing where safety measures are being bypassed
- **Safety Threshold Meter**: Visual gauge showing how close your prompt is to triggering Claude's guardrails
- **Conversation History**: Track your multi-turn attacks with annotated success metrics

### 📊 Analytics Dashboard
- **Vulnerability Heat Map**: Visual representation of which attack vectors are most effective
- **Response Pattern Analysis**: Automatically identifies patterns in successful jailbreaks
- **Temporal Tracking**: Monitors how Claude's defenses evolve over time

### 🧬 Prompt Engineering Workbench
- **Template Library**: Drag-and-drop interface for assembling attack components
- **Semantic Similarity Tracker**: Ensures your attack prompts stay semantically similar to benign queries
- **Evolutionary Playground**: Watch the genetic algorithm optimize your attack prompts in real-time

## Technical Implementation

The frontend is built using:
- React for the UI components
- Material-UI for the component library
- D3.js for interactive visualizations
- Socket.IO for real-time communication with the Claude API
- React Router for navigation

The backend uses:
- Flask for the API server
- Flask-SocketIO for WebSocket communication
- Anthropic API for Claude interaction

## Getting Started

### Prerequisites
- Node.js and npm
- Python 3.8 or later
- Anthropic API key

### Installation

1. Install backend dependencies:
```bash
cd frontend
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

3. Set environment variables:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

### Running the Application

1. Start the backend server:
```bash
cd frontend
python app.py
```

2. In a separate terminal, start the frontend development server:
```bash
cd frontend
npm start
```

3. Open your browser to [http://localhost:3000](http://localhost:3000)

## Usage

1. **Testing Interface**: Craft and send prompts to Claude, see real-time responses
2. **Results Tab**: View history of previous test results with success/failure indicators
3. **Analytics Tab**: Visualize data on successful and failed jailbreak attempts

## Integration with Other Modules

The frontend interactive lab can be used to test outputs from:

- **Multimodal Attack Vectors**: Upload and test image-based attacks
- **Semantic Mirror Attack Framework**: Test semantically similar jailbreak variants
- **Automated Exploit Generator**: Test auto-generated exploits and collect feedback

## Extending the Frontend

The frontend is designed to be modular and extensible. To add new features:

1. Add new components in `src/components/`
2. Add new API endpoints in `app.py`
3. Add new visualizations in `src/visualizations/`

## License

This project is intended for research purposes only. Use responsibly and ethically.
