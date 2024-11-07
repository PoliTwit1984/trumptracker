import PropTypes from 'prop-types';
import { Card, CardContent, Typography, Box, IconButton, Collapse } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useState } from 'react';
import { styled } from '@mui/material/styles';

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} sx={{ transform: expand ? 'rotate(180deg)' : 'rotate(0deg)' }} />;
})(({ theme }) => ({
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

function InflationPromiseCard({ promise }) {
  const [expanded, setExpanded] = useState(false);

  if (!promise) {
    console.error('No promise data provided to InflationPromiseCard');
    return null;
  }

  console.log('Rendering InflationPromiseCard with data:', promise);

  const formatValue = (value) => {
    if (typeof value !== 'number') return 'N/A';
    return value.toFixed(2);
  };

  const formatPercentage = (value) => {
    if (typeof value !== 'number') return 'N/A';
    return `${value > 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  const getValueColor = (percentage) => {
    if (typeof percentage !== 'number') return 'text.primary';
    return percentage > 0 ? 'error.main' : 'success.main';
  };

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
    <Card sx={{ 
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      bgcolor: 'background.paper',
      borderRadius: 2,
      boxShadow: 3
    }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography variant="h6" component="div" gutterBottom>
          {promise.title || 'Unknown Metric'}
        </Typography>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Current Value
          </Typography>
          <Typography variant="h4" component="div">
            {formatValue(promise.current_value)}
            <Typography component="span" variant="body2" sx={{ ml: 1 }}>
              {promise.units}
            </Typography>
          </Typography>
        </Box>

        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Change from Previous Year
          </Typography>
          <Typography 
            variant="h5" 
            component="div"
            sx={{ color: getValueColor(promise.percentage_change) }}
          >
            {formatPercentage(promise.percentage_change)}
          </Typography>
        </Box>

        {promise.historical_data && promise.historical_data.length > 0 && (
          <Box sx={{ height: 200, mt: 3 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={promise.historical_data}
                margin={{
                  top: 5,
                  right: 5,
                  left: 5,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tick={{ fontSize: 12 }}
                  interval="preserveStartEnd"
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  domain={['auto', 'auto']}
                />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#8884d8"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </Box>
        )}

        <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Typography variant="body2" color="text.secondary">
            Last Updated: {promise.last_updated || 'Unknown'}
          </Typography>
          {promise.analysis && (
            <ExpandMore
              expand={expanded}
              onClick={handleExpandClick}
              aria-expanded={expanded}
              aria-label="show analysis"
              size="small"
            >
              <ExpandMoreIcon />
            </ExpandMore>
          )}
        </Box>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <Box sx={{ 
            mt: 2, 
            p: 2, 
            bgcolor: 'rgba(255, 255, 255, 0.05)', 
            borderRadius: 1,
            border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <Typography 
              variant="body2" 
              component="pre" 
              sx={{ 
                whiteSpace: 'pre-wrap',
                fontFamily: 'inherit',
                mb: 0,
                color: 'rgba(255, 255, 255, 0.9)',
                lineHeight: 1.6
              }}
            >
              {promise.analysis}
            </Typography>
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
}

InflationPromiseCard.propTypes = {
  promise: PropTypes.shape({
    id: PropTypes.string,
    title: PropTypes.string,
    description: PropTypes.string,
    metric_type: PropTypes.string,
    current_value: PropTypes.number,
    baseline_value: PropTypes.number,
    percentage_change: PropTypes.number,
    historical_data: PropTypes.arrayOf(
      PropTypes.shape({
        date: PropTypes.string,
        value: PropTypes.number
      })
    ),
    units: PropTypes.string,
    last_updated: PropTypes.string,
    analysis: PropTypes.string
  }).isRequired
};

export default InflationPromiseCard;
