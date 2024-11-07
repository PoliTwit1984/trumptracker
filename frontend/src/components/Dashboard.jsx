import { useState, useEffect } from 'react';
import { Box, Grid, Typography, CircularProgress, Alert } from '@mui/material';
import axios from 'axios';
import PromiseMenu from './PromiseMenu';
import InflationPromiseCard from './InflationPromiseCard';

function Dashboard() {
  const [categories, setCategories] = useState({});
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPromises = async () => {
      try {
        const response = await axios.get('http://localhost:5001/api/promises');
        console.log('Fetched promises:', response.data);
        setCategories(response.data);
        // Auto-select Inflation category
        if (response.data.Inflation) {
          setSelectedCategory('Inflation');
        }
        setLoading(false);
      } catch (error) {
        setError('Failed to fetch promises');
        setLoading(false);
        console.error('Error fetching promises:', error);
      }
    };

    fetchPromises();
  }, []);

  const handleCategorySelect = (category) => {
    console.log('Selected category:', category);
    console.log('Promises for category:', categories[category]);
    setSelectedCategory(category);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  const selectedPromises = selectedCategory ? categories[selectedCategory] : [];
  console.log('Rendering promises:', selectedPromises);

  return (
    <Box sx={{ 
      display: 'flex', 
      minHeight: '100vh',
      bgcolor: 'background.default'
    }}>
      {/* Left Sidebar Menu */}
      <Box sx={{ 
        width: 280, 
        flexShrink: 0, 
        borderRight: 1, 
        borderColor: 'divider',
        bgcolor: 'background.paper',
        position: 'fixed',
        height: '100vh',
        overflowY: 'auto',
        zIndex: 1
      }}>
        <Box sx={{ p: 2 }}>
          <Typography variant="h6" sx={{ mb: 2, pl: 2 }}>
            Dashboard
          </Typography>
          <PromiseMenu 
            categories={categories} 
            selectedCategory={selectedCategory}
            onCategorySelect={handleCategorySelect}
          />
        </Box>
      </Box>

      {/* Main Content */}
      <Box sx={{ 
        flexGrow: 1,
        ml: '280px', // Offset for fixed sidebar
        p: 3,
        maxWidth: 'calc(100vw - 280px)', // Prevent horizontal scrolling
        overflowX: 'hidden'
      }}>
        {selectedCategory && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="h5" sx={{ pl: 1 }}>
              {selectedCategory} Promises ({selectedPromises.length})
            </Typography>
          </Box>
        )}
        
        {selectedCategory === 'Inflation' && (
          <Grid 
            container 
            spacing={3} 
            columns={{ xs: 12, sm: 12, md: 12, lg: 12 }}
            sx={{ 
              width: '100%',
              m: 0, // Remove margin
              '& > .MuiGrid-item': {
                pt: 3, // Add top padding to grid items
                pl: 3, // Add left padding to grid items
              }
            }}
          >
            {selectedPromises.map(promise => (
              <Grid item xs={12} sm={6} lg={4} key={promise.id}>
                <InflationPromiseCard 
                  promise={promise}
                  metricType={promise.metric_type}
                />
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Box>
  );
}

export default Dashboard;
