import {
  Card,
  CardContent,
  Typography,
  Box,
  LinearProgress,
  Chip,
  IconButton,
  Collapse,
} from '@mui/material';
import { useState } from 'react';
import PropTypes from 'prop-types';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { styled } from '@mui/material/styles';

const ExpandMore = styled(IconButton, {
  shouldForwardProp: (prop) => prop !== 'expand',
})(({ theme, expand }) => ({
  transform: expand ? 'rotate(180deg)' : 'rotate(0deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
  height: 8,
  borderRadius: 4,
  [`&.MuiLinearProgress-colorPrimary`]: {
    backgroundColor: theme.palette.grey[800],
  },
  [`& .MuiLinearProgress-bar`]: {
    borderRadius: 4,
    backgroundColor: theme.palette.primary.main,
  },
}));

const getStatusColor = (status) => {
  switch (status.toLowerCase()) {
    case 'completed':
      return 'success';
    case 'in progress':
      return 'warning';
    case 'not started':
      return 'error';
    default:
      return 'default';
  }
};

function PromiseCard({ promise }) {
  const [expanded, setExpanded] = useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
    <Card
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: (theme) => `0 6px 12px ${theme.palette.background.default}`,
        },
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" component="div" gutterBottom>
            {promise.title}
          </Typography>
          <Chip
            label={promise.status}
            color={getStatusColor(promise.status)}
            size="small"
            sx={{
              '& .MuiChip-label': {
                color: 'white',
              },
            }}
          />
        </Box>

        <Typography variant="body2" color="text.secondary" gutterBottom>
          Category: {promise.category}
        </Typography>

        <Box sx={{ mt: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Progress
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {promise.progress_percentage}%
            </Typography>
          </Box>
          <BorderLinearProgress
            variant="determinate"
            value={promise.progress_percentage}
          />
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Last Updated: {new Date(promise.last_updated).toLocaleDateString()}
          </Typography>
          <ExpandMore
            expand={expanded}
            onClick={handleExpandClick}
            aria-expanded={expanded}
            aria-label="show more"
          >
            <ExpandMoreIcon />
          </ExpandMore>
        </Box>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <Box sx={{ mt: 2 }}>
            <Typography paragraph color="text.secondary">
              {promise.description}
            </Typography>
            <Typography variant="h6" gutterBottom color="text.primary">
              Key Events
            </Typography>
            {promise.key_events.map((event, index) => (
              <Box key={index} sx={{ mb: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  {new Date(event.date).toLocaleDateString()}
                </Typography>
                <Typography variant="body2" color="text.primary">
                  {event.description}
                </Typography>
              </Box>
            ))}
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
}

PromiseCard.propTypes = {
  promise: PropTypes.shape({
    id: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
    category: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    progress_percentage: PropTypes.number.isRequired,
    last_updated: PropTypes.string.isRequired,
    key_events: PropTypes.arrayOf(
      PropTypes.shape({
        date: PropTypes.string.isRequired,
        description: PropTypes.string.isRequired,
      })
    ).isRequired,
  }).isRequired,
};

export default PromiseCard;
