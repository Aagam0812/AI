import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

// Mock data - In production, this would come from your API
const mockMetrics = {
  requestsPerMinute: [
    { time: '00:00', value: 45 },
    { time: '00:01', value: 52 },
    { time: '00:02', value: 48 },
    { time: '00:03', value: 55 },
    { time: '00:04', value: 59 },
    { time: '00:05', value: 51 },
  ],
  systemMetrics: {
    cpu: 65,
    memory: 78,
    disk: 45,
  },
  modelMetrics: {
    accuracy: 0.92,
    latency: 150,
    errorRate: 0.02,
  },
};

function MetricCard({ title, value, unit, color }) {
  return (
    <Card>
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          {title}
        </Typography>
        <Typography variant="h4" component="div" color={color}>
          {value}
          {unit && <Typography variant="caption" sx={{ ml: 1 }}>{unit}</Typography>}
        </Typography>
      </CardContent>
    </Card>
  );
}

function SystemMetric({ label, value }) {
  return (
    <Box sx={{ mb: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
        <Typography variant="body2">{label}</Typography>
        <Typography variant="body2">{value}%</Typography>
      </Box>
      <LinearProgress 
        variant="determinate" 
        value={value} 
        sx={{
          height: 8,
          borderRadius: 4,
        }}
      />
    </Box>
  );
}

function Dashboard() {
  const [metrics, setMetrics] = useState(mockMetrics);

  // In production, fetch real metrics from your API
  useEffect(() => {
    // Simulating API call
    const fetchMetrics = () => {
      setMetrics(mockMetrics);
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>
        System Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Key Metrics */}
        <Grid item xs={12} md={4}>
          <MetricCard
            title="Model Accuracy"
            value={metrics.modelMetrics.accuracy * 100}
            unit="%"
            color="primary"
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <MetricCard
            title="Average Latency"
            value={metrics.modelMetrics.latency}
            unit="ms"
            color="secondary"
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <MetricCard
            title="Error Rate"
            value={metrics.modelMetrics.errorRate * 100}
            unit="%"
            color="error"
          />
        </Grid>

        {/* Requests Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Requests per Minute
            </Typography>
            <ResponsiveContainer width="100%" height="90%">
              <LineChart data={metrics.requestsPerMinute}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#8884d8"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* System Metrics */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 3 }}>
              System Resources
            </Typography>
            <SystemMetric label="CPU Usage" value={metrics.systemMetrics.cpu} />
            <SystemMetric label="Memory Usage" value={metrics.systemMetrics.memory} />
            <SystemMetric label="Disk Usage" value={metrics.systemMetrics.disk} />
          </Paper>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              System Status
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="textSecondary">
                  Model Status
                </Typography>
                <Typography variant="body1" color="success.main">
                  Operational
                </Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="textSecondary">
                  Last Updated
                </Typography>
                <Typography variant="body1">
                  {new Date().toLocaleString()}
                </Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="textSecondary">
                  Active Users
                </Typography>
                <Typography variant="body1">127</Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="textSecondary">
                  Total Requests Today
                </Typography>
                <Typography variant="body1">12,453</Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
