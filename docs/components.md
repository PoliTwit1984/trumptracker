# Component Documentation

## InflationPromiseCard
Displays individual economic indicators with the following features:
- Current value and year-ago comparison
- Year-over-year percentage change
- Status indicator (Improving/Worsening)
- Interactive price trend chart
- Last updated timestamp

### Props
```javascript
{
  promise: PropTypes.shape({
    id: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
    category: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
  }).isRequired,
  metricType: PropTypes.string.isRequired,
}
```

## PromiseMenu
Navigation component with the following features:
- Category-based organization
- Visual selection indicators
- Smooth transitions
- Fixed positioning with scroll

### Props
```javascript
{
  categories: PropTypes.object.isRequired,
  selectedCategory: PropTypes.string,
  onCategorySelect: PropTypes.func.isRequired
}
