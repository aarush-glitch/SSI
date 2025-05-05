import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './JuniorDoctor.css'; 
import logo from './logo.png'; 

// List of patients
const patients = [
  { id: 'P001', name: 'Rachna Singh' },
  { id: 'P002', name: 'Prabnoor Kaur' },
  { id: 'P003', name: 'Rajeev Kumar' },
];

const JuniorDoctor = () => {
  const [expandedPatientId, setExpandedPatientId] = useState(null);
  const navigate = useNavigate(); 

  // Toggle logic for patient card expansion
  const togglePatientCard = (patientId) => {
    setExpandedPatientId(expandedPatientId === patientId ? null : patientId);
  };

  // List of form options to navigate to
  const formOptions = [
    { path: '/surveillance-form', label: 'Administration Details' },
    { path: '/surgery-form', label: 'Surgery Details' },
    { path: '/antibiotic-form', label: 'Antibiotic Details' },
    { path: '/microbiology-form', label: 'Microbiology Details' },
    { path: '/event-details-form', label: 'Event Details' },
    { path: '/SSI-evaluation-form', label: 'SSI Evaluation' },
  ];

  return (
    <div className="junior-doctor-page">
      {/* Taskbar Section */}
      <div className="taskbar">
        <div className="logo-container">
          <img src={logo} alt="Junior Doctor Portal Logo" className="logo" />
          <h1 className="hospital-name">Junior Doctor Portal</h1>
        </div>
      </div>

      
      {/* <h1 className="page-title">Welcome to Junior Doctor Portal</h1> */}
      <p className="intro-text">Click on a patient to open their forms:</p> 

      {/* Patient Cards */}
      <div className="patient-cards-container">
        {patients.map((patient) => (
          <div
            key={patient.id}
            className={`patient-card ${expandedPatientId === patient.id ? 'expanded' : ''}`}
            onClick={() => togglePatientCard(patient.id)}
          >
            {/* Patient Icon and Name */}
            <h2>
              <i className="bi bi-person-fill patient-icon"></i> {/* Bootstrap icon */}
              {patient.name}
            </h2>
            <p>ID: {patient.id}</p>

            {/* Form Buttons */}
            {expandedPatientId === patient.id && (
              <div className="form-buttons">
                {formOptions.map((option) => (
                  <button
                    key={option.path}
                    onClick={(e) => {
                      e.stopPropagation(); // Prevent card collapse when clicking button
                      navigate(option.path);
                    }}
                  >
                    {option.label}
                  </button>
                ))}
                 <button
                  className="ssi-prediction-button"
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/ssi-prediction/${patient.id}`);
                  }}
                >
                  SSI Prediction
                </button>
              
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default JuniorDoctor;  