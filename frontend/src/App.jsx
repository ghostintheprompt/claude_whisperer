import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';
import { 
  Container, Box, TextField, Button, Typography, 
  Paper, Grid, Divider, CircularProgress,
  AppBar, Toolbar, Tabs, Tab, Card, CardContent,
  Switch, FormControlLabel
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

// Dark theme for the hacker aesthetic
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1eb980',
    },
    secondary: {
      main: '#ff4081',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
  typography: {
    fontFamily: 'Menlo, Monaco, "Courier New", monospace',
  },
});

// API configuration
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
const socket = io(API_URL);

function App() {
  // State
  const [connected, setConnected] = useState(false);
  const [prompt, setPrompt] = useState('');
  const [systemPrompt, setSystemPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [attackType, setAttackType] = useState('direct');
  const [realTimeMode, setRealTimeMode] = useState(true);
  const [tabValue, setTabValue] = useState(0);
  const [results, setResults] = useState([]);
  const [analysisData, setAnalysisData] = useState([]);
  const [success, setSuccess] = useState(false);
  
  const responseRef = useRef(null);

  // Socket connection
  useEffect(() => {
    socket.on('connect', () => {
      console.log('Socket connected');
      setConnected(true);
    });

    socket.on('connection_success', (data) => {
      console.log('Connection success:', data);
    });

    socket.on('disconnect', () => {
      console.log('Socket disconnected');
      setConnected(false);
    });

    socket.on('response_chunk', (data) => {
      setResponse(prev => prev + data.text);
      if (responseRef.current) {
        responseRef.current.scrollTop = responseRef.current.scrollHeight;
      }
    });

    socket.on('test_complete', (data) => {
      setLoading(false);
      setSuccess(data.success);
      // Add to results
      setResults(prev => [data, ...prev]);
      updateAnalysisData([data, ...results]);
    });

    socket.on('test_error', (data) => {
      setLoading(false);
      console.error('Test error:', data.error);
      setResponse(prev => prev + '\n\nError: ' + data.error);
    });

    // Load initial results
    fetchResults();

    return () => {
      socket.off('connect');
      socket.off('connection_success');
      socket.off('disconnect');
      socket.off('response_chunk');
      socket.off('test_complete');
      socket.off('test_error');
    };
  }, [results]);

  // Fetch past results
  const fetchResults = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/results`);
      setResults(response.data.results || []);
      updateAnalysisData(response.data.results || []);
    } catch (error) {
      console.error('Error fetching results:', error);
    }
  };

  // Update analysis data for charts
  const updateAnalysisData = (resultData) => {
    // Simple analysis - success rates by day
    const successByDay = {};
    
    resultData.forEach(result => {
      const date = result.timestamp.split('T')[0];
      if (!successByDay[date]) {
        successByDay[date] = { total: 0, success: 0 };
      }
      
      successByDay[date].total += 1;
      if (result.success) {
        successByDay[date].success += 1;
      }
    });
    
    const chartData = Object.keys(successByDay).map(date => ({
      date: date,
      successRate: (successByDay[date].success / successByDay[date].total) * 100,
      totalTests: successByDay[date].total
    }));
    
    setAnalysisData(chartData);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!prompt.trim()) return;
    
    setLoading(true);
    setResponse('');
    setSuccess(false);
    
    if (realTimeMode) {
      // Use WebSocket for real-time response
      socket.emit('run_test', {
        prompt,
        system_prompt: systemPrompt,
        attack_type: attackType
      });
    } else {
      // Use REST API
      try {
        const response = await axios.post(`${API_URL}/api/test`, {
          prompt,
          system_prompt: systemPrompt,
          attack_type: attackType
        });
        
        setResponse(response.data.response);
        setSuccess(response.data.success);
        setResults(prev => [response.data, ...prev]);
        updateAnalysisData([response.data, ...results]);
        setLoading(false);
      } catch (error) {
        console.error('Error running test:', error);
        setResponse(`Error: ${error.message}`);
        setLoading(false);
      }
    }
  };

  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static" color="primary">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              CLAUDE WHISPERER: Interactive Lab
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Typography variant="body2" sx={{ mr: 1 }}>
                {connected ? '🟢 Connected' : '🔴 Disconnected'}
              </Typography>
            </Box>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth="xl" sx={{ mt: 4 }}>
          <Tabs value={tabValue} onChange={handleTabChange} centered>
            <Tab label="Testing Interface" />
            <Tab label="Results" />
            <Tab label="Analytics" />
          </Tabs>
          
          {/* Testing Interface */}
          {tabValue === 0 && (
            <Grid container spacing={3} sx={{ mt: 2 }}>
              <Grid item xs={12} md={5}>
                <Paper
                  elevation={3}
                  sx={{
                    p: 3,
                    borderRadius: 2,
                    position: 'relative',
                    height: '80vh',
                    overflowY: 'auto'
                  }}
                >
                  <Typography variant="h6" gutterBottom>
                    Attack Configuration
                  </Typography>
                  
                  <form onSubmit={handleSubmit}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={realTimeMode}
                          onChange={() => setRealTimeMode(!realTimeMode)}
                          color="secondary"
                        />
                      }
                      label="Real-time Response Mode"
                    />
                    
                    <TextField
                      label="System Prompt (Optional)"
                      multiline
                      rows={3}
                      fullWidth
                      variant="outlined"
                      value={systemPrompt}
                      onChange={(e) => setSystemPrompt(e.target.value)}
                      sx={{ mt: 2, mb: 2 }}
                    />
                    
                    <TextField
                      label="Your Prompt"
                      multiline
                      rows={10}
                      fullWidth
                      required
                      variant="outlined"
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      sx={{ mb: 2 }}
                    />
                    
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      fullWidth
                      disabled={loading || !prompt.trim()}
                    >
                      {loading ? <CircularProgress size={24} /> : 'Test Prompt'}
                    </Button>
                  </form>
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={7}>
                <Paper
                  elevation={3}
                  sx={{
                    p: 3,
                    borderRadius: 2,
                    height: '80vh',
                    display: 'flex',
                    flexDirection: 'column'
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography variant="h6">
                      Claude's Response
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{
                        color: success ? 'success.main' : 'error.main',
                        fontWeight: 'bold'
                      }}
                    >
                      {response ? (success ? '✅ VULNERABLE!' : '❌ SECURE') : ''}
                    </Typography>
                  </Box>
                  
                  <Divider sx={{ mb: 2 }} />
                  
                  <Box
                    ref={responseRef}
                    sx={{
                      flexGrow: 1,
                      backgroundColor: 'background.default',
                      p: 2,
                      borderRadius: 1,
                      fontFamily: 'monospace',
                      overflowY: 'auto',
                      whiteSpace: 'pre-wrap'
                    }}
                  >
                    {loading && !response && (
                      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                        <CircularProgress />
                      </Box>
                    )}
                    {response}
                  </Box>
                </Paper>
              </Grid>
            </Grid>
          )}
          
          {/* Results Tab */}
          {tabValue === 1 && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                Test Results
              </Typography>
              
              <Grid container spacing={3}>
                {results.map((result, index) => (
                  <Grid item xs={12} key={index}>
                    <Card 
                      elevation={3} 
                      sx={{ 
                        borderLeft: result.success ? '4px solid #1eb980' : '4px solid #ff4081',
                        mb: 2 
                      }}
                    >
                      <CardContent>
                        <Typography variant="subtitle2" color="text.secondary">
                          {new Date(result.timestamp).toLocaleString()} - {result.success ? '✅ VULNERABLE' : '❌ SECURE'}
                        </Typography>
                        
                        <Typography variant="body2" sx={{ mt: 1, fontWeight: 'bold' }}>
                          Prompt:
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 0.5, maxHeight: '100px', overflowY: 'auto' }}>
                          {result.prompt}
                        </Typography>
                        
                        <Divider sx={{ my: 2 }} />
                        
                        <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                          Response:
                        </Typography>
                        <Typography 
                          variant="body2" 
                          sx={{ 
                            mt: 0.5, 
                            maxHeight: '200px', 
                            overflowY: 'auto',
                            whiteSpace: 'pre-wrap',
                            fontFamily: 'monospace'
                          }}
                        >
                          {result.response}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
                
                {results.length === 0 && (
                  <Grid item xs={12}>
                    <Paper sx={{ p: 3, textAlign: 'center' }}>
                      <Typography>No test results yet. Run some tests!</Typography>
                    </Paper>
                  </Grid>
                )}
              </Grid>
            </Box>
          )}
          
          {/* Analytics Tab */}
          {tabValue === 2 && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                Vulnerability Analytics
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Paper sx={{ p: 3 }}>
                    <Typography variant="subtitle1" gutterBottom>
                      Success Rate by Day
                    </Typography>
                    
                    {analysisData.length > 0 ? (
                      <BarChart
                        width={800}
                        height={400}
                        data={analysisData}
                        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis yAxisId="left" orientation="left" stroke="#1eb980" />
                        <YAxis yAxisId="right" orientation="right" stroke="#ff4081" />
                        <Tooltip />
                        <Legend />
                        <Bar yAxisId="left" dataKey="successRate" name="Success Rate (%)" fill="#1eb980" />
                        <Bar yAxisId="right" dataKey="totalTests" name="Total Tests" fill="#ff4081" />
                      </BarChart>
                    ) : (
                      <Typography sx={{ textAlign: 'center', my: 5 }}>
                        No data available for analysis yet.
                      </Typography>
                    )}
                  </Paper>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 3 }}>
                    <Typography variant="subtitle1" gutterBottom>
                      Overall Statistics
                    </Typography>
                    
                    <Typography variant="body1">
                      Total Tests: {results.length}
                    </Typography>
                    <Typography variant="body1">
                      Successful Jailbreaks: {results.filter(r => r.success).length}
                    </Typography>
                    <Typography variant="body1">
                      Success Rate: {results.length > 0 ? 
                        ((results.filter(r => r.success).length / results.length) * 100).toFixed(2) + '%' 
                        : '0%'}
                    </Typography>
                  </Paper>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 3 }}>
                    <Typography variant="subtitle1" gutterBottom>
                      Vulnerability Heat Map
                    </Typography>
                    
                    <Typography sx={{ textAlign: 'center', my: 5, fontStyle: 'italic' }}>
                      Advanced visualizations coming soon!
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </Box>
          )}
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
