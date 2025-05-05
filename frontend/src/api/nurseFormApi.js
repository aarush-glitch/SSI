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

// export const submitSurveillanceForm = async (formData) => {
//   try {
//     const response = await fetch(surveillanceFormUrl, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(formData),
//     });
//     return await response.json();
//   } catch (error) {
//     console.error('submitSurveillanceForm error:', error);
//     return { status: 'ERROR', msg: error.message || 'Network error while submitting surveillance form.' };
//   }
// };

export const submitSurveillanceForm = async (formData) => {
  try {
    // Transform data to match Django expectations
    const payload = {
      ...formData,
      // Fix case mismatches (React -> Django)
      // weight: formData.Weight,  // Map 'Weight' (React) to 'weight' (Django)
      bmi: formData.bmi || null,
      dateOfAdmission: formData.dateOfAdmission || null,  // Handle empty dates
      dateOfProcedure: formData.dateOfProcedure || null,
      dateOfEvent: formData.dateOfEvent || null
    };
    
    // Remove React-only fields that Django doesn't expect
    // delete payload.Weight;
    // delete payload.Height;
    // delete payload.BMI;

    const response = await fetch(surveillanceFormUrl, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        // No CSRF token needed since using @csrf_exempt
      },
      body: JSON.stringify(payload),
      credentials: 'include' // Still required for session cookies
    });

    // Handle non-2xx responses
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.msg || 
        errorData.message || 
        `HTTP error! status: ${response.status}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error('API submission failed:', error);
    throw error; // Re-throw for handling in UI layer
  }
};