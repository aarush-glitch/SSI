// frontend/src/api/nurseFormsApi.js

const BASE_URL = 'http://localhost:8000/nurse';

const antibioticFormUrl = `${BASE_URL}/patient_antibiotic_surveillance/add/`;
const surgeryFormUrl = `${BASE_URL}/patient_post_surgery_details/add/`;
const microbiologyFormUrl = `${BASE_URL}/patient_microbiology_details/add/`;
const eventDetailsFormUrl = `${BASE_URL}/patient_event_details/add/`;
const ssiEvaluationFormUrl = `${BASE_URL}/patient_ssi_evaluation_details/add/`;
const surveillanceFormUrl = `${BASE_URL}/patient_administration_details/add/`;

export const submitAntibioticForm = async (formData) => {
  try {
    const response = await fetch(antibioticFormUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    return await response.json();
  } catch (error) {
    console.error('submitAntibioticForm error:', error);
    return { status: 'ERROR', msg: error.message || 'Network error while submitting antibiotic form.' };
  }
};

export const submitSurgeryForm = async (formData) => {
  try {
    const response = await fetch(surgeryFormUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    return await response.json();
  } catch (error) {
    console.error('submitSurgeryForm error:', error);
    return { status: 'ERROR', msg: error.message || 'Network error while submitting surgery form.' };
  }
};

export const submitMicrobiologyForm = async (formData) => {
  try {
    const response = await fetch(microbiologyFormUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    return await response.json();
  } catch (error) {
    console.error('submitMicrobiologyForm error:', error);
    return { status: 'ERROR', msg: error.message || 'Network error while submitting microbiology form.' };
  }
};

export const submitEventDetailsForm = async (formData) => {
  try {
    const response = await fetch(eventDetailsFormUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    return await response.json();
  } catch (error) {
    console.error('submitEventDetailsForm error:', error);
    return { status: 'ERROR', msg: error.message || 'Network error while submitting event details form.' };
  }
};

export const submitSSIEvaluationForm = async (formData) => {
  try {
    const response = await fetch(ssiEvaluationFormUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    return await response.json();
  } catch (error) {
    console.error('submitSSIEvaluationForm error:', error);
    return { status: 'ERROR', msg: error.message || 'Network error while submitting SSI evaluation form.' };
  }
};

export const submitSurveillanceForm = async (formData) => {
  try {
    const response = await fetch(surveillanceFormUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    return await response.json();
  } catch (error) {
    console.error('submitSurveillanceForm error:', error);
    return { status: 'ERROR', msg: error.message || 'Network error while submitting surveillance form.' };
  }
};
