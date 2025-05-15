/**
 * Error Handling and Utility Functions
 * 
 * This file contains shared utilities for error handling and data formatting across the application.
 */

import axios from 'axios';

/**
 * Standard error response format
 */
export interface ErrorResponse {
  message: string;
  code?: string;
  details?: any;
  timestamp: string;
}

/**
 * Create a standardized error response
 * @param message Error message
 * @param code Error code
 * @param details Additional error details
 * @returns Standardized error response object
 */
export const createErrorResponse = (
  message: string,
  code?: string,
  details?: any
): ErrorResponse => {
  return {
    message,
    code,
    details,
    timestamp: new Date().toISOString()
  };
};

/**
 * Handle API errors in a consistent way
 * @param error The error object
 * @param defaultMessage Default message to show if error details can't be extracted
 * @returns Standardized error response
 */
export const handleApiError = (
  error: any,
  defaultMessage: string = 'An error occurred while fetching data'
): ErrorResponse => {
  console.error('API Error:', error);
  
  // Handle Axios errors
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const statusText = error.response?.statusText;
    const responseData = error.response?.data;
    const requestUrl = error.config?.url;
    
    console.error('Axios error details:');
    console.error('- Status:', status);
    console.error('- Status text:', statusText);
    console.error('- Response data:', responseData);
    console.error('- Request URL:', requestUrl);
    
    // Create appropriate error message based on status code
    let message = defaultMessage;
    let code = 'API_ERROR';
    
    if (status === 401 || status === 403) {
      message = 'Authentication error. Please check your API credentials.';
      code = 'AUTH_ERROR';
    } else if (status === 404) {
      message = 'The requested resource was not found.';
      code = 'NOT_FOUND';
    } else if (status === 429) {
      message = 'Rate limit exceeded. Please try again later.';
      code = 'RATE_LIMIT';
    } else if (status && status >= 500) {
      message = 'Server error. Please try again later.';
      code = 'SERVER_ERROR';
    }
    
    return createErrorResponse(message, code, {
      status,
      statusText,
      responseData,
      requestUrl
    });
  }
  
  // Handle other types of errors
  if (error instanceof Error) {
    return createErrorResponse(
      error.message || defaultMessage,
      'UNKNOWN_ERROR',
      { stack: error.stack }
    );
  }
  
  // Handle unknown errors
  return createErrorResponse(
    defaultMessage,
    'UNKNOWN_ERROR',
    { originalError: error }
  );
};

/**
 * Retry a function with exponential backoff
 * @param fn The function to retry
 * @param maxRetries Maximum number of retries
 * @param initialDelay Initial delay in milliseconds
 * @returns Promise that resolves with the function result or rejects after all retries
 */
export const retryWithBackoff = async <T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  initialDelay: number = 1000
): Promise<T> => {
  let lastError: any;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      console.log(`Attempt ${i + 1} failed, retrying...`);
      lastError = error;
      
      // Wait with exponential backoff before retrying
      const delay = initialDelay * Math.pow(2, i);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError;
};

/**
 * Safely format a date string
 * @param dateString The date string to format
 * @param fallback Fallback string to return if date is invalid
 * @returns Formatted date string or fallback
 */
export const formatDate = (dateString: string | undefined | null, fallback: string = 'Unknown date'): string => {
  if (!dateString) return fallback;
  
  try {
    // Try to parse the date
    const date = new Date(dateString);
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
      return fallback;
    }
    
    // Format the date
    return date.toLocaleDateString();
  } catch (error) {
    console.error('Error formatting date:', error);
    return fallback;
  }
};

/**
 * Safely check if a date string is valid
 * @param dateString The date string to check
 * @returns Boolean indicating if the date is valid
 */
export const isValidDate = (dateString: string | undefined | null): boolean => {
  if (!dateString) return false;
  
  try {
    const date = new Date(dateString);
    return !isNaN(date.getTime());
  } catch (error) {
    return false;
  }
};
