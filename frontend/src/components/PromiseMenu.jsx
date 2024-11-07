import { Box, List, ListItem, ListItemButton, ListItemText } from '@mui/material';
import PropTypes from 'prop-types';

function PromiseMenu({ categories, selectedCategory, onCategorySelect }) {
  return (
    <Box sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
      <List component="nav">
        {Object.keys(categories).map((category) => (
          <ListItem key={category} disablePadding>
            <ListItemButton 
              onClick={() => onCategorySelect(category)}
              selected={selectedCategory === category}
              sx={{
                '&.Mui-selected': {
                  bgcolor: 'action.selected',
                  borderLeft: 3,
                  borderColor: 'primary.main',
                  '&:hover': {
                    bgcolor: 'action.selected',
                  },
                },
              }}
            >
              <ListItemText 
                primary={category} 
                sx={{ 
                  color: selectedCategory === category ? 'primary.main' : 'text.primary',
                  pl: 1
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );
}

PromiseMenu.propTypes = {
  categories: PropTypes.object.isRequired,
  selectedCategory: PropTypes.string,
  onCategorySelect: PropTypes.func.isRequired
};

export default PromiseMenu;
