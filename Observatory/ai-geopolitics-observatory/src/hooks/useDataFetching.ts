import { useEffect, useCallback } from 'react';
import { useAppContext } from '../context/AppContext';
import newsApiService, { PerceptionData } from '../services/newsApi';
import twitterApiService from '../services/twitterApi';
import * as errorHandling from '../utils/errorHandling';

/**
 * Custom hook for fetching data from News API and Twitter API
 * @param initialFetch Whether to fetch data on mount
 * @returns Object with data, loading states, error states, and fetch functions
 */
export const useDataFetching = (initialFetch: boolean = true) => {
  const { state, dispatch } = useAppContext();
  const { filters } = state;

  // Fetch news data
  const fetchNewsData = useCallback(async () => {
    try {
      dispatch({ 
        type: 'SET_LOADING', 
        payload: { key: 'news', value: true } 
      });
      
      dispatch({ 
        type: 'SET_ERROR', 
        payload: { key: 'news', value: null } 
      });

      // Determine query based on selected lens or tags
      let query = '';
      
      if (filters.selectedLens === 'security') {
        query = newsApiService.QUERY_THEMES.AI_CONTAINMENT_POLICIES;
      } else if (filters.selectedLens === 'industrial') {
        query = newsApiService.QUERY_THEMES.NVIDIA_CHINA;
      } else if (filters.selectedLens === 'ethics') {
        query = newsApiService.QUERY_THEMES.OPENAI_SECURITY;
      } else if (filters.selectedLens === 'legal') {
        query = newsApiService.QUERY_THEMES.BIS_AND_DOC;
      } else {
        query = newsApiService.QUERY_THEMES.AI_COLD_WAR; // Default query
      }
      
      // Fetch news data
      const response = await newsApiService.getEverything(
        query,
        filters.dateRange.start,
        filters.dateRange.end
      );
      
      if (response.status === 'error') {
        throw new Error('Failed to fetch news data');
      }
      
      // Transform to PerceptionData format
      const perceptionData = newsApiService.transformToPerceptionData(response.articles);
      
      // Update state
      dispatch({ type: 'SET_NEWS_DATA', payload: perceptionData });
    } catch (error) {
      const errorResponse = errorHandling.handleApiError(
        error, 
        'Failed to fetch news data. Please try again later.'
      );
      
      dispatch({ 
        type: 'SET_ERROR', 
        payload: { key: 'news', value: errorResponse.message } 
      });
      
      console.error('News API error:', errorResponse);
    } finally {
      dispatch({ 
        type: 'SET_LOADING', 
        payload: { key: 'news', value: false } 
      });
    }
  }, [dispatch, filters.dateRange.end, filters.dateRange.start, filters.selectedLens]);

  // Fetch Twitter data
  const fetchTwitterData = useCallback(async () => {
    try {
      dispatch({ 
        type: 'SET_LOADING', 
        payload: { key: 'twitter', value: true } 
      });
      
      dispatch({ 
        type: 'SET_ERROR', 
        payload: { key: 'twitter', value: null } 
      });

      // Determine query based on selected lens or tags
      let query = '';
      
      if (filters.selectedLens === 'security') {
        query = twitterApiService.QUERY_THEMES.AI_CONTAINMENT_POLICIES;
      } else if (filters.selectedLens === 'industrial') {
        query = twitterApiService.QUERY_THEMES.NVIDIA_CHINA;
      } else if (filters.selectedLens === 'ethics') {
        query = twitterApiService.QUERY_THEMES.OPENAI_SECURITY;
      } else if (filters.selectedLens === 'legal') {
        query = twitterApiService.QUERY_THEMES.BIS_AND_DOC;
      } else {
        query = twitterApiService.QUERY_THEMES.AI_COLD_WAR; // Default query
      }
      
      // Fetch Twitter data
      const response = await twitterApiService.searchRecentTweets(query, 10);
      
      if (!response.data || !response.includes?.users) {
        throw new Error('Invalid Twitter API response');
      }
      
      // Transform to PerceptionData format
      const perceptionData = twitterApiService.transformToPerceptionData(
        response.data, 
        response.includes.users
      );
      
      // Update state
      dispatch({ type: 'SET_TWITTER_DATA', payload: perceptionData });
    } catch (error) {
      const errorResponse = errorHandling.handleApiError(
        error, 
        'Failed to fetch Twitter data. Please try again later.'
      );
      
      dispatch({ 
        type: 'SET_ERROR', 
        payload: { key: 'twitter', value: errorResponse.message } 
      });
      
      console.error('Twitter API error:', errorResponse);
    } finally {
      dispatch({ 
        type: 'SET_LOADING', 
        payload: { key: 'twitter', value: false } 
      });
    }
  }, [dispatch, filters.selectedLens]);

  // Fetch all data
  const fetchAllData = useCallback(async () => {
    await Promise.all([
      fetchNewsData(),
      fetchTwitterData()
    ]);
  }, [fetchNewsData, fetchTwitterData]);

  // Initial fetch
  useEffect(() => {
    if (initialFetch) {
      fetchAllData();
    }
  }, [initialFetch, fetchAllData]);

  // Filter data based on current filters
  const getFilteredData = useCallback((): PerceptionData[] => {
    let filteredData: PerceptionData[] = [];
    
    // Filter by data source
    if (filters.dataSource === 'all' || filters.dataSource === 'news') {
      filteredData = [...filteredData, ...state.newsData];
    }
    
    if (filters.dataSource === 'all' || filters.dataSource === 'twitter') {
      filteredData = [...filteredData, ...state.twitterData];
    }
    
    // Filter by date range
    if (filters.dateRange.start || filters.dateRange.end) {
      filteredData = filteredData.filter(item => {
        const itemDate = new Date(item.date);
        
        if (filters.dateRange.start && filters.dateRange.end) {
          const startDate = new Date(filters.dateRange.start);
          const endDate = new Date(filters.dateRange.end);
          return itemDate >= startDate && itemDate <= endDate;
        } else if (filters.dateRange.start) {
          const startDate = new Date(filters.dateRange.start);
          return itemDate >= startDate;
        } else if (filters.dateRange.end) {
          const endDate = new Date(filters.dateRange.end);
          return itemDate <= endDate;
        }
        
        return true;
      });
    }
    
    // Filter by regions
    if (filters.selectedRegions.length > 0) {
      filteredData = filteredData.filter(item => 
        item.regions.some(region => 
          filters.selectedRegions.includes(region)
        )
      );
    }
    
    // Filter by actors
    if (filters.selectedActors.length > 0) {
      filteredData = filteredData.filter(item => 
        item.actors.some(actor => 
          filters.selectedActors.includes(actor)
        )
      );
    }
    
    // Filter by technologies
    if (filters.selectedTechnologies.length > 0) {
      filteredData = filteredData.filter(item => 
        item.technologies.some(tech => 
          filters.selectedTechnologies.includes(tech)
        )
      );
    }
    
    // Filter by tags
    if (filters.selectedTags.length > 0) {
      filteredData = filteredData.filter(item => 
        item.keywords.some(keyword => 
          filters.selectedTags.includes(keyword)
        )
      );
    }
    
    // Sort data
    if (filters.sortBy === 'recent') {
      filteredData.sort((a, b) => 
        new Date(b.date).getTime() - new Date(a.date).getTime()
      );
    } else if (filters.sortBy === 'sentiment') {
      filteredData.sort((a, b) => b.sentiment - a.sentiment);
    }
    
    return filteredData;
  }, [
    filters.dataSource, 
    filters.dateRange.end, 
    filters.dateRange.start, 
    filters.selectedActors, 
    filters.selectedRegions, 
    filters.selectedTags, 
    filters.selectedTechnologies, 
    filters.sortBy, 
    state.newsData, 
    state.twitterData
  ]);

  return {
    newsData: state.newsData,
    twitterData: state.twitterData,
    filteredData: getFilteredData(),
    isLoading: state.isLoading,
    errors: state.errors,
    fetchNewsData,
    fetchTwitterData,
    fetchAllData
  };
};
