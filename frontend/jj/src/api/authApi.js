// src/api/authApi.js

const getOtpUrl = (role) => `http://localhost:8000/${role}/otp/`;
const getRegisterUrl = (role) => `http://localhost:8000/${role}/register/`; // Endpoint for registering a user

export const sendOtp = async (role, phone_number) => {
  try {
    const response = await fetch(getOtpUrl(role), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone_number: parseInt(phone_number),
        action: 'generate',
      }),
    });
    return await response.json();
  } catch (error) {
    console.error('sendOtp error:', error);
    return { status: 'ERROR', msg: 'Network error while sending OTP.' };
  }
};

export const verifyOtp = async (role, phone_number, otp) => {
  try {
    const response = await fetch(getOtpUrl(role), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone_number: parseInt(phone_number),
        action: 'verify',
        otp: parseInt(otp),
      }),
    });
    return await response.json();
  } catch (error) {
    console.error('verifyOtp error:', error);
    return { status: 'ERROR', msg: error.message || 'Network error while verifying OTP.' };
  }
};

export const resendOtp = async (role, phone_number) => {
  try {
    const response = await fetch(getOtpUrl(role), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone_number: parseInt(phone_number),
        action: 'resend',
      }),
    });
    return await response.json();
  } catch (error) {
    console.error('resendOtp error:', error);
    return { status: 'ERROR', msg: 'Network error while resending OTP.' };
  }
};
//GIving error
export const registerUser = async (role, userDetails) => {
  try {
    const response = await fetch(getRegisterUrl(role), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userDetails),
    });
    return await response.json();
  } catch (error) {
    console.error('registerUser error:', error);
    return { status: 'ERROR', msg: 'Network error while registering the user.' };
  }
};
