import React from "react";
import "./SSIPrediction.css";
import chart from './chart.png';


const SSIPrediction = () => {
  return (
    <div className="ssi-container">
      <h1 className="ssi-heading">Surgical Site Infection Prediction</h1>


      <div className="ssi-chart">
        <h2 className="ssi-subheading">Patient vs SSI Patients (Feature Comparison)</h2>
        <img src={chart} alt="Comparison Chart" className="chart-image" />
      </div>


      <div className="ssi-alert-text">
        <span className="alert-icon">⚠️</span>
        <strong>RISK | Probability of SSI: 95.93%</strong>
        <p>You have Surgical Site Infection. Please review the following analysis.</p>
      </div>
    </div>
  );
};


export default SSIPrediction;
