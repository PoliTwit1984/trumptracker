import { useState } from 'react';
import { Box, Typography, Checkbox, FormControlLabel, Accordion, AccordionSummary, AccordionDetails, Chip } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const promises = {
  'Core Inflation Promises': [
    {
      id: 'end_inflation',
      text: 'End inflation entirely',
      source: 'AP News',
      sourceLink: 'https://apnews.com/article/trump-inflation-tariffs-taxes-immigration-federal-reserve-a18de763fcc01557258c7f33cab375ed',
      completed: false
    },
    {
      id: 'decrease_prices',
      text: 'Make prices "decrease dramatically and quickly"',
      source: 'AP News',
      sourceLink: 'https://apnews.com/article/trump-inflation-tariffs-taxes-immigration-federal-reserve-a18de763fcc01557258c7f33cab375ed',
      completed: false
    },
    {
      id: 'elon_commission',
      text: 'Create economic commission led by Elon Musk',
      source: 'TIME',
      sourceLink: 'https://time.com/7095898/donald-trump-economy-plan-2024/',
      completed: false
    }
  ],
  'Energy Costs': [
    {
      id: 'cut_energy_costs',
      text: 'Cut energy costs by 50% within first year',
      source: 'CNN',
      sourceLink: 'https://www.cnn.com/2024/08/20/business/trump-inflation-prices-deflation/index.html',
      completed: false
    },
    {
      id: 'lower_gas_prices',
      text: 'Lower gas prices "below $2 a gallon"',
      source: 'CNN',
      sourceLink: 'https://www.cnn.com/2024/08/20/business/trump-inflation-prices-deflation/index.html',
      completed: false
    },
    {
      id: 'emergency_declaration',
      text: 'Issue "national emergency declaration" to increase domestic energy supply',
      source: 'NBC News',
      sourceLink: 'https://www.nbcnews.com/politics/2024-election/trumps-return-white-house-mean-economy-taxes-rcna177690',
      completed: false
    },
    {
      id: 'expand_drilling',
      text: 'Expand oil/gas drilling on federal land, including Alaska',
      source: 'LA Times',
      sourceLink: 'https://www.latimes.com/politics/story/2024-10-16/2024-election-trump-campaign-promises-reality',
      completed: false
    }
  ],
  'Tax Measures': [
    {
      id: 'social_security_tax',
      text: 'Eliminate federal taxes on Social Security benefits',
      source: 'NBC News',
      sourceLink: 'https://www.nbcnews.com/politics/2024-election/trumps-return-white-house-mean-economy-taxes-rcna177690',
      completed: false
    },
    {
      id: 'tips_tax',
      text: 'Eliminate federal taxes on tips',
      source: 'NBC News',
      sourceLink: 'https://www.nbcnews.com/politics/2024-election/trumps-return-white-house-mean-economy-taxes-rcna177690',
      completed: false
    },
    {
      id: 'overtime_tax',
      text: 'Eliminate federal taxes on overtime pay',
      source: 'NBC News',
      sourceLink: 'https://www.nbcnews.com/politics/2024-election/trumps-return-white-house-mean-economy-taxes-rcna177690',
      completed: false
    },
    {
      id: 'car_loan_interest',
      text: 'Make car loan interest fully tax-deductible',
      source: 'TIME',
      sourceLink: 'https://time.com/7095898/donald-trump-economy-plan-2024/',
      completed: false
    },
    {
      id: 'credit_card_interest',
      text: 'Temporarily cap credit card interest rates at 10%',
      source: 'TIME',
      sourceLink: 'https://time.com/7095898/donald-trump-economy-plan-2024/',
      completed: false
    }
  ],
  'Trade Policy': [
    {
      id: 'overseas_tariffs',
      text: 'Impose 10-20% tariffs on all overseas imports',
      source: 'NBC News',
      sourceLink: 'https://www.nbcnews.com/politics/2024-election/trumps-return-white-house-mean-economy-taxes-rcna177690',
      completed: false
    },
    {
      id: 'china_tariffs',
      text: 'Impose 60% or higher tariffs on Chinese imports',
      source: 'NBC News',
      sourceLink: 'https://www.nbcnews.com/politics/2024-election/trumps-return-white-house-mean-economy-taxes-rcna177690',
      completed: false
    },
    {
      id: 'matching_tariffs',
      text: 'Match other countries\' levies on American goods',
      source: 'NBC News',
      sourceLink: 'https://www.nbcnews.com/politics/2024-election/trumps-return-white-house-mean-economy-taxes-rcna177690',
      completed: false
    }
  ],
  'Housing Affordability': [
    {
      id: 'protected_lands',
      text: 'Build on federally protected lands',
      source: 'LA Times',
      sourceLink: 'https://www.latimes.com/politics/story/2024-10-16/2024-election-trump-campaign-promises-reality',
      completed: false
    },
    {
      id: 'builder_regulations',
      text: 'Reduce builder regulations',
      source: 'LA Times',
      sourceLink: 'https://www.latimes.com/politics/story/2024-10-16/2024-election-trump-campaign-promises-reality',
      completed: false
    },
    {
      id: 'homeownership_incentives',
      text: 'Implement tax incentives for homeownership',
      source: 'LA Times',
      sourceLink: 'https://www.latimes.com/politics/story/2024-10-16/2024-election-trump-campaign-promises-reality',
      completed: false
    },
    {
      id: 'federal_land_housing',
      text: 'Open federal land for housing projects',
      source: 'LA Times',
      sourceLink: 'https://www.latimes.com/politics/story/2024-10-16/2024-election-trump-campaign-promises-reality',
      completed: false
    }
  ]
};

function PromiseTracker() {
  const [checkedPromises, setCheckedPromises] = useState({});
  const [expandedSections, setExpandedSections] = useState(
    Object.keys(promises).reduce((acc, category) => {
      acc[category] = true; // Set all sections to expanded by default
      return acc;
    }, {})
  );

  const handlePromiseToggle = (promiseId) => {
    setCheckedPromises(prev => ({
      ...prev,
      [promiseId]: !prev[promiseId]
    }));
  };

  const handleSectionToggle = (category) => {
    setExpandedSections(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Campaign Promises Tracker
      </Typography>
      
      {Object.entries(promises).map(([category, categoryPromises]) => (
        <Accordion 
          key={category} 
          expanded={expandedSections[category]}
          onChange={() => handleSectionToggle(category)}
          sx={{ 
            mb: 2, 
            bgcolor: 'background.paper',
            '&:before': {
              display: 'none', // Removes the default divider
            }
          }}
        >
          <AccordionSummary 
            expandIcon={<ExpandMoreIcon />}
            sx={{
              borderBottom: 1,
              borderColor: 'divider'
            }}
          >
            <Typography variant="h6">{category}</Typography>
          </AccordionSummary>
          <AccordionDetails>
            {categoryPromises.map((promise) => (
              <Box 
                key={promise.id} 
                sx={{ 
                  mb: 2,
                  display: 'flex',
                  alignItems: 'flex-start'
                }}
              >
                <Chip 
                  label="Waiting" 
                  size="small"
                  sx={{ 
                    mr: 1, 
                    mt: 1,
                    bgcolor: 'error.main',
                    color: 'white',
                    fontWeight: 'medium',
                    '& .MuiChip-label': {
                      px: 1.5 // Add more horizontal padding
                    }
                  }}
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={checkedPromises[promise.id] || false}
                      onChange={() => handlePromiseToggle(promise.id)}
                    />
                  }
                  label={
                    <Box>
                      <Typography>{promise.text}</Typography>
                      <Typography 
                        variant="caption" 
                        component="a" 
                        href={promise.sourceLink}
                        target="_blank"
                        rel="noopener noreferrer"
                        sx={{ 
                          color: 'text.secondary',
                          textDecoration: 'none',
                          '&:hover': {
                            textDecoration: 'underline'
                          }
                        }}
                      >
                        Source: {promise.source}
                      </Typography>
                    </Box>
                  }
                  sx={{
                    alignItems: 'flex-start',
                    '& .MuiFormControlLabel-label': {
                      mt: -0.5
                    }
                  }}
                />
              </Box>
            ))}
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );
}

export default PromiseTracker;
