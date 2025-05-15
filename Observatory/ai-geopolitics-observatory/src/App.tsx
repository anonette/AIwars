import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Import styles
import './styles/main.css';

// Lazy load page components for code splitting
const Home = lazy(() => import('./pages/Home'));
const PerceptionTracker = lazy(() => import('./pages/PerceptionTracker'));
const Signals = lazy(() => import('./pages/Signals'));
const Timeline = lazy(() => import('./pages/Timeline'));
const About = lazy(() => import('./pages/About'));

// Loading component for Suspense fallback
const Loading: React.FC = () => (
  <div className="loading-container">
    <div className="loading-spinner"></div>
    <p>Loading...</p>
  </div>
);

const App: React.FC = () => {
  return (
    <Router>
      <Suspense fallback={<Loading />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/perception-tracker" element={<PerceptionTracker />} />
          <Route path="/signals" element={<Signals />} />
          <Route path="/timeline" element={<Timeline />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Suspense>
    </Router>
  );
};

export default App;
