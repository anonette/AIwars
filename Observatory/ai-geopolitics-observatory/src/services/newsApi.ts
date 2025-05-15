import axios from 'axios';
import * as textAnalysis from '../utils/textAnalysis';
import * as errorHandling from '../utils/errorHandling';

// Types for SerpAPI Google News responses
export interface NewsArticle {
  source: {
    id: string | null;
    name: string;
  };
  author: string | null;
  title: string;
  description: string;
  url: string;
  urlToImage: string | null;
  publishedAt: string;
  content: string;
}

export interface NewsApiResponse {
  status: string;
  totalResults: number;
  articles: NewsArticle[];
}

// Transform SerpAPI article to our PerceptionData format
export interface PerceptionData {
  source: string;
  sourceType: 'media' | 'social' | 'academic' | 'policy';
  date: string;
  content: string;
  narrativeTropes: string[];
  sentiment: number;
  affectCategory: string;
  regions: string[];
  actors: string[];
  technologies: string[];
  keywords: string[];
  url: string;
  language: string;
  addedBy: string;
  addedOn: string;
  verified: boolean;
}

// SerpAPI Google News service
class NewsApiService {
  private apiKey: string;
  private baseUrl: string = 'https://serpapi.com';
  private corsProxyUrl: string = 'https://api.allorigins.win/get?url=';

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  // Predefined query strings by theme
  public readonly QUERY_THEMES = {
    AI_CONTAINMENT_POLICIES: 'AI export control" OR "AI model weights" OR "dual-use AI" OR "closed-weight AI models',
    BIS_AND_DOC: '("Bureau of Industry and Security" OR "Department of Commerce") AND ("AI" OR "semiconductors")',
    CHINA_AI: '"DeepSeek" OR ("China" AND "AI surveillance") OR ("China" AND "compute restrictions")',
    NVIDIA_CHINA: '"Nvidia" AND ("China" OR "export ban")',
    CHIPS_ACT: '"CHIPS Act" OR "European Chips Act" OR "US-Japan AI" OR "AI alliance" OR "TSMC export"',
    AI_LICENSING: '"validated end-user" OR "AI compute licensing" OR "ECCN 4E091"',
    AI_COLD_WAR: '"AI Cold War" OR "AI containment" OR "AGI risk" OR "AI national security"',
    AI_SOVEREIGNTY: '"AI sovereignty" AND ("infrastructure" OR "model weights" OR "semiconductors")',
    OPENAI_SECURITY: '("OpenAI" OR "Anthropic") AND ("national security" OR "AGI" OR "frontier models")'
  };

  // Get everything endpoint using SerpAPI Google News
  async getEverything(
    query: string,
    fromDate?: string,
    toDate?: string,
    language: string = 'en',
    sortBy: 'relevancy' | 'popularity' | 'publishedAt' = 'publishedAt',
    pageSize: number = 10,
    page: number = 1
  ): Promise<NewsApiResponse> {
    try {
      if (!this.apiKey) {
        throw new Error('News API key is not configured. Please set REACT_APP_SERP_API_KEY or REACT_APP_NEWS_API_KEY in your environment variables.');
      }

      console.log('SerpAPI Google News called with:');
      console.log('- query:', query);
      console.log('- fromDate:', fromDate);
      console.log('- toDate:', toDate);
      console.log('- language:', language);
      console.log('- sortBy:', sortBy);
      console.log('- pageSize:', pageSize);
      console.log('- page:', page);
      console.log('- API Key:', this.apiKey ? 'API key is set' : 'API key is NOT set');
      
      // Convert date format if provided (YYYY-MM-DD to timestamp if needed)
      let timeRange;
      if (fromDate && toDate) {
        timeRange = 'custom';
      }

      // Build the SerpAPI URL with parameters
      let serpApiUrl = `${this.baseUrl}/search?api_key=${this.apiKey}&q=${encodeURIComponent(query)}&tbm=nws&num=${pageSize}&start=${(page - 1) * pageSize}&gl=${language === 'en' ? 'us' : language}`;
      
      // Add time range parameters if provided
      if (timeRange) {
        serpApiUrl += '&tbs=cdr:1';
        if (fromDate) serpApiUrl += `&cd_min=${fromDate}`;
        if (toDate) serpApiUrl += `&cd_max=${toDate}`;
      }

      // Encode the SerpAPI URL for the CORS proxy
      const proxyUrl = `${this.corsProxyUrl}${encodeURIComponent(serpApiUrl)}`;
      
      console.log('Request URL (via proxy):', proxyUrl);
      
      // Use retry with backoff for API requests
      const response = await errorHandling.retryWithBackoff(
        () => axios.get(proxyUrl),
        3, // max retries
        1000 // initial delay
      );

      console.log('Proxy response status:', response.status);
      
      // Parse the response content from the proxy
      let serpApiResponse;
      if (response.data && response.data.contents) {
        serpApiResponse = JSON.parse(response.data.contents);
      } else {
        throw new Error('Invalid response from proxy');
      }
      
      // Transform SerpAPI response to match our expected format
      const transformedResponse: NewsApiResponse = {
        status: 'ok',
        totalResults: serpApiResponse.news_results?.length || 0,
        articles: this.transformSerpApiToArticles(serpApiResponse.news_results || [])
      };
      
      console.log('Transformed response:', transformedResponse);
      
      return transformedResponse;
    } catch (error) {
      // Use standardized error handling
      const errorResponse = errorHandling.handleApiError(
        error, 
        'Failed to fetch news data. Please try again later.'
      );
      
      console.error('News API error:', errorResponse);
      
      // Return an empty response instead of throwing to prevent UI crashes
      return {
        status: 'error',
        totalResults: 0,
        articles: []
      };
    }
  }

  // Transform SerpAPI news results to our NewsArticle format
  private transformSerpApiToArticles(newsResults: any[]): NewsArticle[] {
    return newsResults.map(result => ({
      source: {
        id: null,
        name: result.source || 'Unknown Source'
      },
      author: result.author || null,
      title: result.title || '',
      description: result.snippet || '',
      url: result.link || '',
      urlToImage: result.thumbnail || null,
      publishedAt: result.date || new Date().toISOString(),
      content: result.snippet || ''
    }));
  }

  // Transform NewsAPI articles to PerceptionData format
  transformToPerceptionData(articles: NewsArticle[]): PerceptionData[] {
    return articles.map(article => {
      try {
        // Extract potential actors, technologies, and regions from title and description
        const combinedText = `${article.title} ${article.description}`;
        
        // Use shared text analysis utilities
        const actors = textAnalysis.extractActors(combinedText);
        const technologies = textAnalysis.extractTechnologies(combinedText);
        const regions = textAnalysis.extractRegions(combinedText);
        const narrativeTropes = textAnalysis.extractNarrativeTropes(combinedText);
        const sentiment = textAnalysis.calculateSimpleSentiment(combinedText);
        
        // Validate and format the date
        let formattedDate = article.publishedAt;
        if (!errorHandling.isValidDate(formattedDate)) {
          formattedDate = new Date().toISOString();
        }
        
        return {
          source: article.source.name || 'Unknown Source',
          sourceType: 'media',
          date: formattedDate,
          content: article.title + (article.description ? ` - ${article.description}` : ''),
          narrativeTropes: narrativeTropes || [],
          sentiment: isNaN(sentiment) ? 0 : sentiment,
          affectCategory: textAnalysis.getSentimentCategory(sentiment),
          regions: regions || [],
          actors: actors || [],
          technologies: technologies || [],
          keywords: textAnalysis.extractKeywords(combinedText) || [],
          url: article.url || '#',
          language: 'en', // Assuming English based on the API call
          addedBy: 'system',
          addedOn: new Date().toISOString(),
          verified: true
        };
      } catch (error) {
        console.error('Error transforming article to perception data:', error);
        
        // Return a fallback object with default values
        return {
          source: 'Unknown Source',
          sourceType: 'media',
          date: new Date().toISOString(),
          content: 'Error processing content',
          narrativeTropes: [],
          sentiment: 0,
          affectCategory: 'neutral',
          regions: [],
          actors: [],
          technologies: [],
          keywords: [],
          url: '#',
          language: 'en',
          addedBy: 'system',
          addedOn: new Date().toISOString(),
          verified: false
        };
      }
    });
  }
}

// Create and export the service instance
// Get API key from environment variables
const apiKey = process.env.REACT_APP_SERP_API_KEY || process.env.REACT_APP_NEWS_API_KEY;

// Check if API key is properly configured
if (!apiKey) {
  console.error('News API credentials not properly configured in environment variables.');
  console.error('Please ensure REACT_APP_SERP_API_KEY or REACT_APP_NEWS_API_KEY is set.');
}

const newsApiService = new NewsApiService(apiKey || '');

// Log API key status without exposing actual values
console.log('News API key status:', apiKey ? 'Set' : 'Not set');

export default newsApiService;
