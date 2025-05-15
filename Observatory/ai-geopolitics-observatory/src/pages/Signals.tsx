import React, { useState, useEffect } from 'react';
import Layout from '../components/common/Layout';
import twitterApiService from '../services/twitterApi';

// Interface for Signal data
interface Signal {
  id: string;
  title: string;
  contributor: string;
  date: string;
  tags: string[];
  summary: string;
  upvotes: number;
  comments: number;
}

// Interface for Twitter Signal data
interface TwitterSignal {
  id: string;
  content: string;
  author: string;
  date: string;
  tags: string[];
  metrics: {
    likes: number;
    retweets: number;
    replies: number;
  };
  url: string;
}

const Signals: React.FC = () => {
  // State for filters
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [selectedContributor, setSelectedContributor] = useState<string>('');
  const [selectedLens, setSelectedLens] = useState<string>('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState<string>('recent');
  const [dataSource, setDataSource] = useState<'all' | 'manual' | 'twitter'>('all');
  const [twitterSignals, setTwitterSignals] = useState<TwitterSignal[]>([]);
  const [isLoadingTwitter, setIsLoadingTwitter] = useState<boolean>(false);
  const [twitterError, setTwitterError] = useState<string | null>(null);

  // Mock data for signals
  const [signals] = useState<Signal[]>([
    {
      id: '1',
      title: 'The Impact of Export Controls on AI Chip Development',
      contributor: 'Jane Smith',
      date: '2025-03-15',
      tags: ['Security', 'Policy'],
      summary: 'Analysis of how recent export controls are reshaping the global AI chip development landscape.',
      upvotes: 23,
      comments: 5
    },
    {
      id: '2',
      title: 'Ethical Considerations in AI Governance Frameworks',
      contributor: 'John Doe',
      date: '2025-03-10',
      tags: ['Ethics', 'Industrial'],
      summary: 'Examination of how ethical principles are being incorporated into emerging AI governance frameworks.',
      upvotes: 17,
      comments: 3
    },
    {
      id: '3',
      title: 'Social Implications of AI-Driven Automation',
      contributor: 'Alex Johnson',
      date: '2025-03-05',
      tags: ['Social', 'Legal'],
      summary: 'Assessment of the social and legal challenges arising from increased AI-driven automation.',
      upvotes: 9,
      comments: 1
    },
    {
      id: '4',
      title: 'Compute Resource Competition in AI Research',
      contributor: 'Sarah Williams',
      date: '2025-03-01',
      tags: ['Industrial', 'Security'],
      summary: 'Analysis of the growing competition for compute resources in advanced AI research and its implications.',
      upvotes: 5,
      comments: 0
    }
  ]);

  // Log environment variables on component mount
  useEffect(() => {
    console.log('Environment variables:');
    console.log('REACT_APP_TWITTER_API_KEY:', process.env.REACT_APP_TWITTER_API_KEY ? 'Set' : 'Not set');
    console.log('REACT_APP_TWITTER_API_SECRET:', process.env.REACT_APP_TWITTER_API_SECRET ? 'Set' : 'Not set');
    console.log('REACT_APP_TWITTER_BEARER_TOKEN:', process.env.REACT_APP_TWITTER_BEARER_TOKEN ? 'Set' : 'Not set');
    console.log('REACT_APP_NEWS_API_KEY:', process.env.REACT_APP_NEWS_API_KEY ? 'Set' : 'Not set');
  }, []);

  // Fetch Twitter data
  useEffect(() => {
    const fetchTwitterData = async () => {
      try {
        setIsLoadingTwitter(true);
        setTwitterError(null);
        
        // Select a query based on the selected lens or tags
        let query = twitterApiService.QUERY_THEMES.AI_COLD_WAR; // Default query
        
        if (selectedLens === 'security') {
          query = twitterApiService.QUERY_THEMES.AI_CONTAINMENT_POLICIES;
        } else if (selectedLens === 'industrial') {
          query = twitterApiService.QUERY_THEMES.NVIDIA_CHINA;
        } else if (selectedLens === 'ethics') {
          query = twitterApiService.QUERY_THEMES.OPENAI_SECURITY;
        } else if (selectedLens === 'legal') {
          query = twitterApiService.QUERY_THEMES.BIS_AND_DOC;
        }
        
        // Fetch tweets
        const response = await twitterApiService.searchRecentTweets(query, 10);
        
        if (response.data && response.includes?.users) {
          // Transform tweets to TwitterSignal format
          const transformedTweets: TwitterSignal[] = response.data.map(tweet => {
            const author = response.includes?.users.find(user => user.id === tweet.author_id);
            
            return {
              id: tweet.id,
              content: tweet.text,
              author: author?.name || 'Unknown',
              date: tweet.created_at,
              tags: tweet.entities?.hashtags?.map(h => h.tag) || [],
              metrics: {
                likes: tweet.public_metrics?.like_count || 0,
                retweets: tweet.public_metrics?.retweet_count || 0,
                replies: tweet.public_metrics?.reply_count || 0
              },
              url: `https://twitter.com/${author?.username}/status/${tweet.id}`
            };
          });
          
          setTwitterSignals(transformedTweets);
        } else {
          setTwitterError('No Twitter data available');
        }
      } catch (error) {
        console.error('Error fetching Twitter data:', error);
        setTwitterError('Failed to fetch Twitter data');
      } finally {
        setIsLoadingTwitter(false);
      }
    };
    
    // Only fetch if Twitter API keys are set
    const twitterBearerToken = process.env.REACT_APP_TWITTER_BEARER_TOKEN;
    if (twitterBearerToken) {
      console.log('Twitter API credentials found, fetching data...');
      fetchTwitterData();
    } else {
      console.log('Twitter API credentials not found');
      setTwitterError('Twitter API credentials not configured');
    }
  }, [selectedLens, selectedTags]);

  // Handler for filter application
  const handleApplyFilters = () => {
    // This would fetch data based on the selected filters
    console.log('Applying filters:', {
      dateRange,
      selectedContributor,
      selectedLens,
      selectedTags,
      sortBy,
      dataSource
    });
  };

  // Handler for filter reset
  const handleResetFilters = () => {
    setDateRange({ start: '', end: '' });
    setSelectedContributor('');
    setSelectedLens('');
    setSelectedTags([]);
    setDataSource('all');
  };

  return (
    <Layout>
      <div className="signals-page">
        <div className="page-header">
          <h1>Signals</h1>
          <button className="btn btn-outline">Export ▼</button>
        </div>

        <div className="signals-content">
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
                <label>Contributor:</label>
                <select
                  value={selectedContributor}
                  onChange={(e) => setSelectedContributor(e.target.value)}
                >
                  <option value="">All Contributors</option>
                  <option value="jane-smith">Jane Smith</option>
                  <option value="john-doe">John Doe</option>
                  <option value="alex-johnson">Alex Johnson</option>
                  <option value="sarah-williams">Sarah Williams</option>
                  {/* More options would be added here */}
                </select>
              </div>

              <div className="filter-group">
                <label>Lens:</label>
                <select
                  value={selectedLens}
                  onChange={(e) => setSelectedLens(e.target.value)}
                >
                  <option value="">All Lenses</option>
                  <option value="security">Security</option>
                  <option value="ethics">Ethics</option>
                  <option value="industrial">Industrial</option>
                  <option value="social">Social</option>
                  <option value="legal">Legal</option>
                </select>
              </div>

              <div className="filter-group">
                <label>Tags:</label>
                <select
                  multiple
                  value={selectedTags}
                  onChange={(e) => setSelectedTags(Array.from(e.target.selectedOptions, option => option.value))}
                >
                  <option value="regulation">Regulation</option>
                  <option value="safety">Safety</option>
                  <option value="compute">Compute</option>
                  <option value="china">China</option>
                  <option value="europe">Europe</option>
                  {/* More options would be added here */}
                </select>
              </div>

              <div className="filter-group">
                <label>Data Source:</label>
                <select
                  value={dataSource}
                  onChange={(e) => setDataSource(e.target.value as 'all' | 'manual' | 'twitter')}
                >
                  <option value="all">All Sources</option>
                  <option value="manual">Manual Signals</option>
                  <option value="twitter">Twitter</option>
                </select>
              </div>

              <div className="filter-group">
                <label>Data Source:</label>
                <select
                  value={dataSource}
                  onChange={(e) => setDataSource(e.target.value as 'all' | 'manual' | 'twitter')}
                >
                  <option value="all">All Sources</option>
                  <option value="manual">Manual Signals</option>
                  <option value="twitter">Twitter</option>
                </select>
              </div>

              <div className="filter-actions">
                <button className="btn btn-primary" onClick={handleApplyFilters}>Apply Filters</button>
                <button className="btn btn-outline" onClick={handleResetFilters}>Reset</button>
              </div>
            </div>

            <div className="popular-tags-section">
              <h2>Popular Tags</h2>
              <ul className="tags-list">
                <li><span className="tag">#regulation</span> (23)</li>
                <li><span className="tag">#safety</span> (19)</li>
                <li><span className="tag">#compute</span> (15)</li>
                <li><span className="tag">#china</span> (12)</li>
                <li><span className="tag">#europe</span> (10)</li>
              </ul>
            </div>

            <div className="interpretive-lenses-section">
              <h2>Interpretive Lenses</h2>
              <div className="radio-group">
                <label>
                  <input
                    type="radio"
                    name="lens-filter"
                    checked={selectedLens === ''}
                    onChange={() => setSelectedLens('')}
                  />
                  All
                </label>
                <label>
                  <input
                    type="radio"
                    name="lens-filter"
                    checked={selectedLens === 'security'}
                    onChange={() => setSelectedLens('security')}
                  />
                  Security
                </label>
                <label>
                  <input
                    type="radio"
                    name="lens-filter"
                    checked={selectedLens === 'ethics'}
                    onChange={() => setSelectedLens('ethics')}
                  />
                  Ethics
                </label>
                <label>
                  <input
                    type="radio"
                    name="lens-filter"
                    checked={selectedLens === 'industrial'}
                    onChange={() => setSelectedLens('industrial')}
                  />
                  Industrial
                </label>
                <label>
                  <input
                    type="radio"
                    name="lens-filter"
                    checked={selectedLens === 'social'}
                    onChange={() => setSelectedLens('social')}
                  />
                  Social
                </label>
                <label>
                  <input
                    type="radio"
                    name="lens-filter"
                    checked={selectedLens === 'legal'}
                    onChange={() => setSelectedLens('legal')}
                  />
                  Legal
                </label>
              </div>
            </div>
          </div>

          <div className="signals-list-column">
            <div className="signals-list-header">
              <div className="sort-by">
                <label>Sort by:</label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                >
                  <option value="recent">Recent</option>
                  <option value="popular">Popular</option>
                  <option value="comments">Most Commented</option>
                </select>
              </div>
            </div>

            <div className="signals-list">
              {/* Twitter data loading indicator */}
              {isLoadingTwitter && (
                <div className="loading-indicator">
                  <p>Loading Twitter data...</p>
                </div>
              )}

              {/* Twitter error message */}
              {twitterError && (
                <div className="error-message">
                  <p>{twitterError}</p>
                </div>
              )}

              {/* Manual signals */}
              {(dataSource === 'all' || dataSource === 'manual') && signals.map(signal => (
                <div key={signal.id} className="signal-card">
                  <h2 className="signal-title">{signal.title}</h2>
                  <div className="signal-meta">
                    <span className="contributor">{signal.contributor}</span>
                    <span className="date">{signal.date}</span>
                  </div>
                  <div className="signal-tags">
                    {signal.tags.map(tag => (
                      <span key={tag} className="tag">{tag}</span>
                    ))}
                  </div>
                  <p className="signal-summary">{signal.summary}</p>
                  <div className="signal-stats">
                    <span className="upvotes">{signal.upvotes} upvotes</span>
                    <span className="comments">{signal.comments} comments</span>
                  </div>
                </div>
              ))}

              {/* Twitter signals */}
              {(dataSource === 'all' || dataSource === 'twitter') && twitterSignals.map(tweet => (
                <div key={tweet.id} className="signal-card twitter-signal">
                  <div className="signal-source">
                    <span className="source-icon">🐦</span>
                    <span className="source-label">Twitter</span>
                  </div>
                  <div className="signal-meta">
                    <span className="contributor">{tweet.author}</span>
                    <span className="date">{new Date(tweet.date).toLocaleDateString()}</span>
                  </div>
                  <p className="signal-summary">{tweet.content}</p>
                  <div className="signal-tags">
                    {tweet.tags.map(tag => (
                      <span key={tag} className="tag">#{tag}</span>
                    ))}
                  </div>
                  <div className="signal-stats">
                    <span className="likes">{tweet.metrics.likes} likes</span>
                    <span className="retweets">{tweet.metrics.retweets} retweets</span>
                    <span className="replies">{tweet.metrics.replies} replies</span>
                  </div>
                  <div className="signal-actions">
                    <a href={tweet.url} target="_blank" rel="noopener noreferrer" className="view-source">
                      View on Twitter
                    </a>
                  </div>
                </div>
              ))}

              <button className="btn btn-outline load-more">Load more signals</button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Signals;
