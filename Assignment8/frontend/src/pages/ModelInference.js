import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Card,
  CardContent,
  Divider,
  Alert,
  Chip,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import HistoryIcon from '@mui/icons-material/History';

function ModelInference() {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    setError(null);

    try {
      // In production, this would be an actual API call
      // const response = await api.post('/predict', { text: input });
      
      // Simulating API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      const mockResponse = {
        prediction: 1,
        confidence: 0.92,
        inference_time: 0.15,
        timestamp: new Date().toISOString()
      };

      setResult(mockResponse);
      setHistory(prev => [{
        input,
        ...mockResponse
      }, ...prev].slice(0, 5));
      
    } catch (err) {
      setError(err.message || 'An error occurred during inference');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 2 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>
        Model Inference
      </Typography>

      {/* Input Form */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            label="Enter text for inference"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            sx={{ mb: 2 }}
          />
          <Button
            type="submit"
            variant="contained"
            size="large"
            endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
            disabled={loading || !input.trim()}
          >
            Run Inference
          </Button>
        </form>
      </Paper>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      {/* Result Display */}
      {result && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Inference Result
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <Chip
                label={`Confidence: ${(result.confidence * 100).toFixed(2)}%`}
                color="primary"
              />
              <Chip
                label={`Inference Time: ${(result.inference_time * 1000).toFixed(0)}ms`}
                color="secondary"
              />
            </Box>
            <Typography variant="body1">
              Prediction Class: {result.prediction}
            </Typography>
            <Typography variant="caption" color="textSecondary">
              Timestamp: {new Date(result.timestamp).toLocaleString()}
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* History Section */}
      {history.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <HistoryIcon sx={{ mr: 1 }} />
            <Typography variant="h6">
              Recent Inferences
            </Typography>
          </Box>
          {history.map((item, index) => (
            <React.Fragment key={index}>
              {index > 0 && <Divider sx={{ my: 2 }} />}
              <Box>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Input:
                </Typography>
                <Typography variant="body1" sx={{ mb: 1 }}>
                  {item.input}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <Chip
                    size="small"
                    label={`Class: ${item.prediction}`}
                  />
                  <Chip
                    size="small"
                    label={`Confidence: ${(item.confidence * 100).toFixed(2)}%`}
                  />
                  <Chip
                    size="small"
                    label={`Time: ${(item.inference_time * 1000).toFixed(0)}ms`}
                  />
                </Box>
                <Typography variant="caption" color="textSecondary" display="block" sx={{ mt: 1 }}>
                  {new Date(item.timestamp).toLocaleString()}
                </Typography>
              </Box>
            </React.Fragment>
          ))}
        </Paper>
      )}
    </Box>
  );
}

export default ModelInference;
