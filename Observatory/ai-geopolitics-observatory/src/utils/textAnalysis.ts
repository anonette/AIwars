/**
 * Text Analysis Utilities
 * 
 * This file contains shared utilities for text analysis used across the application,
 * particularly for extracting entities and performing sentiment analysis on text data.
 */

/**
 * Extract actor entities from text
 * @param text The text to analyze
 * @returns Array of actor names found in the text
 */
export const extractActors = (text: string): string[] => {
  const actorKeywords = [
    'China', 'US', 'United States', 'EU', 'European Union', 
    'Nvidia', 'OpenAI', 'Anthropic', 'DeepSeek', 'Google', 
    'Microsoft', 'Meta', 'Bureau of Industry and Security', 
    'Department of Commerce', 'TSMC'
  ];
  
  return actorKeywords.filter(actor => 
    text.toLowerCase().includes(actor.toLowerCase())
  );
};

/**
 * Extract technology entities from text
 * @param text The text to analyze
 * @returns Array of technology terms found in the text
 */
export const extractTechnologies = (text: string): string[] => {
  const techKeywords = [
    'AI', 'artificial intelligence', 'semiconductors', 'chips', 
    'compute', 'model weights', 'AGI', 'frontier models', 
    'large language models', 'LLM', 'GPU', 'TPU'
  ];
  
  return techKeywords.filter(tech => 
    text.toLowerCase().includes(tech.toLowerCase())
  );
};

/**
 * Extract region entities from text
 * @param text The text to analyze
 * @returns Array of region names found in the text
 */
export const extractRegions = (text: string): string[] => {
  const regionKeywords = [
    'China', 'US', 'United States', 'Europe', 'EU', 'Japan', 
    'South Korea', 'Taiwan', 'Asia', 'North America', 'Africa', 
    'Middle East', 'Latin America'
  ];
  
  return regionKeywords.filter(region => 
    text.toLowerCase().includes(region.toLowerCase())
  );
};

/**
 * Extract narrative tropes from text
 * @param text The text to analyze
 * @returns Array of narrative tropes found in the text
 */
export const extractNarrativeTropes = (text: string): string[] => {
  const tropeKeywords = [
    'AI Cold War', 'containment', 'national security', 'sovereignty', 
    'export control', 'dual-use', 'risk', 'safety', 'competition', 
    'alliance', 'regulation', 'restriction', 'ban'
  ];
  
  return tropeKeywords.filter(trope => 
    text.toLowerCase().includes(trope.toLowerCase())
  );
};

/**
 * Extract keywords from text
 * @param text The text to analyze
 * @returns Array of keywords extracted from the text
 */
export const extractKeywords = (text: string): string[] => {
  // In a real app, this would use a keyword extraction algorithm
  // For now, just split by spaces and take unique words longer than 4 chars
  const words = text.toLowerCase()
    .replace(/[^\w\s]/g, '')
    .split(/\s+/)
    .filter(word => word.length > 4);
  
  return Array.from(new Set(words)).slice(0, 10);
};

/**
 * Calculate sentiment score for text
 * @param text The text to analyze
 * @returns Sentiment score between -1 (negative) and 1 (positive)
 */
export const calculateSimpleSentiment = (text: string): number => {
  // Very simple sentiment analysis
  // In a real app, you'd use a proper NLP library
  const positiveWords = [
    'good', 'great', 'excellent', 'positive', 'advance', 'benefit', 
    'progress', 'success', 'innovation', 'cooperation', 'collaborate'
  ];
  
  const negativeWords = [
    'bad', 'poor', 'negative', 'risk', 'threat', 'danger', 'concern', 
    'fear', 'restrict', 'ban', 'control', 'conflict', 'war', 'tension'
  ];
  
  let score = 0;
  const lowerText = text.toLowerCase();
  
  positiveWords.forEach(word => {
    if (lowerText.includes(word)) score += 0.1;
  });
  
  negativeWords.forEach(word => {
    if (lowerText.includes(word)) score -= 0.1;
  });
  
  // Clamp between -1 and 1
  return Math.max(-1, Math.min(1, score));
};

/**
 * Get sentiment category based on score
 * @param sentiment Sentiment score between -1 and 1
 * @returns Category label: 'positive', 'negative', or 'neutral'
 */
export const getSentimentCategory = (sentiment: number): string => {
  if (sentiment > 0.3) return 'positive';
  if (sentiment < -0.3) return 'negative';
  return 'neutral';
};
