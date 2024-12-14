import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Button,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Alert,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  CheckCircle as CheckIcon,
  Storage as StorageIcon,
  PlayArrow as StartIcon,
  Assessment as AssessmentIcon,
  AccessTime as AccessTimeIcon,
} from '@mui/icons-material';

const steps = [
  'Data Upload',
  'Preprocessing',
  'Training',
  'Evaluation',
];

const mockDatasets = [
  {
    name: 'training_data_v1.csv',
    size: '2.5GB',
    records: 1000000,
    status: 'processed',
    quality_score: 0.95,
  },
  {
    name: 'validation_data_v1.csv',
    size: '500MB',
    records: 200000,
    status: 'processing',
    quality_score: 0.92,
  },
  {
    name: 'test_data_v1.csv',
    size: '250MB',
    records: 100000,
    status: 'pending',
    quality_score: null,
  },
];

const mockTrainingJobs = [
  {
    id: 'train_001',
    status: 'completed',
    accuracy: 0.92,
    loss: 0.08,
    duration: '2h 15m',
    timestamp: '2023-11-15T10:00:00Z',
  },
  {
    id: 'train_002',
    status: 'running',
    progress: 65,
    timestamp: '2023-11-15T12:30:00Z',
  },
];

function DatasetCard({ dataset }) {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6">{dataset.name}</Typography>
          <Chip
            label={dataset.status}
            color={
              dataset.status === 'processed'
                ? 'success'
                : dataset.status === 'processing'
                ? 'warning'
                : 'default'
            }
            size="small"
          />
        </Box>
        <List dense>
          <ListItem>
            <ListItemIcon>
              <StorageIcon />
            </ListItemIcon>
            <ListItemText
              primary={`Size: ${dataset.size}`}
              secondary={`Records: ${dataset.records.toLocaleString()}`}
            />
          </ListItem>
          {dataset.quality_score && (
            <ListItem>
              <ListItemIcon>
                <AssessmentIcon />
              </ListItemIcon>
              <ListItemText
                primary={`Quality Score: ${(dataset.quality_score * 100).toFixed(1)}%`}
              />
            </ListItem>
          )}
        </List>
      </CardContent>
    </Card>
  );
}

function TrainingJobCard({ job }) {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6">Job {job.id}</Typography>
          <Chip
            label={job.status}
            color={job.status === 'completed' ? 'success' : 'warning'}
            size="small"
          />
        </Box>
        {job.status === 'running' ? (
          <>
            <LinearProgress
              variant="determinate"
              value={job.progress}
              sx={{ mb: 2 }}
            />
            <Typography variant="body2" color="textSecondary">
              Progress: {job.progress}%
            </Typography>
          </>
        ) : (
          <List dense>
            <ListItem>
              <ListItemIcon>
                <CheckIcon color="success" />
              </ListItemIcon>
              <ListItemText
                primary={`Accuracy: ${(job.accuracy * 100).toFixed(1)}%`}
                secondary={`Loss: ${job.loss.toFixed(3)}`}
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <AccessTimeIcon />
              </ListItemIcon>
              <ListItemText
                primary={`Duration: ${job.duration}`}
                secondary={`Completed: ${new Date(job.timestamp).toLocaleString()}`}
              />
            </ListItem>
          </List>
        )}
      </CardContent>
    </Card>
  );
}

function DataPipeline() {
  const [activeStep, setActiveStep] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = () => {
    setUploading(true);
    setError(null);
    // Simulate upload
    setTimeout(() => {
      setUploading(false);
      setActiveStep(1);
    }, 2000);
  };

  const handleNext = () => {
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 2 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>
        Data Pipeline
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Pipeline Steps */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <Box sx={{ mt: 4, mb: 2 }}>
          {activeStep === steps.length ? (
            <Typography variant="h6" align="center" color="success.main">
              Pipeline completed successfully!
            </Typography>
          ) : (
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <Button
                disabled={activeStep === 0}
                onClick={handleBack}
              >
                Back
              </Button>
              <Button
                variant="contained"
                onClick={activeStep === 0 ? handleUpload : handleNext}
                disabled={uploading}
                startIcon={activeStep === 0 ? <UploadIcon /> : <StartIcon />}
              >
                {activeStep === 0 ? 'Upload Data' : 'Start Processing'}
              </Button>
            </Box>
          )}
        </Box>
      </Paper>

      {/* Datasets */}
      <Typography variant="h5" sx={{ mb: 3 }}>
        Datasets
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {mockDatasets.map((dataset, index) => (
          <Grid item xs={12} md={4} key={index}>
            <DatasetCard dataset={dataset} />
          </Grid>
        ))}
      </Grid>

      {/* Training Jobs */}
      <Typography variant="h5" sx={{ mb: 3 }}>
        Training Jobs
      </Typography>
      <Grid container spacing={3}>
        {mockTrainingJobs.map((job, index) => (
          <Grid item xs={12} md={6} key={index}>
            <TrainingJobCard job={job} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default DataPipeline;
