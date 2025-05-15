import React from 'react';
import { NavLink } from 'react-router-dom';

const Navigation: React.FC = () => {
  return (
    <nav className="main-navigation">
      <div className="container">
        <ul className="nav-list">
          <li className="nav-item">
            <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>
              Home
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/perception-tracker" className={({ isActive }) => isActive ? 'active' : ''}>
              Perception Tracker
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/signals" className={({ isActive }) => isActive ? 'active' : ''}>
              Signals
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/timeline" className={({ isActive }) => isActive ? 'active' : ''}>
              Timeline
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/about" className={({ isActive }) => isActive ? 'active' : ''}>
              About
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;