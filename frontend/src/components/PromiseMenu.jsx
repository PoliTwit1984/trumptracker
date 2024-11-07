import { List, ListItemButton, ListItemText, Collapse } from '@mui/material';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { useState } from 'react';
import PropTypes from 'prop-types';

function PromiseMenu({ selectedCategory, onCategorySelect }) {
  // Start with the Inflation section expanded
  const [inflationOpen, setInflationOpen] = useState(true);

  const handleInflationClick = () => {
    setInflationOpen(!inflationOpen);
  };

  return (
    <List component="nav">
      {/* Inflation Section */}
      <ListItemButton onClick={handleInflationClick}>
        <ListItemText 
          primary="Inflation" 
          primaryTypographyProps={{
            fontWeight: 'medium',
            color: 'primary'
          }}
        />
        {inflationOpen ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Collapse in={inflationOpen} timeout="auto">
        <List component="div" disablePadding>
          <ListItemButton 
            sx={{ 
              pl: 4,
              '&.Mui-selected': {
                bgcolor: 'action.selected',
                '&:hover': {
                  bgcolor: 'action.selected',
                }
              }
            }}
            selected={selectedCategory === 'Metrics'}
            onClick={() => onCategorySelect('Metrics')}
          >
            <ListItemText primary="Metrics" />
          </ListItemButton>
          <ListItemButton 
            sx={{ 
              pl: 4,
              '&.Mui-selected': {
                bgcolor: 'action.selected',
                '&:hover': {
                  bgcolor: 'action.selected',
                }
              }
            }}
            selected={selectedCategory === 'Promises'}
            onClick={() => onCategorySelect('Promises')}
          >
            <ListItemText primary="Promises" />
          </ListItemButton>
        </List>
      </Collapse>
    </List>
  );
}

PromiseMenu.propTypes = {
  selectedCategory: PropTypes.string,
  onCategorySelect: PropTypes.func.isRequired
};

export default PromiseMenu;
