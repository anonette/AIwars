import axios from 'axios';
import { PerceptionData } from './newsApi';
import * as textAnalysis from '../utils/textAnalysis';
import * as errorHandling from '../utils/errorHandling';

// Types for Twitter API responses
export interface TwitterUser {
  id: string;
  name: string;
  username: string;
  profile_image_url?: string;
}

export interface TwitterTweet {
  id: string;
  text: string;
  created_at: string;
  author_id: string;
  public_metrics?: {
    retweet_count: number;
    reply_count: number;
    like_count: number;
    quote_count: number;
  };
  entities?: {
    hashtags?: { tag: string }[];
    mentions?: { username: string }[];
    urls?: { expanded_url: string }[];
  };
}

export interface TwitterApiResponse {
  data: TwitterTweet[];
  includes?: {
    users: TwitterUser[];
  };
  meta: {
    result_count: number;
    newest_id?: string;
    oldest_id?: string;
    next_token?: string;
  };
}

// Twitter API service
class TwitterApiService {
  private apiKey: string;
  private apiSecret: string;
  private bearerToken: string;
  private baseUrl: string = 'https://api.twitter.com/2';
  // Use a more reliable CORS proxy
  private corsProxyUrl: string = 'https://corsproxy.io/?';

  constructor(apiKey: string, apiSecret: string, bearerToken: string) {
    this.apiKey = apiKey;
    this.apiSecret = apiSecret;
    this.bearerToken = bearerToken;
  }

  // Predefined query strings by theme
  public readonly QUERY_THEMES = {
    AI_CONTAINMENT_POLICIES: 'AI export control OR AI model weights OR dual-use AI OR closed-weight AI models',
    BIS_AND_DOC: '(Bureau of Industry and Security OR Department of Commerce) (AI OR semiconductors)',
    CHINA_AI: 'DeepSeek OR (China AI surveillance) OR (China compute restrictions)',
    NVIDIA_CHINA: 'Nvidia (China OR export ban)',
    CHIPS_ACT: 'CHIPS Act OR European Chips Act OR US-Japan AI OR AI alliance OR TSMC export',
    AI_LICENSING: 'validated end-user OR AI compute licensing OR ECCN 4E091',
    AI_COLD_WAR: 'AI Cold War OR AI containment OR AGI risk OR AI national security',
    AI_SOVEREIGNTY: 'AI sovereignty (infrastructure OR model weights OR semiconductors)',
    OPENAI_SECURITY: '(OpenAI OR Anthropic) (national security OR AGI OR frontier models)'
  };

  // Search recent tweets
  async searchRecentTweets(
    query: string,
    maxResults: number = 10,
    nextToken?: string
  ): Promise<TwitterApiResponse> {
    try {
      if (!this.bearerToken) {
        throw new Error('Twitter API bearer token is not configured. Please set REACT_APP_TWITTER_BEARER_TOKEN in your environment variables.');
      }

      console.log('Twitter API called with:');
      console.log('- query:', query);
      console.log('- maxResults:', maxResults);
      console.log('- nextToken:', nextToken);
      console.log('- Bearer Token:', this.bearerToken ? 'Bearer token is set' : 'Bearer token is NOT set');
      // Don't log the actual bearer token value for security reasons
      
      // Build the Twitter API URL with parameters
      let twitterApiUrl = `${this.baseUrl}/tweets/search/recent?query=${encodeURIComponent(query)}&max_results=${maxResults}&tweet.fields=created_at,public_metrics,entities&expansions=author_id&user.fields=name,username,profile_image_url`;
      
      if (nextToken) {
        twitterApiUrl += `&next_token=${nextToken}`;
      }
      
      // Create headers for the Twitter API request
      const headers = {
        'Authorization': `Bearer ${this.bearerToken}`
      };
      
      console.log('Twitter API headers:', headers);
      console.log('Twitter bearer token length:', this.bearerToken.length);
      
      // For debugging, log a truncated version of the token
      if (this.bearerToken.length > 10) {
        console.log('Token starts with:', this.bearerToken.substring(0, 5) + '...' + this.bearerToken.substring(this.bearerToken.length - 5));
      }
      
      // Use the CORS proxy to make the request
      const proxyUrl = `${this.corsProxyUrl}${twitterApiUrl}`;
      console.log('Making API call via CORS proxy:', proxyUrl);
      
      // Use retry with backoff for API requests
      const response = await errorHandling.retryWithBackoff(
        () => axios.get(proxyUrl, { 
          headers: {
            ...headers
            // corsproxy.io doesn't require special headers
          }
        }),
        3, // max retries
        1000 // initial delay
      );
      
      console.log('Proxy response status:', response.status);
      
      // Get the response data
      const twitterApiResponse = response.data;
      
      console.log('Twitter API response:', twitterApiResponse);
      
      return twitterApiResponse;
    } catch (error) {
      // Use standardized error handling
      const errorResponse = errorHandling.handleApiError(
        error, 
        'Failed to fetch Twitter data. Please try again later.'
      );
      
      console.error('Twitter API error:', errorResponse);
      
      // Rethrow with standardized error message
      throw new Error(errorResponse.message);
    }
  }

  // Transform Twitter tweets to PerceptionData format
  transformToPerceptionData(tweets: TwitterTweet[], users: TwitterUser[]): PerceptionData[] {
    return tweets.map(tweet => {
      // Find the author of the tweet
      const author = users.find(user => user.id === tweet.author_id);
      
      // Extract hashtags from entities
      const hashtags = tweet.entities?.hashtags?.map(hashtag => hashtag.tag) || [];
      
      // Use shared text analysis utilities
      const actors = textAnalysis.extractActors(tweet.text);
      const technologies = textAnalysis.extractTechnologies(tweet.text);
      const regions = textAnalysis.extractRegions(tweet.text);
      const narrativeTropes = textAnalysis.extractNarrativeTropes(tweet.text);
      const sentiment = textAnalysis.calculateSimpleSentiment(tweet.text);
      
      return {
        source: author?.name || 'Unknown Twitter User',
        sourceType: 'social',
        date: tweet.created_at,
        content: tweet.text,
        narrativeTropes,
        sentiment,
        affectCategory: textAnalysis.getSentimentCategory(sentiment),
        regions,
        actors,
        technologies,
        keywords: [...hashtags, ...textAnalysis.extractKeywords(tweet.text)],
        url: `https://twitter.com/${author?.username}/status/${tweet.id}`,
        language: 'en', // Assuming English based on the API call
        addedBy: 'system',
        addedOn: new Date().toISOString(),
        verified: true
      };
    });
  }

  // These methods are now provided by the shared textAnalysis utility
}

// Create and export the service instance
// Load API keys from environment variables
const apiKey = process.env.REACT_APP_TWITTER_API_KEY;
const apiSecret = process.env.REACT_APP_TWITTER_API_SECRET;
const bearerToken = process.env.REACT_APP_TWITTER_BEARER_TOKEN;

// Check if API keys are properly configured
if (!apiKey || !apiSecret || !bearerToken) {
  console.error('Twitter API credentials not properly configured in environment variables.');
  console.error('Please ensure REACT_APP_TWITTER_API_KEY, REACT_APP_TWITTER_API_SECRET, and REACT_APP_TWITTER_BEARER_TOKEN are set.');
}

const twitterApiService = new TwitterApiService(
  apiKey || '',
  apiSecret || '',
  bearerToken || ''
);

// Log API key status without exposing actual values
console.log('Twitter API keys status:');
console.log('- API Key:', apiKey ? 'Set' : 'Not set');
console.log('- API Secret:', apiSecret ? 'Set' : 'Not set');
console.log('- Bearer Token:', bearerToken ? 'Set' : 'Not set');

export default twitterApiService;
