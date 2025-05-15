import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { PerceptionData } from '../services/newsApi';

// Define the state shape
interface AppState {
  // User preferences
  theme: 'light' | 'dark';
  
  // Data state
  newsData: PerceptionData[];
  twitterData: PerceptionData[];
  isLoading: {
    news: boolean;
    twitter: boolean;
  };
  errors: {
    news: string | null;
    twitter: string | null;
  };
  
  // Filters
  filters: {
    dateRange: {
      start: string;
      end: string;
    };
    selectedRegions: string[];
    selectedActors: string[];
    selectedTechnologies: string[];
    selectedLens: string;
    selectedTags: string[];
    dataSource: 'all' | 'news' | 'twitter';
    sortBy: 'recent' | 'relevance' | 'sentiment';
  };
}

// Define action types
type ActionType = 
  | { type: 'SET_THEME'; payload: 'light' | 'dark' }
  | { type: 'SET_NEWS_DATA'; payload: PerceptionData[] }
  | { type: 'SET_TWITTER_DATA'; payload: PerceptionData[] }
  | { type: 'SET_LOADING'; payload: { key: 'news' | 'twitter'; value: boolean } }
  | { type: 'SET_ERROR'; payload: { key: 'news' | 'twitter'; value: string | null } }
  | { type: 'SET_DATE_RANGE'; payload: { start: string; end: string } }
  | { type: 'SET_SELECTED_REGIONS'; payload: string[] }
  | { type: 'SET_SELECTED_ACTORS'; payload: string[] }
  | { type: 'SET_SELECTED_TECHNOLOGIES'; payload: string[] }
  | { type: 'SET_SELECTED_LENS'; payload: string }
  | { type: 'SET_SELECTED_TAGS'; payload: string[] }
  | { type: 'SET_DATA_SOURCE'; payload: 'all' | 'news' | 'twitter' }
  | { type: 'SET_SORT_BY'; payload: 'recent' | 'relevance' | 'sentiment' }
  | { type: 'RESET_FILTERS' };

// Initial state
const initialState: AppState = {
  theme: 'light',
  newsData: [],
  twitterData: [],
  isLoading: {
    news: false,
    twitter: false
  },
  errors: {
    news: null,
    twitter: null
  },
  filters: {
    dateRange: {
      start: '',
      end: ''
    },
    selectedRegions: [],
    selectedActors: [],
    selectedTechnologies: [],
    selectedLens: '',
    selectedTags: [],
    dataSource: 'all',
    sortBy: 'recent'
  }
};

// Create context
const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<ActionType>;
}>({
  state: initialState,
  dispatch: () => null
});

// Reducer function
const appReducer = (state: AppState, action: ActionType): AppState => {
  switch (action.type) {
    case 'SET_THEME':
      return {
        ...state,
        theme: action.payload
      };
    case 'SET_NEWS_DATA':
      return {
        ...state,
        newsData: action.payload
      };
    case 'SET_TWITTER_DATA':
      return {
        ...state,
        twitterData: action.payload
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: {
          ...state.isLoading,
          [action.payload.key]: action.payload.value
        }
      };
    case 'SET_ERROR':
      return {
        ...state,
        errors: {
          ...state.errors,
          [action.payload.key]: action.payload.value
        }
      };
    case 'SET_DATE_RANGE':
      return {
        ...state,
        filters: {
          ...state.filters,
          dateRange: action.payload
        }
      };
    case 'SET_SELECTED_REGIONS':
      return {
        ...state,
        filters: {
          ...state.filters,
          selectedRegions: action.payload
        }
      };
    case 'SET_SELECTED_ACTORS':
      return {
        ...state,
        filters: {
          ...state.filters,
          selectedActors: action.payload
        }
      };
    case 'SET_SELECTED_TECHNOLOGIES':
      return {
        ...state,
        filters: {
          ...state.filters,
          selectedTechnologies: action.payload
        }
      };
    case 'SET_SELECTED_LENS':
      return {
        ...state,
        filters: {
          ...state.filters,
          selectedLens: action.payload
        }
      };
    case 'SET_SELECTED_TAGS':
      return {
        ...state,
        filters: {
          ...state.filters,
          selectedTags: action.payload
        }
      };
    case 'SET_DATA_SOURCE':
      return {
        ...state,
        filters: {
          ...state.filters,
          dataSource: action.payload
        }
      };
    case 'SET_SORT_BY':
      return {
        ...state,
        filters: {
          ...state.filters,
          sortBy: action.payload
        }
      };
    case 'RESET_FILTERS':
      return {
        ...state,
        filters: initialState.filters
      };
    default:
      return state;
  }
};

// Provider component
interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook for using the context
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
