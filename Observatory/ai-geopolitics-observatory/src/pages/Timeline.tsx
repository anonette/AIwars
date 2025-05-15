import React, { useState } from 'react';
import Layout from '../components/common/Layout';

// Interface for Timeline Event data
interface TimelineEvent {
  id: string;
  title: string;
  date: string;
  type: 'Regulation' | 'Corporate' | 'Bloc' | 'Other';
  description: string;
  actors: string[];
  assets: string[];
  containmentLogic: string;
  sources: string[];
}

const Timeline: React.FC = () => {
  // State for filters
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [eventTypes, setEventTypes] = useState<string[]>(['Regulation', 'Corporate', 'Bloc', 'Other']);
  const [selectedActors, setSelectedActors] = useState<string[]>([]);
  const [selectedAssets, setSelectedAssets] = useState<string[]>([]);
  
  // State for selected event
  const [selectedEvent, setSelectedEvent] = useState<TimelineEvent | null>(null);

  // Mock data for timeline events
  const [events] = useState<TimelineEvent[]>([
    {
      id: '1',
      title: 'CHIPS Act Implementation Phase 2',
      date: '2025-03-15',
      type: 'Regulation',
      description: 'The second phase of the CHIPS Act implementation introduces new restrictions on advanced semiconductor exports and establishes additional funding for domestic manufacturing capabilities.',
      actors: ['US Department of Commerce', 'Semiconductor Industry'],
      assets: ['Compute', 'Hardware'],
      containmentLogic: 'National Security, Economic Competition',
      sources: ['Source 1', 'Source 2', 'Source 3']
    },
    {
      id: '2',
      title: 'EU AI Act Enforcement Begins',
      date: '2025-02-20',
      type: 'Regulation',
      description: 'The European Union begins enforcement of the AI Act, requiring compliance with risk-based regulations for AI systems deployed within the EU market.',
      actors: ['European Commission', 'EU Member States'],
      assets: ['Software', 'Data'],
      containmentLogic: 'Consumer Protection, Ethical AI',
      sources: ['Source 1', 'Source 2']
    },
    {
      id: '3',
      title: 'DeepMind-OpenAI Research Collaboration',
      date: '2025-01-10',
      type: 'Corporate',
      description: 'DeepMind and OpenAI announce a joint research initiative focused on AI safety and alignment, sharing resources and research findings.',
      actors: ['DeepMind', 'OpenAI'],
      assets: ['Research', 'Talent'],
      containmentLogic: 'Safety, Competitive Advantage',
      sources: ['Source 1']
    },
    {
      id: '4',
      title: 'China Announces AI Sovereignty Initiative',
      date: '2024-12-05',
      type: 'Bloc',
      description: 'China announces a comprehensive initiative to achieve AI sovereignty, including increased funding for domestic AI research and development.',
      actors: ['Chinese Government', 'Chinese Tech Companies'],
      assets: ['Research', 'Compute', 'Data'],
      containmentLogic: 'National Security, Economic Development',
      sources: ['Source 1', 'Source 2', 'Source 3']
    }
  ]);

  // Handler for filter application
  const handleApplyFilters = () => {
    // This would fetch data based on the selected filters
    console.log('Applying filters:', {
      dateRange,
      eventTypes,
      selectedActors,
      selectedAssets
    });
  };

  // Handler for filter reset
  const handleResetFilters = () => {
    setDateRange({ start: '', end: '' });
    setEventTypes(['Regulation', 'Corporate', 'Bloc', 'Other']);
    setSelectedActors([]);
    setSelectedAssets([]);
  };

  // Handler for event selection
  const handleEventSelect = (event: TimelineEvent) => {
    setSelectedEvent(event);
  };

  return (
    <Layout>
      <div className="timeline-page">
        <div className="page-header">
          <h1>Timeline & Policy Map</h1>
          <button className="btn btn-outline">Export ▼</button>
        </div>

        <div className="filters-section">
          <h2>Filters</h2>
          <div className="filters-content">
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
              <label>Event Type:</label>
              <div className="checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={eventTypes.includes('Regulation')}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setEventTypes([...eventTypes, 'Regulation']);
                      } else {
                        setEventTypes(eventTypes.filter(type => type !== 'Regulation'));
                      }
                    }}
                  />
                  Regulation
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={eventTypes.includes('Corporate')}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setEventTypes([...eventTypes, 'Corporate']);
                      } else {
                        setEventTypes(eventTypes.filter(type => type !== 'Corporate'));
                      }
                    }}
                  />
                  Corporate
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={eventTypes.includes('Bloc')}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setEventTypes([...eventTypes, 'Bloc']);
                      } else {
                        setEventTypes(eventTypes.filter(type => type !== 'Bloc'));
                      }
                    }}
                  />
                  Bloc
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={eventTypes.includes('Other')}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setEventTypes([...eventTypes, 'Other']);
                      } else {
                        setEventTypes(eventTypes.filter(type => type !== 'Other'));
                      }
                    }}
                  />
                  Other
                </label>
              </div>
            </div>

            <div className="filter-group">
              <label>Actors:</label>
              <select
                multiple
                value={selectedActors}
                onChange={(e) => setSelectedActors(Array.from(e.target.selectedOptions, option => option.value))}
              >
                <option value="us-government">US Government</option>
                <option value="eu-commission">European Commission</option>
                <option value="china-government">Chinese Government</option>
                <option value="tech-companies">Tech Companies</option>
                {/* More options would be added here */}
              </select>
            </div>

            <div className="filter-group">
              <label>Assets:</label>
              <select
                multiple
                value={selectedAssets}
                onChange={(e) => setSelectedAssets(Array.from(e.target.selectedOptions, option => option.value))}
              >
                <option value="compute">Compute</option>
                <option value="hardware">Hardware</option>
                <option value="software">Software</option>
                <option value="data">Data</option>
                <option value="research">Research</option>
                {/* More options would be added here */}
              </select>
            </div>

            <div className="filter-actions">
              <button className="btn btn-primary" onClick={handleApplyFilters}>Apply Filters</button>
              <button className="btn btn-outline" onClick={handleResetFilters}>Reset</button>
            </div>
          </div>
        </div>

        <div className="timeline-content">
          <div className="timeline-visualization">
            <div className="timeline-scale">
              <span>2024</span>
              <div className="timeline-line">
                {events.map(event => (
                  <div
                    key={event.id}
                    className={`timeline-marker ${event.type.toLowerCase()} ${selectedEvent?.id === event.id ? 'selected' : ''}`}
                    style={{
                      left: `${calculatePosition(event.date)}%`
                    }}
                    onClick={() => handleEventSelect(event)}
                    title={event.title}
                  />
                ))}
              </div>
              <span>2025</span>
            </div>
          </div>

          {selectedEvent && (
            <div className="event-details">
              <h2>{selectedEvent.title}</h2>
              <div className="event-meta">
                <span className="date">Date: {selectedEvent.date}</span>
                <span className={`type ${selectedEvent.type.toLowerCase()}`}>Type: {selectedEvent.type}</span>
              </div>
              
              <div className="event-description">
                <h3>Description:</h3>
                <p>{selectedEvent.description}</p>
              </div>
              
              <div className="event-actors">
                <h3>Actors:</h3>
                <ul>
                  {selectedEvent.actors.map((actor, index) => (
                    <li key={index}>{actor}</li>
                  ))}
                </ul>
              </div>
              
              <div className="event-assets">
                <h3>Assets:</h3>
                <ul>
                  {selectedEvent.assets.map((asset, index) => (
                    <li key={index}>{asset}</li>
                  ))}
                </ul>
              </div>
              
              <div className="event-containment">
                <h3>Containment Logic:</h3>
                <p>{selectedEvent.containmentLogic}</p>
              </div>
              
              <div className="event-sources">
                <h3>Sources:</h3>
                <ul>
                  {selectedEvent.sources.map((source, index) => (
                    <li key={index}><button className="link-button">{source}</button></li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          <div className="related-content">
            <h2>Related Content</h2>
            <div className="related-content-columns">
              <div className="related-signals">
                <h3>Related Signals</h3>
                <ul>
                  <li><button className="link-button">Signal 1</button></li>
                  <li><button className="link-button">Signal 2</button></li>
                </ul>
              </div>
              
              <div className="related-perception">
                <h3>Perception Data</h3>
                <div className="perception-visualization-placeholder">
                  <p>Small visualization of related perception data</p>
                </div>
                <button className="btn btn-outline">View all related data</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

// Helper function to calculate position on timeline
const calculatePosition = (dateString: string): number => {
  const date = new Date(dateString);
  const start = new Date('2024-01-01');
  const end = new Date('2025-12-31');
  
  const totalDays = (end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);
  const daysSinceStart = (date.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);
  
  return (daysSinceStart / totalDays) * 100;
};

export default Timeline;