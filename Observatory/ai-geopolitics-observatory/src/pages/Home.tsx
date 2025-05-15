import React from 'react';
import Layout from '../components/common/Layout';

const Home: React.FC = () => {
  return (
    <Layout>
      <div className="home-page">
        <section className="hero-section">
          <h1>Public Observatory of AI Geopolitics</h1>
          <p className="subtitle">
            Tracking perceptions, signals, and policies in the global AI landscape
          </p>
        </section>

        <section className="featured-visualization">
          <h2>Featured Visualization</h2>
          <div className="visualization-placeholder">
            <p>Interactive visualization showing current hot topic</p>
            {/* This will be replaced with actual visualization component */}
          </div>
        </section>

        <div className="home-grid">
          <section className="latest-signals">
            <h2>Latest Signals</h2>
            <ul className="signals-list">
              <li className="signal-item">
                <h3>Signal Title 1</h3>
                <p className="meta">Contributor name, date</p>
              </li>
              <li className="signal-item">
                <h3>Signal Title 2</h3>
                <p className="meta">Contributor name, date</p>
              </li>
              <li className="signal-item">
                <h3>Signal Title 3</h3>
                <p className="meta">Contributor name, date</p>
              </li>
            </ul>
          </section>

          <section className="key-metrics">
            <h2>Key Metrics</h2>
            <ul className="metrics-list">
              <li>Total narratives tracked: XX</li>
              <li>Active regions: XX</li>
              <li>Trending topics: XXXX, YYYY</li>
              <li>New signals this week: XX</li>
            </ul>
          </section>

          <section className="recent-timeline">
            <h2>Recent Timeline Events</h2>
            <ul className="timeline-list">
              <li className="timeline-item">
                <h3>Event Title 1</h3>
                <p className="meta">Date, type</p>
              </li>
              <li className="timeline-item">
                <h3>Event Title 2</h3>
                <p className="meta">Date, type</p>
              </li>
              <li className="timeline-item">
                <h3>Event Title 3</h3>
                <p className="meta">Date, type</p>
              </li>
            </ul>
          </section>
        </div>
      </div>
    </Layout>
  );
};

export default Home;