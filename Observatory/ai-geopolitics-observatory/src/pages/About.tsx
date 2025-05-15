import React from 'react';
import Layout from '../components/common/Layout';

const About: React.FC = () => {
  return (
    <Layout>
      <div className="about-page">
        <div className="page-header">
          <h1>About the Public Observatory of AI Geopolitics</h1>
        </div>

        <section className="about-section">
          <h2>Our Mission</h2>
          <p>
            The Public Observatory of AI Geopolitics (POAIG) is an educational resource for researchers and students 
            focused on understanding the complex geopolitical landscape of artificial intelligence. Our mission is to 
            provide unique insights through data-driven analysis of global AI narratives, policies, and developments.
          </p>
        </section>

        <section className="about-section">
          <h2>Key Components</h2>
          
          <div className="component-description">
            <h3>Perception Tracker</h3>
            <p>
              The Perception Tracker monitors and visualizes media headlines, social media discourse, and narrative 
              tropes related to AI geopolitics. It provides researchers with tools to understand how AI is perceived 
              and discussed across different regions, actors, and contexts.
            </p>
          </div>
          
          <div className="component-description">
            <h3>Signals</h3>
            <p>
              The Signals component features expert analysis and insights on emerging trends, developments, and 
              inflection points in AI geopolitics. Contributors from various backgrounds provide interpretations 
              through different lenses including security, ethics, industrial, social, and legal perspectives.
            </p>
          </div>
          
          <div className="component-description">
            <h3>Timeline & Policy Map</h3>
            <p>
              The Timeline & Policy Map provides chronological context for key regulatory developments, corporate 
              actions, and bloc-level initiatives in the global AI landscape. It helps researchers understand the 
              sequence and relationships between significant events.
            </p>
          </div>
        </section>

        <section className="about-section">
          <h2>Our Approach</h2>
          <p>
            POAIG takes a multidisciplinary approach to understanding AI geopolitics, combining:
          </p>
          <ul>
            <li>Data-driven analysis of media and social discourse</li>
            <li>Expert interpretation of key developments</li>
            <li>Contextual mapping of policies and regulations</li>
            <li>Visualization of complex relationships and trends</li>
          </ul>
          <p>
            Our goal is to provide researchers, students, and policymakers with the tools and insights needed to 
            navigate the increasingly complex intersection of AI technology and geopolitics.
          </p>
        </section>

        <section className="about-section">
          <h2>The Team</h2>
          <p>
            POAIG is developed and maintained by a small team of researchers and developers with backgrounds in 
            international relations, technology policy, data science, and software engineering. The platform also 
            benefits from contributions by a network of experts who provide signals and analysis.
          </p>
          <p>
            If you're interested in contributing to POAIG as a signal contributor or have suggestions for improving 
            the platform, please contact us using the form below.
          </p>
        </section>

        <section className="about-section">
          <h2>Contact Us</h2>
          <form className="contact-form">
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input type="text" id="name" name="name" />
            </div>
            
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input type="email" id="email" name="email" />
            </div>
            
            <div className="form-group">
              <label htmlFor="subject">Subject</label>
              <input type="text" id="subject" name="subject" />
            </div>
            
            <div className="form-group">
              <label htmlFor="message">Message</label>
              <textarea id="message" name="message" rows={5}></textarea>
            </div>
            
            <button type="submit" className="btn btn-primary">Send Message</button>
          </form>
        </section>
      </div>
    </Layout>
  );
};

export default About;