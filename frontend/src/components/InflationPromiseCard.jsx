import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  CircularProgress,
  Alert,
  Tooltip,
  IconButton,
  Collapse,
  Link,
} from '@mui/material';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { LineChart, Line, XAxis, YAxis, Tooltip as ChartTooltip, ResponsiveContainer } from 'recharts';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import axios from 'axios';

const MetricCard = ({ title, value, baselineValue, change, units }) => (
  <Tooltip title={`${title} - measured in ${units}`} arrow>
    <Box sx={{ mb: 2, p: 1, bgcolor: 'background.paper', borderRadius: 1, cursor: 'help' }}>
      <Typography variant="h6">
        {value.toFixed(2)} {units}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Year ago: {baselineValue.toFixed(2)} {units}
      </Typography>
      <Typography
        variant="body2"
        color={change >= 0 ? 'error.main' : 'success.main'}
      >
        {change >= 0 ? '+' : ''}{change.toFixed(2)}% year-over-year
      </Typography>
    </Box>
  </Tooltip>
);

MetricCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  baselineValue: PropTypes.number.isRequired,
  change: PropTypes.number.isRequired,
  units: PropTypes.string.isRequired,
};

const getMetricDetails = (metricType) => {
  const details = {
    cpi: {
      name: 'CPI-U (Consumer Price Index for All Urban Consumers)',
      description: 'Overall inflation',
      frequency: 'Monthly'
    },
    core_cpi: {
      name: 'Core CPI (excluding food and energy)',
      description: 'Underlying inflation trends',
      frequency: 'Monthly'
    },
    food: {
      name: 'Food CPI',
      description: 'Food price inflation',
      frequency: 'Monthly'
    },
    gas: {
      name: 'Regular Gas Prices',
      description: 'National average gas prices',
      frequency: 'Weekly'
    },
    housing: {
      name: 'Case-Shiller Home Price Index',
      description: 'Housing market trends',
      frequency: 'Monthly'
    }
  };
  return details[metricType] || { name: 'Unknown metric', description: '', frequency: '' };
};

function InflationPromiseCard({ promise, metricType }) {
  const [inflationData, setInflationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    const fetchInflationData = async () => {
      try {
        const response = await axios.get('http://localhost:5001/api/inflation-data');
        setInflationData(response.data);
        setLoading(false);
      } catch (error) {
        setError('Failed to fetch inflation data');
        setLoading(false);
        console.error('Error fetching inflation data:', error);
      }
    };

    fetchInflationData();
    // Refresh data every hour
    const interval = setInterval(fetchInflationData, 3600000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <Card sx={{ minHeight: 300, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <CircularProgress />
      </Card>
    );
  }

  if (error) {
    return (
      <Card sx={{ minHeight: 300 }}>
        <CardContent>
          <Alert severity="error">{error}</Alert>
        </CardContent>
      </Card>
    );
  }

  const metrics = inflationData?.metrics || {};
  const metric = metrics[metricType];
  
  if (!metric) {
    return (
      <Card sx={{ minHeight: 300 }}>
        <CardContent>
          <Alert severity="error">Metric data not found</Alert>
        </CardContent>
      </Card>
    );
  }

  const status = metric.percentage_change >= 0 ? 'Worsening' : 'Improving';
  const metricDetails = getMetricDetails(metricType);

  return (
    <Card sx={{ minHeight: 300 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" component="div">
            {promise.title}
          </Typography>
          <Chip
            label={status}
            color={status === 'Improving' ? 'success' : 'error'}
            sx={{ ml: 1 }}
          />
        </Box>

        <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 2 }}>
          Analysis as of November 5th, 2024 (Day after Election)
        </Typography>

        <MetricCard
          title={metric.title}
          value={metric.current_value}
          baselineValue={metric.baseline_value}
          change={metric.percentage_change}
          units={metric.units}
        />

        <Box sx={{ mt: 3, height: 200 }}>
          <Typography variant="subtitle2" gutterBottom>
            Price Trend
          </Typography>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={metric.historical_data}
              margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
            >
              <Line
                type="monotone"
                dataKey="value"
                name={metric.title}
                stroke="#8884d8"
                dot={false}
              />
              <XAxis
                dataKey="date"
                tickFormatter={(date) => new Date(date).toLocaleDateString()}
              />
              <YAxis />
              <ChartTooltip
                labelFormatter={(date) => new Date(date).toLocaleDateString()}
                formatter={(value) => [value.toFixed(2), metric.title]}
              />
            </LineChart>
          </ResponsiveContainer>
        </Box>

        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            Last updated: {new Date(inflationData.last_updated).toLocaleString()}
          </Typography>
          <IconButton
            onClick={() => setExpanded(!expanded)}
            sx={{
              transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
              transition: 'transform 0.3s',
            }}
            aria-expanded={expanded}
            aria-label="show analysis"
          >
            <ExpandMoreIcon />
          </IconButton>
        </Box>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
            <Typography variant="h6" gutterBottom>
              AI Analysis
            </Typography>
            <Typography variant="body2" paragraph>
              {inflationData.analysis}
            </Typography>
          </Box>
        </Collapse>

        <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid rgba(0, 0, 0, 0.12)' }}>
          <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
            Data source: {' '}
            <Link 
              href="https://fred.stlouisfed.org/" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              Federal Reserve Economic Data (FRED)
            </Link>
          </Typography>
          <Typography variant="caption" color="text.secondary" display="block">
            Metric: {metricDetails.name} - {metricDetails.description} ({metricDetails.frequency} data)
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}

InflationPromiseCard.propTypes = {
  promise: PropTypes.shape({
    id: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
    category: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
  }).isRequired,
  metricType: PropTypes.string.isRequired,
};

export default InflationPromiseCard;
