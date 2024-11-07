import { useState, useEffect, useCallback, useRef } from 'react';
import { Box, Grid, Typography, CircularProgress, Alert } from '@mui/material';
import axios from 'axios';
import PromiseMenu from './PromiseMenu';
import InflationPromiseCard from './InflationPromiseCard';

const UPDATE_INTERVAL = 300000; // 5 minutes

function Dashboard() {
  const [categories, setCategories] = useState({});
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const initialFetchDone = useRef(false);
  const updateTimeoutRef = useRef(null);

  const transformData = useCallback((data) => {
    if (!data?.metrics) {
      console.error('No metrics in response data:', data);
      return null;
    }
    
    const metrics = data.metrics;
    console.log('Transforming metrics:', metrics);
    
    return {
      Inflation: [
        {
          id: 'cpi',
          title: metrics.cpi?.title || 'Consumer Price Index',
          description: 'Track changes in CPI',
          metric_type: 'cpi',
          current_value: metrics.cpi?.current_value,
          baseline_value: metrics.cpi?.baseline_value,
          percentage_change: metrics.cpi?.percentage_change,
          historical_data: metrics.cpi?.historical_data || [],
          units: metrics.cpi?.units,
          last_updated: metrics.cpi?.last_updated,
          analysis: data.analysis
        },
        {
          id: 'core_cpi',
          title: metrics.core_cpi?.title || 'Core Consumer Price Index',
          description: 'Track changes in Core CPI (excluding food and energy)',
          metric_type: 'core_cpi',
          current_value: metrics.core_cpi?.current_value,
          baseline_value: metrics.core_cpi?.baseline_value,
          percentage_change: metrics.core_cpi?.percentage_change,
          historical_data: metrics.core_cpi?.historical_data || [],
          units: metrics.core_cpi?.units,
          last_updated: metrics.core_cpi?.last_updated,
          analysis: data.analysis
        },
        {
          id: 'food',
          title: metrics.food?.title || 'Food Price Index',
          description: 'Track changes in food prices',
          metric_type: 'food',
          current_value: metrics.food?.current_value,
          baseline_value: metrics.food?.baseline_value,
          percentage_change: metrics.food?.percentage_change,
          historical_data: metrics.food?.historical_data || [],
          units: metrics.food?.units,
          last_updated: metrics.food?.last_updated,
          analysis: data.analysis
        },
        {
          id: 'gas',
          title: metrics.gas?.title || 'Gas Prices',
          description: 'Track changes in gas prices',
          metric_type: 'gas',
          current_value: metrics.gas?.current_value,
          baseline_value: metrics.gas?.baseline_value,
          percentage_change: metrics.gas?.percentage_change,
          historical_data: metrics.gas?.historical_data || [],
          units: metrics.gas?.units,
          last_updated: metrics.gas?.last_updated,
          analysis: data.analysis
        },
        {
          id: 'housing',
          title: metrics.housing?.title || 'Housing Price Index',
          description: 'Track changes in housing prices',
          metric_type: 'housing',
          current_value: metrics.housing?.current_value,
          baseline_value: metrics.housing?.baseline_value,
          percentage_change: metrics.housing?.percentage_change,
          historical_data: metrics.housing?.historical_data || [],
          units: metrics.housing?.units,
          last_updated: metrics.housing?.last_updated,
          analysis: data.analysis
        }
      ]
    };
  }, []);

  const fetchData = useCallback(async () => {
    try {
      console.log('Fetching data from API...');
      const response = await axios.get('http://localhost:5003/api/v1/inflation/data');
      console.log('API Response:', response.data);
      
      if (response.data.status !== 'Success') {
        throw new Error('API returned unsuccessful status');
      }
      
      const transformedData = transformData(response.data);
      console.log('Transformed data:', transformedData);
      
      if (transformedData) {
        setCategories(transformedData);
        if (!selectedCategory) {
          setSelectedCategory('Inflation');
        }
        setError(null);
      } else {
        throw new Error('Failed to transform data');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      setError(error.response?.status === 429 
        ? 'Rate limit exceeded. Please try again in a moment.'
        : 'Failed to fetch data. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, [transformData, selectedCategory]);

  // Initial data fetch
  useEffect(() => {
    if (!initialFetchDone.current) {
      console.log('Performing initial data fetch...');
      fetchData();
      initialFetchDone.current = true;
    }
  }, [fetchData]);

  // Set up periodic updates
  useEffect(() => {
    if (initialFetchDone.current) {
      console.log('Setting up periodic updates...');
      const startPeriodicFetch = () => {
        updateTimeoutRef.current = setTimeout(() => {
          console.log('Performing periodic update...');
          fetchData();
          startPeriodicFetch();
        }, UPDATE_INTERVAL);
      };

      startPeriodicFetch();
    }

    return () => {
      if (updateTimeoutRef.current) {
        clearTimeout(updateTimeoutRef.current);
      }
    };
  }, [fetchData]);

  const handleCategorySelect = useCallback((category) => {
    console.log('Selected category:', category);
    setSelectedCategory(category);
  }, []);

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
              {selectedCategory} Metrics ({selectedPromises?.length || 0})
            </Typography>
          </Box>
        )}
        
        {selectedCategory === 'Inflation' && selectedPromises && (
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
