import { useMemo, useCallback } from 'react';
import { PerceptionData } from '../services/newsApi';

/**
 * Custom hook for memoizing expensive calculations related to perception data
 * @param data The perception data to analyze
 * @returns Memoized values and functions
 */
export const useMemoization = (data: PerceptionData[]) => {
  // Memoize unique regions
  const uniqueRegions = useMemo(() => {
    const regions = new Set<string>();
    
    data.forEach(item => {
      item.regions.forEach(region => regions.add(region));
    });
    
    return Array.from(regions).sort();
  }, [data]);
  
  // Memoize unique actors
  const uniqueActors = useMemo(() => {
    const actors = new Set<string>();
    
    data.forEach(item => {
      item.actors.forEach(actor => actors.add(actor));
    });
    
    return Array.from(actors).sort();
  }, [data]);
  
  // Memoize unique technologies
  const uniqueTechnologies = useMemo(() => {
    const technologies = new Set<string>();
    
    data.forEach(item => {
      item.technologies.forEach(tech => technologies.add(tech));
    });
    
    return Array.from(technologies).sort();
  }, [data]);
  
  // Memoize unique keywords/tags
  const uniqueTags = useMemo(() => {
    const tags = new Set<string>();
    
    data.forEach(item => {
      item.keywords.forEach(keyword => tags.add(keyword));
    });
    
    return Array.from(tags).sort();
  }, [data]);
  
  // Memoize sentiment distribution
  const sentimentDistribution = useMemo(() => {
    const distribution = {
      positive: 0,
      neutral: 0,
      negative: 0
    };
    
    data.forEach(item => {
      if (item.sentiment > 0.3) {
        distribution.positive++;
      } else if (item.sentiment < -0.3) {
        distribution.negative++;
      } else {
        distribution.neutral++;
      }
    });
    
    return distribution;
  }, [data]);
  
  // Memoize region distribution
  const regionDistribution = useMemo(() => {
    const distribution: Record<string, number> = {};
    
    uniqueRegions.forEach(region => {
      distribution[region] = 0;
    });
    
    data.forEach(item => {
      item.regions.forEach(region => {
        distribution[region] = (distribution[region] || 0) + 1;
      });
    });
    
    return distribution;
  }, [data, uniqueRegions]);
  
  // Memoize actor distribution
  const actorDistribution = useMemo(() => {
    const distribution: Record<string, number> = {};
    
    uniqueActors.forEach(actor => {
      distribution[actor] = 0;
    });
    
    data.forEach(item => {
      item.actors.forEach(actor => {
        distribution[actor] = (distribution[actor] || 0) + 1;
      });
    });
    
    return distribution;
  }, [data, uniqueActors]);
  
  // Memoize technology distribution
  const technologyDistribution = useMemo(() => {
    const distribution: Record<string, number> = {};
    
    uniqueTechnologies.forEach(tech => {
      distribution[tech] = 0;
    });
    
    data.forEach(item => {
      item.technologies.forEach(tech => {
        distribution[tech] = (distribution[tech] || 0) + 1;
      });
    });
    
    return distribution;
  }, [data, uniqueTechnologies]);
  
  // Memoize tag distribution
  const tagDistribution = useMemo(() => {
    const distribution: Record<string, number> = {};
    
    uniqueTags.forEach(tag => {
      distribution[tag] = 0;
    });
    
    data.forEach(item => {
      item.keywords.forEach(keyword => {
        distribution[keyword] = (distribution[keyword] || 0) + 1;
      });
    });
    
    return distribution;
  }, [data, uniqueTags]);
  
  // Memoize top tags
  const topTags = useMemo(() => {
    return Object.entries(tagDistribution)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([tag, count]) => ({ tag, count }));
  }, [tagDistribution]);
  
  // Memoize top actors
  const topActors = useMemo(() => {
    return Object.entries(actorDistribution)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([actor, count]) => ({ actor, count }));
  }, [actorDistribution]);
  
  // Memoize sentiment over time
  const sentimentOverTime = useMemo(() => {
    // Group data by date (YYYY-MM-DD)
    const dateGroups: Record<string, PerceptionData[]> = {};
    
    data.forEach(item => {
      const date = new Date(item.date).toISOString().split('T')[0];
      if (!dateGroups[date]) {
        dateGroups[date] = [];
      }
      dateGroups[date].push(item);
    });
    
    // Calculate average sentiment for each date
    const result = Object.entries(dateGroups).map(([date, items]) => {
      const totalSentiment = items.reduce((sum, item) => sum + item.sentiment, 0);
      const averageSentiment = totalSentiment / items.length;
      
      return {
        date,
        sentiment: averageSentiment,
        count: items.length
      };
    });
    
    // Sort by date
    return result.sort((a, b) => a.date.localeCompare(b.date));
  }, [data]);
  
  // Memoized function to get co-occurrence matrix
  const getCoOccurrenceMatrix = useCallback((type: 'actors' | 'technologies' | 'regions') => {
    const items = type === 'actors' 
      ? uniqueActors 
      : type === 'technologies' 
        ? uniqueTechnologies 
        : uniqueRegions;
    
    // Initialize matrix
    const matrix: Record<string, Record<string, number>> = {};
    items.forEach(item1 => {
      matrix[item1] = {};
      items.forEach(item2 => {
        matrix[item1][item2] = 0;
      });
    });
    
    // Fill matrix
    data.forEach(item => {
      const elements = type === 'actors' 
        ? item.actors 
        : type === 'technologies' 
          ? item.technologies 
          : item.regions;
      
      // Count co-occurrences
      for (let i = 0; i < elements.length; i++) {
        for (let j = 0; j < elements.length; j++) {
          if (i !== j) {
            matrix[elements[i]][elements[j]]++;
          }
        }
      }
    });
    
    return matrix;
  }, [data, uniqueActors, uniqueRegions, uniqueTechnologies]);
  
  return {
    uniqueRegions,
    uniqueActors,
    uniqueTechnologies,
    uniqueTags,
    sentimentDistribution,
    regionDistribution,
    actorDistribution,
    technologyDistribution,
    tagDistribution,
    topTags,
    topActors,
    sentimentOverTime,
    getCoOccurrenceMatrix
  };
};
