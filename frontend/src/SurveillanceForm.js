import React, { useState } from 'react';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';
import { submitSurveillanceForm } from './api/nurseFormApi';

const SurveillanceForm = () => {
  const [formData, setFormData] = useState({
    patientName: '',
    age: '',
    gender: '',
    dateOfAdmission: '',
    dateOfProcedure: '',
    admittingDepartment: '',
    departmentPrimarySurgeon: '',
    procedureName: '',
    diagnosis: '',
    procedureDoneBy: '',
    operationTheatre: '',
    outpatientProcedure: '',
    scenarioProcedure: '',
    woundClass: '',
    papGiven: '',
    antibioticsGiven: '',
    durationPAP: '',
    ssiEventOccurred: '',
    dateOfEvent: '',
    diabeticPatient: '',
    patientOnSteroids: '',
    alcoholConsumption: '',
    tobaccoConsumption: '',
    // weight: '',
    lengthOfSurgery: '',
    // height: '', // Kept for BMI calculation
    bmi: '',    // Kept for BMI calculation
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Prepare payload for backend
    const payload = {
      patientName: formData.patientName,
      age: parseInt(formData.age) || 0,
      gender: formData.gender,
      dateOfAdmission: formData.dateOfAdmission,
      dateOfProcedure: formData.dateOfProcedure,
      admittingDepartment: formData.admittingDepartment,
      departmentPrimarySurgeon: formData.departmentPrimarySurgeon,
      procedureName: formData.procedureName,
      diagnosis: formData.diagnosis,
      procedureDoneBy: formData.procedureDoneBy,
      operationTheatre: formData.operationTheatre,
      outpatientProcedure: formData.outpatientProcedure,
      scenarioProcedure: formData.scenarioProcedure,
      woundClass: formData.woundClass,
      papGiven: formData.papGiven,
      antibioticsGiven: formData.antibioticsGiven,
      durationPAP: formData.durationPAP,
      ssiEventOccurred: formData.ssiEventOccurred,
      dateOfEvent: formData.ssiEventOccurred === 'yes' ? formData.dateOfEvent : null,
      diabeticPatient: formData.diabeticPatient,
      patientOnSteroids: formData.patientOnSteroids,
      alcoholConsumption: formData.alcoholConsumption,
      tobaccoConsumption: formData.tobaccoConsumption,
      // weight: parseInt(formData.weight) || 0,
      // height: parseInt(formData.height) || 0,
      bmi: parseInt(formData.bmi) || 0,
      lengthOfSurgery: parseInt(formData.lengthOfSurgery) || 0,
    };

    // Client-side validation
    const requiredFields = Object.keys(payload).filter(field => field !== 'dateOfEvent');
    for (const field of requiredFields) {
      if (!payload[field]) {
        alert(`Please fill in ${field}`);
        return;
      }
    }
    if (payload.ssiEventOccurred === 'yes' && !payload.dateOfEvent) {
      alert('Please fill in Date of Event');
      return;
    }

    console.log('Sending payload:', payload); // Log payload for debugging

    try {
      const result = await submitSurveillanceForm(payload);
      if (result.status === 'SUCCESS') {
        alert('Data saved successfully!');
      } else {
        const errorMsg = typeof result.msg === 'object' ? JSON.stringify(result.msg) : result.msg;
        alert(`Server error: ${errorMsg}`);
      }
    } catch (error) {
      console.error('Error:', error.response?.data, error.response?.status);
      const errorMsg = error.response?.data?.msg || error.message;
      alert(`Submission failed: ${typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg}`);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newFormData = {
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    };

    // Calculate BMI if weight or height changes
    if (name === 'weight' || name === 'height') {
      const weight = parseFloat(newFormData.weight) || 0;
      const height = parseFloat(newFormData.height) || 0;
      if (weight > 0 && height > 0) {
        const heightInMeters = height / 100; // Convert cm to meters
        const bmi = (weight / (heightInMeters * heightInMeters)).toFixed(2);
        newFormData.bmi = bmi;
      } else {
        newFormData.bmi = '';
      }
    }

    setFormData(newFormData);
  };

  const generatePDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(18);
    doc.text('Surgical Site Infection Surveillance Form', 20, 20);

    const tableData = [
      ['Patient Name', formData.patientName],
      ['Age', formData.age],
      ['Gender', formData.gender],
      ['Date of Admission', formData.dateOfAdmission],
      ['Date of Procedure', formData.dateOfProcedure],
      ['Admitting Department', formData.admittingDepartment],
      ['Primary Surgeon Department', formData.departmentPrimarySurgeon],
      ['Procedure Name', formData.procedureName],
      ['Diagnosis', formData.diagnosis],
      ['Procedure Done By', formData.procedureDoneBy],
      ['Operation Theatre', formData.operationTheatre],
      ['Outpatient Procedure', formData.outpatientProcedure],
      ['Scenario Procedure', formData.scenarioProcedure],
      ['Wound Class', formData.woundClass],
      ['PAP Given', formData.papGiven],
      ['Antibiotics Given', formData.antibioticsGiven],
      ['Duration of PAP', formData.durationPAP],
      ['SSI Event Occurred', formData.ssiEventOccurred],
      ['Date of Event', formData.dateOfEvent],
      ['Diabetes', formData.diabeticPatient],
      ['Patient on Steroids', formData.patientOnSteroids],
      ['Alcohol Consumption', formData.alcoholConsumption],
      ['Tobacco Consumption', formData.tobaccoConsumption],
      // ['Patient Weight (kg)', formData.weight],
      // ['Patient Height (cm)', formData.height],
      ['BMI', formData.bmi],
      ['Length of Surgery (hours)', formData.lengthOfSurgery],
    ];

    doc.autoTable({
      head: [['Field', 'Value']],
      body: tableData,
      startY: 40,
    });

    doc.save('SurveillanceForm.pdf');
  };

  const handleDownloadExcel = () => {
    alert('Downloaded as Excel.');
  };

  // Choice options aligned with backend
  const genderOptions = [
    { value: 'M', label: 'Male' },
    { value: 'F', label: 'Female' },
    { value: 'O', label: 'Other' },
  ];

  const yesNoOptions = [
    { value: 'yes', label: 'Yes' },
    { value: 'no', label: 'No' },
  ];

  const diabeticOptions = [
    { value: 'no', label: 'No' },
    { value: 'high', label: 'High' },
    { value: 'low', label: 'Low' },
  ];

  const scenarioOptions = [
    { value: 'elective', label: 'Elective' },
    { value: 'emergency', label: 'Emergency' },
  ];

  const woundClassOptions = [
    { value: 'clean', label: 'Clean' },
    { value: 'clean-contaminated', label: 'Clean-contaminated' },
    { value: 'contaminated', label: 'Contaminated' },
    { value: 'dirty', label: 'Dirty' },
  ];

  const durationPAPOptions = [
    { value: 'within 30 mins', label: 'within 30 mins' },
    { value: 'within 60 mins', label: 'within 60 mins' },
    { value: 'within 90 mins', label: 'within 90 mins' },
    { value: 'more than 90 mins', label: 'more than 90 mins' },
  ];

  // Backend-aligned CHOICES
  const procedures = [
    'Abdominal aortic aneurysm repair',
    'Limb amputation',
    'Appendix surgery',
    'Shunt for dialysis',
    'Bile duct, liver, or pancreas surgery',
    'Carotid endarterectomy',
    'Gallbladder surgery',
    'Colon surgery',
    'Cesarean section',
    'Gastric surgery',
    'Heart transplant',
    'Abdominal hysterectomy',
    'Kidney transplant',
    'Laminectomy',
    'Liver transplant',
    'Neck surgery',
    'Kidney surgery',
    'Ovarian surgery',
    'Prostate surgery',
    'Rectal surgery',
    'Small bowel surgery',
    'Spleen surgery',
    'Thoracic surgery',
    'Thyroid and parathyroid surgery',
    'Vaginal hysterectomy',
    'Exploratory laparotomy',
    'Breast surgery',
    'Cardiac surgery',
    'Coronary artery bypass graft',
    'Craniotomy',
    'Spinal fusion',
    'Open reduction of fracture',
    'Hip prosthesis',
    'Knee prosthesis',
    'Pacemaker surgery',
    'Peripheral vascular bypass surgery',
    'Ventricular shunt',
    'Herniorrhaphy',
    'Laparotomy',
  ];

  const theatres = [
    'OT NO. 1',
    'OT NO. 2',
    'OT NO. 3',
    'OT NO. 4',
    'OT NO. 5',
    'OT NO. 6',
    'OT NO. 7',
    'OT NO. 8',
    'OT NO. 9',
    'OT NO. 10',
    'OT NO. 11',
    'OT NO. 12',
    'ROBOTIC OT',
    'C-SEC OT',
    'MINOR OT',
    'COSMETOLOGY OT',
    'Others',
  ];

  const departments = [
    'Cardiothoracic Surgery',
    'Internal Medicine',
    'Anesthesia',
    'Cardiology',
    'Hemato-Oncology & Bone Marrow Transplant',
    'Liver Transplant & Surgical Gastroenterology',
    'Oncology',
    'GI & Hepato-Pancreatico-Biliary Surgery',
    'Critical Care',
    'Pulmonary Medicine & Critical Care',
    'Radiodiagnosis & Imaging',
    'Nephrology',
    'Urology & Renal Transplant',
    'Plastic & Aesthetic Surgery',
    'Gastroenterology',
    'Orthopedics & Joint Replacement',
    'NeuroSciences',
    'Pediatric',
    'Laboratory Medicine',
    'Endocrinology',
    'General & Minimally Access Surgery',
    'Obstetrics & Gynaecology',
    'Dental Department',
    'Nuclear Medicine',
    'Dermatology',
    'Rheumatology',
    'IVF & Reproductive Medicine',
    'Orthopedic Spine',
    'Onco Surgery',
    'Medical Services',
    'Ophthalmology',
    'ENT',
    'Respiratory, Critical Care & Sleep Medicine',
    'Behavioral Sciences',
  ];

  const doctors = [
    'Dr. Manoj Luthra',
    'Dr. Vinay Labroo',
    'Dr. Ramesh Gourishankar',
    'Dr. Biswajit Paul',
    'Dr. Brig (Dr.) Satyaranjan Das',
    'Dr. Karisangal Vasudevan Ramaswamy',
    'Dr. (Col) Sunil Sofat',
    'Dr. Ashish Goel',
    'Dr. Rajesh Kapoor',
    'Dr. Shalendra Goel',
    'Dr. Gyanendra Agrawal',
    'Dr. Chandra Prakash Singh Chauhan',
    'Dr. Anil Prasad Bhatt',
    'Dr. Amit Kumar Devra',
    'Dr. Ashish Rai',
    'Dr. Manik Sharma',
    'Dr. B. L. Agarwal',
    'Dr. Vijay Kumar Sinha',
    'Dr. Sumit Bhushan Sharma',
    'Dr. Rohan Sinha',
    'Dr. Dinesh Rattnani',
    'Dr. Ashu Sawhney',
    'Dr. Suryasnata Das',
    'Dr. (Col) Vimal Upreti',
    'Dr. Nidhi Malhotra',
    'Dr. Manish Gupta',
    'Dr. Abhishek Goyal',
    'Dr. Poonam Yadav',
    'Dr. Praveen Kumar',
    'Dr. Reenu Jain',
    'Dr. Abhishek Gulia',
    'Dr. Kishore Das',
    'Dr. Pooja Goel',
    'Dr. Suhas Singla',
    'Dr. Asfaq Khan',
    'Dr. Shalini Sharma',
    'Dr. Sharique Ahmed',
    'Dr. Deepak Singhal',
    'Dr. Smita Sharma',
    'Dr. Pankaj Kumar Goyal',
    'Dr. Sakshi Srivastava',
    'Dr. Suvrat Arya',
    'Dr. Soma Singh',
    'Dr. Devender Chhonker',
    'Dr. Pramod Saini',
    'Dr. Lok Prakash Choudhary',
    'Dr. Dhirendra Pratap Singh Yadav',
    'Dr. Ashish Kumar Govil',
    'Dr. Atul Sharma',
    'Dr. Mansoor Ahmed Siddiqui',
    'Dr. Krishnanu Dutta Choudhury',
    'Dr. Mrinmay Kumar Das',
    'Dr. Minal Singh',
    'Dr. Anshul Jain',
    'Dr. Swapnil Yashwant Gajway',
    'Dr. Ashish Soni',
    'Dr. Kapil Kumar',
    'Dr. Abhinav Kumar',
    'Dr. Hema Rattnani',
    'Dr. Vikash Nayak',
    'Dr. Naveen Prakash Verma',
    'Dr. Bhupender Singh',
    'Dr. Aditya Bhatla',
    'Dr. Shovna Veshnavi',
    'Dr. Purnima Sahni Sood',
    'Dr. (Col) Subodh Kumar',
    'Dr. Shweta Goswami',
    'Dr. Sunita Maheshwari',
    'Dr. Atul K Maheshwari',
    'Dr. Sharad Dev',
    'Dr. Vikram Singh Solanki',
    'Dr. Radha Agartaniya',
    'Dr. Mithee Bhanot',
    'Dr. Vibha Bansal',
    'Dr. Rashmi Vyas',
    'Dr. Richa Thukral',
    'Dr. Nischal Anand',
    'Dr. Abhishek',
    'Dr. Vikram Bhardwaj',
    'Dr. Devashish Sharma',
    'Dr. Aastha Gupta',
    'Dr. Dipali Taneja',
    'Dr. Priyadarshi Jitendra Kumar',
    'Dr. Priyanka Srivastava',
    'Dr. Manasi Mehra',
    'Dr. Anita Singla',
    'Dr. Abhishek Kumar',
    'Dr. Parul Singhal',
    'Dr. Prerna Sharma',
    'Dr. Shweta Gupta',
    'Dr. Kumari Madhulika',
    'Dr. Jyoti Jain',
    'Dr. Sanjay Sharma',
    'Dr. Sandeep Yadav',
    'Dr. Sonalika Singh Chauhan',
    'Dr. Meenakshi Maurya',
    'Dr. Manisha Ranjan',
    'Dr. Pankaj Kumar',
    'Dr. Rohit Kumar Pandey',
    'Dr. Deepshikha',
    'Dr. Meenakshi',
    'Dr. Arti Yadav',
    'Dr. Anjali Gupta',
    'Dr. Rajesh Prasad Gupta',
    'Dr. Abhay Kumar Singh',
    'Dr. Raman Mehta',
    'Dr. Abhishek Dave',
    'Dr. Preeti Deolwari',
    'Dr. Abhijeet Kotabagi',
    'Dr. Chandrika',
    'Dr. Parineeta Maria',
  ];

  const antibiotics = [
    'Ceftriaxone',
    'Amoxicillin',
    'Vancomycin',
    'Metronidazole',
    'Levofloxacin',
    // Add more antibiotics as per ANTIBIOTIC_CHOICES
  ];

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px', border: '1px solid #ccc', borderRadius: '10px', backgroundColor: '#f9f9f9' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Surgical Site Infection Surveillance Form</h2>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
        <label style={{ gridColumn: 'span 1' }}>Patient Name:</label>
        <input type="text" name="patientName" value={formData.patientName} onChange={handleChange} required style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Age:</label>
        <input type="number" name="age" value={formData.age} onChange={handleChange} required style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Gender:</label>
        <select name="gender" value={formData.gender} onChange={handleChange} required style={{ gridColumn: 'span 1' }}>
          <option value="">Select Gender</option>
          {genderOptions.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Date of Admission:</label>
        <input type="date" name="dateOfAdmission" value={formData.dateOfAdmission} onChange={handleChange} required style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Date of Operative Procedure:</label>
        <input type="date" name="dateOfProcedure" value={formData.dateOfProcedure} onChange={handleChange} required style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Admitting Department:</label>
        <select name="admittingDepartment" value={formData.admittingDepartment} onChange={handleChange} required style={{ gridColumn: 'span 1' }}>
          <option value="">Select Department</option>
          {departments.map((dept, index) => (
            <option key={index} value={dept}>{dept}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Department (Primary Surgeon):</label>
        <select name="departmentPrimarySurgeon" value={formData.departmentPrimarySurgeon} onChange={handleChange} required style={{ gridColumn: 'span 1' }}>
          <option value="">Select Department</option>
          {departments.map((dept, index) => (
            <option key={index} value={dept}>{dept}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Name of Procedure:</label>
        <select name="procedureName" value={formData.procedureName} onChange={handleChange} required style={{ gridColumn: 'span 1' }}>
          <option value="">Select Procedure</option>
          {procedures.map((proc, index) => (
            <option key={index} value={proc}>{proc}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Diagnosis:</label>
        <input type="text" name="diagnosis" value={formData.diagnosis} onChange={handleChange} required style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Procedure done by:</label>
        <select name="procedureDoneBy" value={formData.procedureDoneBy} onChange={handleChange} required style={{ gridColumn: 'span 1' }}>
          <option value="">Select Doctor</option>
          {doctors.map((doctor, index) => (
            <option key={index} value={doctor}>{doctor}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Operation Theatre:</label>
        <select name="operationTheatre" value={formData.operationTheatre} onChange={handleChange} required style={{ gridColumn: 'span 1' }}>
          <option value="">Select Theatre</option>
          {theatres.map((theatre, index) => (
            <option key={index} value={theatre}>{theatre}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Outpatient Procedure:</label>
        <div style={{ gridColumn: 'span 1' }}>
          {yesNoOptions.map(opt => (
            <label key={opt.value}>
              <input
                type="radio"
                name="outpatientProcedure"
                value={opt.value}
                checked={formData.outpatientProcedure === opt.value}
                onChange={handleChange}
                required
              /> {opt.label}
            </label>
          ))}
        </div>

        <label style={{ gridColumn: 'span 1' }}>Scenario of Procedure:</label>
        <select name="scenarioProcedure" value={formData.scenarioProcedure} onChange={handleChange} required style={{ gridColumn: 'span 1' }}>
          <option value="">Select Scenario</option>
          {scenarioOptions.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Wound Class:</label>
        <div style={{ gridColumn: 'span 1' }}>
          {woundClassOptions.map(opt => (
            <label key={opt.value}>
              <input
                type="radio"
                name="woundClass"
                value={opt.value}
                checked={formData.woundClass === opt.value}
                onChange={handleChange}
                required
              /> {opt.label}
            </label>
          ))}
        </div>

        <label style={{ gridColumn: 'span 1' }}>Pre/Peri-operative Antibiotic Prophylaxis (PAP) Given:</label>
        <div style={{ gridColumn: 'span 1' }}>
          {yesNoOptions.map(opt => (
            <label key={opt.value}>
              <input
                type="radio"
                name="papGiven"
                value={opt.value}
                checked={formData.papGiven === opt.value}
                onChange={handleChange}
                required
              /> {opt.label}
            </label>
          ))}
        </div>

        <label style={{ gridColumn: 'span 1' }}>If Yes, Antibiotics Given:</label>
        <select name="antibioticsGiven" value={formData.antibioticsGiven} onChange={handleChange} required style={{ gridColumn: 'span 1' }}>
          <option value="">Select Antibiotic</option>
          {antibiotics.map((antibiotic, index) => (
            <option key={index} value={antibiotic}>{antibiotic}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Duration of PAP:</label>
        <select name="durationPAP" value={formData.durationPAP} onChange={handleChange} required style={{ gridColumn: 'span 1' }}>
          <option value="">Select Duration</option>
          {durationPAPOptions.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Diabetes:</label>
        <div style={{ gridColumn: 'span 1' }}>
          {diabeticOptions.map(opt => (
            <label key={opt.value}>
              <input
                type="radio"
                name="diabeticPatient"
                value={opt.value}
                checked={formData.diabeticPatient === opt.value}
                onChange={handleChange}
                required
              /> {opt.label}
            </label>
          ))}
        </div>

        <label style={{ gridColumn: 'span 1' }}>Patient on Steroids:</label>
        <div style={{ gridColumn: 'span 1' }}>
          {yesNoOptions.map(opt => (
            <label key={opt.value}>
              <input
                type="radio"
                name="patientOnSteroids"
                value={opt.value}
                checked={formData.patientOnSteroids === opt.value}
                onChange={handleChange}
                required
              /> {opt.label}
            </label>
          ))}
        </div>

        <label style={{ gridColumn: 'span 1' }}>Alcohol Consumption:</label>
        <div style={{ gridColumn: 'span 1' }}>
          {yesNoOptions.map(opt => (
            <label key={opt.value}>
              <input
                type="radio"
                name="alcoholConsumption"
                value={opt.value}
                checked={formData.alcoholConsumption === opt.value}
                onChange={handleChange}
                required
              /> {opt.label}
            </label>
          ))}
        </div>

        <label style={{ gridColumn: 'span 1' }}>Tobacco Consumption:</label>
        <div style={{ gridColumn: 'span 1' }}>
          {yesNoOptions.map(opt => (
            <label key={opt.value}>
              <input
                type="radio"
                name="tobaccoConsumption"
                value={opt.value}
                checked={formData.tobaccoConsumption === opt.value}
                onChange={handleChange}
                required
              /> {opt.label}
            </label>
          ))}
        </div>

        {/* <label style={{ gridColumn: 'span 1' }}>Patient Weight (kg):</label>
        <input type="number" name="weight" value={formData.weight} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Patient Height (cm):</label>
        <input type="number" name="height" value={formData.height} onChange={handleChange} style={{ gridColumn: 'span 1' }} /> */}

        <label style={{ gridColumn: 'span 1' }}>BMI:</label>
        <input type="number" name="bmi" value={formData.bmi} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Length of Surgery (hours):</label>
        <input type="number" name="lengthOfSurgery" value={formData.lengthOfSurgery} onChange={handleChange} required style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>SSI Event Occurred:</label>
        <div style={{ gridColumn: 'span 1' }}>
          {yesNoOptions.map(opt => (
            <label key={opt.value}>
              <input
                type="radio"
                name="ssiEventOccurred"
                value={opt.value}
                checked={formData.ssiEventOccurred === opt.value}
                onChange={handleChange}
                required
              /> {opt.label}
            </label>
          ))}
        </div>

        {formData.ssiEventOccurred === 'yes' && (
          <>
            <label style={{ gridColumn: 'span 1' }}>If Yes, Date of Event:</label>
            <input
              type="date"
              name="dateOfEvent"
              value={formData.dateOfEvent || ''}
              onChange={handleChange}
              required
              style={{ gridColumn: 'span 1' }}
            />
          </>
        )}

        <div style={{ gridColumn: 'span 2', textAlign: 'center' }}>
          <button type="submit" style={{ marginTop: '20px', padding: '10px 15px', backgroundColor: 'blue', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Submit
          </button>
          <button
            type="button"
            onClick={generatePDF}
            style={{
              padding: '10px 20px',
              backgroundColor: 'red',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              marginTop: '20px',
              marginLeft: '10px',
            }}
          >
            Download as PDF
          </button>
          <button
            type="button"
            onClick={handleDownloadExcel}
            style={{
              padding: '10px 20px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              marginTop: '20px',
              marginLeft: '10px',
            }}
          >
            Download as Excel
          </button>
        </div>
      </form>
    </div>
  );
};

export default SurveillanceForm;