import React, { useState, useCallback } from 'react';
import Layout from '../components/common/Layout';
import NewsDataFeed from '../components/perception/NewsDataFeed';
import newsApiService, { PerceptionData } from '../services/newsApi';
import { useAppContext } from '../context/AppContext';
import { useDataFetching } from '../hooks/useDataFetching';
// import { useMemoization } from '../hooks/useMemoization'; // Not currently used
// No need to import unused utilities
import '../utils/errorHandling';

// Enum for visualization types
enum VisualizationType {
  TEMPORAL = 'temporal',
  GEOGRAPHIC = 'geographic',
  NETWORK = 'network',
  TEXT = 'text'
}

// Enum for query themes
enum QueryTheme {
  AI_CONTAINMENT_POLICIES = 'AI Containment Policies',
  BIS_AND_DOC = 'BIS and Department of Commerce',
  CHINA_AI = 'China AI',
  NVIDIA_CHINA = 'Nvidia and China',
  CHIPS_ACT = 'CHIPS Act and Alliances',
  AI_LICENSING = 'AI Licensing',
  AI_COLD_WAR = 'AI Cold War',
  AI_SOVEREIGNTY = 'AI Sovereignty',
  OPENAI_SECURITY = 'OpenAI and Security'
}

const PerceptionTracker: React.FC = () => {
  // State for filters and visualization type
  const [dateRange, setDateRange] = useState({
    start: '2022-01-01',
    end: new Date().toISOString().split('T')[0] // Current date in YYYY-MM-DD format
  });
  const [selectedRegions, setSelectedRegions] = useState<string[]>([]);
  const [selectedActors, setSelectedActors] = useState<string[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [selectedNarratives, setSelectedNarratives] = useState<string[]>([]);
  const [selectedSources, setSelectedSources] = useState<string[]>([]);
  const [visualizationType, setVisualizationType] = useState<VisualizationType>(VisualizationType.TEMPORAL);
  
  // Use our context and custom hooks
  const { dispatch } = useAppContext();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { filteredData, fetchAllData } = useDataFetching(false);
  // We're not using filteredData directly, but it's part of the hook's return value
  
  // State for NewsAPI integration
  const [selectedQueryTheme, setSelectedQueryTheme] = useState<QueryTheme>(QueryTheme.AI_CONTAINMENT_POLICIES);
  const [newsQuery, setNewsQuery] = useState<string>(newsApiService.QUERY_THEMES.AI_CONTAINMENT_POLICIES);
  const [perceptionData, setPerceptionData] = useState<PerceptionData[]>([]);

  // Handler for filter application - memoized to prevent unnecessary re-renders
  const handleApplyFilters = useCallback(() => {
    // Update filters in context
    dispatch({ 
      type: 'SET_DATE_RANGE', 
      payload: dateRange 
    });
    
    dispatch({ 
      type: 'SET_SELECTED_REGIONS', 
      payload: selectedRegions 
    });
    
    dispatch({ 
      type: 'SET_SELECTED_ACTORS', 
      payload: selectedActors 
    });
    
    // Fetch data with new filters
    fetchAllData();
  }, [dateRange, selectedRegions, selectedActors, dispatch, fetchAllData]);

  // Handler for filter reset - memoized to prevent unnecessary re-renders
  const handleResetFilters = useCallback(() => {
    setDateRange({ start: '', end: '' });
    setSelectedRegions([]);
    setSelectedActors([]);
    setSelectedTopics([]);
    setSelectedNarratives([]);
    setSelectedSources([]);
    
    // Reset filters in context
    dispatch({ type: 'RESET_FILTERS' });
  }, [dispatch]);

  // Handler for query theme selection - memoized to prevent unnecessary re-renders
  const handleQueryThemeChange = useCallback((theme: QueryTheme) => {
    setSelectedQueryTheme(theme);
    
    // Set the appropriate query based on the selected theme
    switch (theme) {
      case QueryTheme.AI_CONTAINMENT_POLICIES:
        setNewsQuery(newsApiService.QUERY_THEMES.AI_CONTAINMENT_POLICIES);
        break;
      case QueryTheme.BIS_AND_DOC:
        setNewsQuery(newsApiService.QUERY_THEMES.BIS_AND_DOC);
        break;
      case QueryTheme.CHINA_AI:
        setNewsQuery(newsApiService.QUERY_THEMES.CHINA_AI);
        break;
      case QueryTheme.NVIDIA_CHINA:
        setNewsQuery(newsApiService.QUERY_THEMES.NVIDIA_CHINA);
        break;
      case QueryTheme.CHIPS_ACT:
        setNewsQuery(newsApiService.QUERY_THEMES.CHIPS_ACT);
        break;
      case QueryTheme.AI_LICENSING:
        setNewsQuery(newsApiService.QUERY_THEMES.AI_LICENSING);
        break;
      case QueryTheme.AI_COLD_WAR:
        setNewsQuery(newsApiService.QUERY_THEMES.AI_COLD_WAR);
        break;
      case QueryTheme.AI_SOVEREIGNTY:
        setNewsQuery(newsApiService.QUERY_THEMES.AI_SOVEREIGNTY);
        break;
      case QueryTheme.OPENAI_SECURITY:
        setNewsQuery(newsApiService.QUERY_THEMES.OPENAI_SECURITY);
        break;
    }
  }, []);

  // Handler for perception data loading
  const handlePerceptionDataLoaded = (data: PerceptionData[]) => {
    setPerceptionData(data);
    console.log('Perception data loaded:', data);
  };

  // Render visualization based on selected type
  const renderVisualization = () => {
    switch (visualizationType) {
      case VisualizationType.TEMPORAL:
        return (
          <div className="visualization-placeholder">
            <h3>Temporal Visualization</h3>
            <p>Line chart showing narrative trends over time</p>
            {/* This will be replaced with actual visualization component */}
          </div>
        );
      case VisualizationType.GEOGRAPHIC:
        return (
          <div className="visualization-placeholder">
            <h3>Geographic Visualization</h3>
            <p>World map with color-coded regions based on narrative intensity</p>
            {/* This will be replaced with actual visualization component */}
          </div>
        );
      case VisualizationType.NETWORK:
        return (
          <div className="visualization-placeholder">
            <h3>Network Visualization</h3>
            <p>Force-directed graph showing relationships between actors</p>
            {/* This will be replaced with actual visualization component */}
          </div>
        );
      case VisualizationType.TEXT:
        return (
          <div className="visualization-placeholder">
            <h3>Text-based Visualization</h3>
            <p>Word cloud showing key terms and their frequency</p>
            {/* This will be replaced with actual visualization component */}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <Layout>
      <div className="perception-tracker-page">
        <div className="page-header">
          <h1>Perception Tracker</h1>
          <button className="btn btn-outline">Export ▼</button>
        </div>

        <div className="perception-tracker-content">
          <div className="filters-column">
            <div className="filters-section">
              <h2>Filters</h2>
              <div className="filter-group">
                <label>Date Range:</label>
                <div className="date-inputs">
                  <input
                    type="date"
                    value={dateRange.start}
                    onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                    placeholder="Start"
                  />
                  <span>to</span>
                  <input
                    type="date"
                    value={dateRange.end}
                    onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
                    placeholder="End"
                  />
                </div>
              </div>

              <div className="filter-group">
                <label>Regions:</label>
                <select
                  multiple
                  value={selectedRegions}
                  onChange={(e) => setSelectedRegions(Array.from(e.target.selectedOptions, option => option.value))}
                >
                  <option value="north-america">North America</option>
                  <option value="europe">Europe</option>
                  <option value="east-asia">East Asia</option>
                  <option value="south-asia">South Asia</option>
                  {/* More options would be added here */}
                </select>
              </div>

              <div className="filter-group">
                <label>Actors:</label>
                <select
                  multiple
                  value={selectedActors}
                  onChange={(e) => setSelectedActors(Array.from(e.target.selectedOptions, option => option.value))}
                >
                  <option value="government">Government</option>
                  <option value="corporate">Corporate</option>
                  <option value="academic">Academic</option>
                  <option value="civil-society">Civil Society</option>
                  {/* More options would be added here */}
                </select>
              </div>

              <div className="filter-group">
                <label>Topics:</label>
                <select
                  multiple
                  value={selectedTopics}
                  onChange={(e) => setSelectedTopics(Array.from(e.target.selectedOptions, option => option.value))}
                >
                  <option value="regulation">Regulation</option>
                  <option value="safety">Safety</option>
                  <option value="innovation">Innovation</option>
                  <option value="ethics">Ethics</option>
                  {/* More options would be added here */}
                </select>
              </div>

              <div className="filter-group">
                <label>Narratives:</label>
                <select
                  multiple
                  value={selectedNarratives}
                  onChange={(e) => setSelectedNarratives(Array.from(e.target.selectedOptions, option => option.value))}
                >
                  <option value="ai-safety">AI Safety</option>
                  <option value="economic-growth">Economic Growth</option>
                  <option value="national-security">National Security</option>
                  <option value="job-displacement">Job Displacement</option>
                  {/* More options would be added here */}
                </select>
              </div>

              <div className="filter-group">
                <label>Sources:</label>
                <select
                  multiple
                  value={selectedSources}
                  onChange={(e) => setSelectedSources(Array.from(e.target.selectedOptions, option => option.value))}
                >
                  <option value="media">Media</option>
                  <option value="social">Social</option>
                  <option value="academic">Academic</option>
                  <option value="policy">Policy</option>
                  {/* More options would be added here */}
                </select>
              </div>

              <div className="filter-actions">
                <button className="btn btn-primary" onClick={handleApplyFilters}>Apply Filters</button>
                <button className="btn btn-outline" onClick={handleResetFilters}>Reset</button>
              </div>
            </div>

            <div className="visualization-type-section">
              <h2>Visualization Type</h2>
              <div className="radio-group">
                <label>
                  <input
                    type="radio"
                    name="visualization-type"
                    checked={visualizationType === VisualizationType.TEMPORAL}
                    onChange={() => setVisualizationType(VisualizationType.TEMPORAL)}
                  />
                  Temporal
                </label>
                <label>
                  <input
                    type="radio"
                    name="visualization-type"
                    checked={visualizationType === VisualizationType.GEOGRAPHIC}
                    onChange={() => setVisualizationType(VisualizationType.GEOGRAPHIC)}
                  />
                  Geographic
                </label>
                <label>
                  <input
                    type="radio"
                    name="visualization-type"
                    checked={visualizationType === VisualizationType.NETWORK}
                    onChange={() => setVisualizationType(VisualizationType.NETWORK)}
                  />
                  Network
                </label>
                <label>
                  <input
                    type="radio"
                    name="visualization-type"
                    checked={visualizationType === VisualizationType.TEXT}
                    onChange={() => setVisualizationType(VisualizationType.TEXT)}
                  />
                  Text-based
                </label>
              </div>
            </div>

            <div className="query-theme-section">
              <h2>Query Themes</h2>
              <div className="radio-group">
                {Object.values(QueryTheme).map((theme) => (
                  <label key={theme}>
                    <input
                      type="radio"
                      name="query-theme"
                      checked={selectedQueryTheme === theme}
                      onChange={() => handleQueryThemeChange(theme)}
                    />
                    {theme}
                  </label>
                ))}
              </div>
            </div>

            <div className="metrics-section">
              <h2>Metrics</h2>
              <ul className="metrics-list">
                <li>Total entries: {perceptionData.length || 'XXX'}</li>
                <li>Sentiment avg: {calculateAverageSentiment(perceptionData)}</li>
                <li>Top narrative: {getTopNarrative(perceptionData)}</li>
                <li>Top source: {getTopSource(perceptionData)}</li>
              </ul>
            </div>
          </div>

          <div className="visualization-column">
            <div className="visualization-display">
              {renderVisualization()}
            </div>

            <div className="news-data-section">
              <NewsDataFeed 
                query={newsQuery}
                fromDate={dateRange.start || undefined}
                toDate={dateRange.end || undefined}
                onDataLoaded={handlePerceptionDataLoaded}
              />
            </div>

            <div className="related-content">
              <h2>Related Content</h2>
              <div className="related-signals">
                <h3>Signals</h3>
                <ul>
                  <li><button className="link-button">Related Signal 1</button></li>
                  <li><button className="link-button">Related Signal 2</button></li>
                </ul>
              </div>
              <div className="related-timeline">
                <h3>Timeline Events</h3>
                <ul>
                  <li><button className="link-button">Related Event 1</button></li>
                  <li><button className="link-button">Related Event 2</button></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

// Helper function to get the most common item in an array
const getMostCommonItem = (arr: string[]): string => {
  if (!arr || !arr.length) return '';
  
  try {
    const counts = arr.reduce((acc, item) => {
      if (item) {
        acc[item] = (acc[item] || 0) + 1;
      }
      return acc;
    }, {} as Record<string, number>);
    
    const entries = Object.entries(counts);
    if (entries.length === 0) return '';
    
    return entries
      .sort((a, b) => b[1] - a[1])
      [0][0];
  } catch (error) {
    console.error('Error in getMostCommonItem:', error);
    return '';
  }
};

// Helper function to calculate average sentiment
const calculateAverageSentiment = (data: PerceptionData[]): string => {
  if (!data || data.length === 0) return 'X.X';
  
  try {
    const validSentiments = data.filter(item => typeof item.sentiment === 'number');
    if (validSentiments.length === 0) return 'X.X';
    
    const sum = validSentiments.reduce((acc, item) => acc + item.sentiment, 0);
    return (sum / validSentiments.length).toFixed(2);
  } catch (error) {
    console.error('Error calculating average sentiment:', error);
    return 'X.X';
  }
};

// Helper function to get top narrative
const getTopNarrative = (data: PerceptionData[]): string => {
  if (!data || data.length === 0) return 'XXXXX';
  
  try {
    const narratives = data.flatMap(item => 
      Array.isArray(item.narrativeTropes) ? item.narrativeTropes : []
    ).filter(Boolean);
    
    return narratives.length > 0 ? getMostCommonItem(narratives) : 'XXXXX';
  } catch (error) {
    console.error('Error getting top narrative:', error);
    return 'XXXXX';
  }
};

// Helper function to get top source
const getTopSource = (data: PerceptionData[]): string => {
  if (!data || data.length === 0) return 'XXXXX';
  
  try {
    const sources = data.map(item => item.source || 'Unknown').filter(Boolean);
    return sources.length > 0 ? getMostCommonItem(sources) : 'XXXXX';
  } catch (error) {
    console.error('Error getting top source:', error);
    return 'XXXXX';
  }
};

export default PerceptionTracker;
