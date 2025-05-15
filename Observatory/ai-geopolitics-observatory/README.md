# Public Observatory of AI Geopolitics

The Public Observatory of AI Geopolitics (POAIG) is an educational resource for researchers and students focused on understanding the complex geopolitical landscape of artificial intelligence.

## Project Overview

This platform provides unique insights through three main components:

1. **Perception Tracker**: Visualizes media headlines, social media discourse, and narrative tropes related to AI geopolitics.
2. **Signals**: Features expert analysis and insights on emerging trends and developments in AI geopolitics.
3. **Timeline & Policy Map**: Provides chronological context for key regulatory developments, corporate actions, and bloc-level initiatives.

## Getting Started

### Prerequisites

- Node.js (v14.0.0 or later)
- npm (v6.0.0 or later)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-geopolitics-observatory.git
   cd ai-geopolitics-observatory
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   REACT_APP_SERP_API_KEY=your_serp_api_key
   REACT_APP_TWITTER_API_KEY=your_twitter_api_key
   REACT_APP_TWITTER_API_SECRET=your_twitter_api_secret
   REACT_APP_TWITTER_BEARER_TOKEN=your_twitter_bearer_token
   ```

4. Start the development server:
   ```
   npm start
   ```

5. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
ai-geopolitics-observatory/
├── public/                  # Public assets
├── src/                     # Source code
│   ├── components/          # Reusable components
│   │   ├── common/          # Common components (Header, Footer, etc.)
│   │   ├── perception/      # Perception Tracker components
│   │   ├── signals/         # Signals components
│   │   └── timeline/        # Timeline components
│   ├── context/             # React Context for state management
│   ├── hooks/               # Custom React hooks
│   │   ├── useDataFetching.ts  # Hook for API data fetching
│   │   └── useMemoization.ts   # Hook for performance optimization
│   ├── pages/               # Page components
│   ├── services/            # API services
│   ├── styles/              # CSS styles
│   ├── utils/               # Utility functions
│   │   ├── errorHandling.ts    # Error handling utilities
│   │   └── textAnalysis.ts     # Text analysis utilities
│   ├── App.tsx              # Main App component
│   └── index.tsx            # Entry point
├── package.json             # Dependencies and scripts
└── tsconfig.json            # TypeScript configuration
```

## Features

### Perception Tracker
- Visualization dashboard with temporal, geographic, network, and text-based visualizations
- Filtering by date range, region, actor, topic, narrative, and source
- Export functionality for research use

### Signals
- Browsing and filtering of expert signals
- Categorization by interpretive lens (security, ethics, industrial, social, legal)
- Upvoting and commenting system

### Timeline & Policy Map
- Chronological display of key regulatory developments
- Filtering by actor or asset type
- Integration with Signals (showing related signals for timeline events)

## Technology Stack

- **Frontend**: React with TypeScript
- **Routing**: React Router
- **State Management**: React Context API with useReducer
- **Visualization**: Recharts, React Simple Maps, React Force Graph, React Wordcloud
- **Styling**: CSS
- **API Integration**: Twitter API, News API (via SerpAPI)
- **Performance Optimization**: Code splitting, lazy loading, memoization

## Architecture

The application follows a modern React architecture with several key features:

### State Management
- Uses React Context API with useReducer for global state management
- Centralized state for filters, data, loading states, and errors

### Code Organization
- Modular component structure with clear separation of concerns
- Custom hooks for reusable logic
- Utility functions for common operations

### Performance Optimization
- Code splitting and lazy loading for improved initial load time
- Memoization of expensive calculations
- Efficient rendering with React.memo and useMemo

### API Integration
- Secure handling of API keys using environment variables
- Standardized error handling
- Retry logic for API requests

## Security Considerations

- API keys are stored in environment variables, not in source code
- Sensitive data is not logged to the console
- CORS proxy usage is documented and can be replaced with a secure backend proxy

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines
1. Follow the existing code structure and naming conventions
2. Write clean, maintainable, and well-documented code
3. Add appropriate error handling
4. Use TypeScript types for better code quality
5. Test your changes thoroughly

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project is part of an educational initiative to improve understanding of AI geopolitics.
- Thanks to all contributors and researchers who have provided insights and data.
