 import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './MainPage.css';
import { FaUserNurse, FaUserMd, FaStethoscope } from 'react-icons/fa';
import logo from './logo.png';
import image1 from './image1.png';
import image2 from './image2.png';
import image3 from './image3.png';

const MainPage = () => {
  const [activeSection, setActiveSection] = useState(null);
  const [currentSlide, setCurrentSlide] = useState(0);
  const navigate = useNavigate();

  const slides = [
    { image: image1, alt: 'Slide 1' },
    { image: image2, alt: 'Slide 2' },
    { image: image3, alt: 'Slide 3' },
  ];

  const handleSectionClick = (section) => {
    setActiveSection(activeSection === section ? null : section);
  };

  const handleRoleClick = (role) => {
    navigate('/login', { state: { role } });
  };

  useEffect(() => {
    const slideInterval = setInterval(() => {
      setCurrentSlide((prevSlide) => (prevSlide + 1) % slides.length);
    }, 3000);

    return () => clearInterval(slideInterval);
  }, [slides.length]);

  return (
    <div className="main-page">
      <header className="taskbar">
        <div className="logo-container">
          <img src={logo} alt="HealthNest Logo" className="logo" />
          <div className="title-group">
            <h1 className="hospital-name">HealthNest</h1>
            <p className="tagline">One Nest for Every Nurse and Doctor</p>
          </div>
        </div>
        <nav className="nav-bar">
          <ul className="nav-list">
            <li onClick={() => handleSectionClick('about')}>About Us</li>
            <li onClick={() => handleSectionClick('contact')}>Contact Us</li>
            <li onClick={() => handleSectionClick('locations')}>Locations</li>
          </ul>
        </nav>
      </header>

      {activeSection && (
        <div className="dynamic-content">
          {activeSection === 'about' && (
            <div className="section-content">
              <h2>About Us</h2>
              <p>
                HealthNest is a secure, collaborative digital workspace designed for modern healthcare teams.
                Built to streamline clinical workflows, HealthNest empowers nurses and doctors to document, review,
                and manage patient information with ease — all in one place. Our advanced Surgical Site Infection (SSI)
                Detection system assists in early identification of post-surgical complications.
              </p>
            </div>
          )}
          {activeSection === 'contact' && (
            <div className="section-content">
              <h2>Contact Us</h2>
              <p>
                Phone: 1800 102 9103<br />
                Email: contact@healthnest.com
              </p>
            </div>
          )}
          {activeSection === 'locations' && (
            <div className="section-content">
              <h2>Locations</h2>
              <p>Find us in New Delhi, Mumbai, and Bengaluru.</p>
            </div>
          )}
        </div>
      )}

      <div className="slideshow">
        <img
          src={slides[currentSlide].image}
          alt={slides[currentSlide].alt}
          className="slideshow-image"
        />
      </div>

      <div className="role-selection-container">
        <div className="role-cards-container">
          <div className="role-card" onClick={() => handleRoleClick('nurse')}>
            <FaUserNurse className="role-icon" />
            <h3>Nurse</h3>
          </div>
          <div className="role-card" onClick={() => handleRoleClick('junior_doctor')}>
            <FaStethoscope className="role-icon" />
            <h3>Junior Doctor</h3>
          </div>
          <div className="role-card" onClick={() => handleRoleClick('senior_doctor')}>
            <FaUserMd className="role-icon" />
            <h3>Senior Doctor</h3>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
