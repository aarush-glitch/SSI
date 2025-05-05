import React, { useState } from 'react';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

const SurveillanceForm = () => {
  const [formData, setFormData] = useState({
    patientName: '',
    patient_id: '',
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
    Weight: '',
    Height: '', // New field for height (cm)
    BMI: '',   // New field for calculated BMI
    lengthOfSurgery: '',
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newFormData = {
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    };

    // Calculate BMI if Weight or Height changes
    if (name === 'Weight' || name === 'Height') {
      const weight = parseFloat(newFormData.Weight) || 0;
      const height = parseFloat(newFormData.Height) || 0;
      if (weight > 0 && height > 0) {
        const heightInMeters = height / 100; // Convert cm to meters
        const bmi = (weight / (heightInMeters * heightInMeters)).toFixed(2);
        newFormData.BMI = bmi;
      } else {
        newFormData.BMI = '';
      }
    }

    setFormData(newFormData);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/nurse/patient_administration_details/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to submit the form');
      }

      const responseData = await response.json();
      console.log('Form submitted successfully:', responseData);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  const generatePDF = () => {
    const doc = new jsPDF();

    // Add title
    doc.setFontSize(18);
    doc.text('Surgical Site Infection Surveillance Form', 20, 20);

    // Add form data as a table
    const tableData = [
      ['Patient Name', formData.patientName],
      ['Patient ID', formData.patient_id],
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
      ['Patient Weight (kg)', formData.Weight], // Fixed from Weighteight
      ['Patient Height (cm)', formData.Height], // New field
      ['BMI', formData.BMI], // New field
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

  const procedures = [
    'Abdominal aortic aneurysm repair', 'Limb amputation', 'Appendix surgery', 'Shunt for dialysis',
    'Bile duct, liver, or pancreas surgery', 'Carotid endarterectomy', 'Gallbladder surgery', 'Colon surgery',
    'Cesarean section', 'Gastric surgery', 'Heart transplant', 'Abdominal hysterectomy', 'Kidney transplant',
    'Laminectomy', 'Liver transplant', 'Neck surgery', 'Kidney surgery', 'Ovarian surgery', 'Prostate surgery',
    'Rectal surgery', 'Small bowel surgery', 'Spleen surgery', 'Thoracic surgery', 'Thyroid and parathyroid surgery',
    'Vaginal hysterectomy', 'Exploratory laparotomy', 'Breast surgery', 'Cardiac surgery', 'Coronary artery bypass graft',
    'Craniotomy', 'Spinal fusion', 'Open reduction of fracture', 'Hip prosthesis', 'Knee prosthesis', 'Pacemaker surgery',
    'Peripheral vascular bypass surgery', 'Ventricular shunt', 'Herniorrhaphy', 'Laparotomy'
  ];

  const theatres = [
    'OT NO. 1', 'OT NO. 2', 'OT NO. 3', 'OT NO. 4', 'OT NO. 5', 'OT NO. 6', 'OT NO. 7', 'OT NO. 8',
    'OT NO. 9', 'OT NO. 10', 'OT NO. 11', 'OT NO. 12', 'ROBOTIC OT', 'C-SEC OT', 'MINOR OT',
    'COSMETOLOGY OT', 'Others'
  ];

  const departments = [
    'Cardiothoracic Surgery', 'Internal Medicine', 'Anesthesia', 'Cardiology',
    'Hemato-Oncology & Bone Marrow Transplant', 'Liver Transplant & Surgical Gastroenterology',
    'Oncology', 'GI & Hepato-Pancreatico-Biliary Surgery', 'Critical Care',
    'Pulmonary Medicine & Critical Care', 'Radiodiagnosis & Imaging', 'Nephrology',
    'Urology & Renal Transplant', 'Plastic & Aesthetic Surgery', 'Gastroenterology',
    'Orthopedics & Joint Replacement', 'NeuroSciences', 'Pediatric', 'Laboratory Medicine',
    'Endocrinology', 'General & Minimally Access Surgery', 'Obstetrics & Gynaecology',
    'Dental Department', 'Nuclear Medicine', 'Dermatology', 'Rheumatology', 'IVF & Reproductive Medicine',
    'Orthopedic Spine', 'Onco Surgery', 'Medical Services', 'Ophthalmology', 'ENT',
    'Respiratory, Critical Care & Sleep Medicine', 'Behavioral Sciences'
  ];

  const doctors = [
    'Dr. Manoj Luthra', 'Dr. Vinay Labroo', 'Dr. Ramesh Gourishankar', 'Dr. Biswajit Paul',
    'Dr. Brig (Dr.) Satyaranjan Das', 'Dr. Karisangal Vasudevan Ramaswamy', 'Dr. (Col) Sunil Sofat',
    'Dr. Ashish Goel', 'Dr. Rajesh Kapoor', 'Dr. Shalendra Goel', 'Dr. Gyanendra Agrawal',
    'Dr. Chandra Prakash Singh Chauhan', 'Dr. Anil Prasad Bhatt', 'Dr. Amit Kumar Devra',
    'Dr. Ashish Rai', 'Dr. Manik Sharma', 'Dr. B. L. Agarwal', 'Dr. Vijay Kumar Sinha',
    'Dr. Sumit Bhushan Sharma', 'Dr. Rohan Sinha', 'Dr. Dinesh Rattnani', 'Dr. Ashu Sawhney',
    'Dr. Suryasnata Das', 'Dr. (Col) Vimal Upreti', 'Dr. Nidhi Malhotra', 'Dr. Manish Gupta',
    'Dr. Abhishek Goyal', 'Dr. Poonam Yadav', 'Dr. Praveen Kumar', 'Dr. Reenu Jain',
    'Dr. Abhishek Gulia', 'Dr. Kishore Das', 'Dr. Pooja Goel', 'Dr. Suhas Singla',
    'Dr. Asfaq Khan', 'Dr. Shalini Sharma', 'Dr. Sharique Ahmed', 'Dr. Deepak Singhal',
    'Dr. Smita Sharma', 'Dr. Pankaj Kumar Goyal', 'Dr. Sakshi Srivastava', 'Dr. Suvrat Arya',
    'Dr. Soma Singh', 'Dr. Devender Chhonker', 'Dr. Pramod Saini', 'Dr. Lok Prakash Choudhary',
    'Dr. Dhirendra Pratap Singh Yadav', 'Dr. Ashish Kumar Govil', 'Dr. Atul Sharma',
    'Dr. Mansoor Ahmed Siddiqui', 'Dr. Krishnanu Dutta Choudhury', 'Dr. Mrinmay Kumar Das',
    'Dr. Minal Singh', 'Dr. Anshul Jain', 'Dr. Swapnil Yashwant Gajway', 'Dr. Ashish Soni',
    'Dr. Kapil Kumar', 'Dr. Abhinav Kumar', 'Dr. Hema Rattnani', 'Dr. Vikash Nayak',
    'Dr. Naveen Prakash Verma', 'Dr. Bhupender Singh', 'Dr. Aditya Bhatla', 'Dr. Shovna Veshnavi',
    'Dr. Purnima Sahni Sood', 'Dr. (Col) Subodh Kumar', 'Dr. Shweta Goswami', 'Dr. Sunita Maheshwari',
    'Dr. Atul K Maheshwari', 'Dr. Sharad Dev', 'Dr. Vikram Singh Solanki', 'Dr. Radha Agartaniya',
    'Dr. Mithee Bhanot', 'Dr. Vibha Bansal', 'Dr. Rashmi Vyas', 'Dr. Richa Thukral',
    'Dr. Nischal Anand', 'Dr. Abhishek', 'Dr. Vikram Bhardwaj', 'Dr. Devashish Sharma',
    'Dr. Aastha Gupta', 'Dr. Dipali Taneja', 'Dr. Priyadarshi Jitendra Kumar',
    'Dr. Priyanka Srivastava', 'Dr. Manasi Mehra', 'Dr. Anita Singla', 'Dr. Abhishek Kumar',
    'Dr. Parul Singhal', 'Dr. Prerna Sharma', 'Dr. Shweta Gupta', 'Dr. Kumari Madhulika',
    'Dr. Jyoti Jain', 'Dr. Sanjay Sharma', 'Dr. Sandeep Yadav', 'Dr. Sonalika Singh Chauhan',
    'Dr. Meenakshi Maurya', 'Dr. Manisha Ranjan', 'Dr. Pankaj Kumar', 'Dr. Rohit Kumar Pandey',
    'Dr. Deepshikha', 'Dr. Meenakshi', 'Dr. Arti Yadav', 'Dr. Anjali Gupta',
    'Dr. Rajesh Prasad Gupta', 'Dr. Abhay Kumar Singh', 'Dr. Raman Mehta', 'Dr. Abhishek Dave',
    'Dr. Preeti Deolwari', 'Dr. Abhijeet Kotabagi', 'Dr. Chandrika', 'Dr. Parineeta Maria'
  ];

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px', border: '1px solid #ccc', borderRadius: '10px', backgroundColor: '#f9f9f9' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Surgical Site Infection Surveillance Form</h2>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
        {/* Row 1 */}
        <label style={{ gridColumn: 'span 1' }}>Patient Name:</label>
        <input type="text" name="patientName" value={formData.patientName} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Patient ID:</label>
        <input type="text" name="patient_id" value={formData.patient_id} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Age:</label>
        <input type="number" name="age" value={formData.age} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Gender:</label>
        <select name="gender" value={formData.gender} onChange={handleChange} style={{ gridColumn: 'span 1' }}>
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>

        {/* Row 2 */}
        <label style={{ gridColumn: 'span 1' }}>Date of Admission:</label>
        <input type="date" name="dateOfAdmission" value={formData.dateOfAdmission} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Date of Operative Procedure:</label>
        <input type="date" name="dateOfProcedure" value={formData.dateOfProcedure} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Admitting Department:</label>
        <select name="admittingDepartment" value={formData.admittingDepartment} onChange={handleChange} style={{ gridColumn: 'span 1' }}>
          <option value="">Select Department</option>
          {departments.map((dept, index) => (
            <option key={index} value={dept}>{dept}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Department (Primary Surgeon):</label>
        <select name="departmentPrimarySurgeon" value={formData.departmentPrimarySurgeon} onChange={handleChange} style={{ gridColumn: 'span 1' }}>
          <option value="">Select Department</option>
          {departments.map((dept, index) => (
            <option key={index} value={dept}>{dept}</option>
          ))}
        </select>

        {/* Row 3 */}
        <label style={{ gridColumn: 'span 1' }}>Name of Procedure:</label>
        <select name="procedureName" value={formData.procedureName} onChange={handleChange} style={{ gridColumn: 'span 1' }}>
          <option value="">Select Procedure</option>
          {procedures.map((proc, index) => (
            <option key={index} value={proc}>{proc}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Diagnosis:</label>
        <input type="text" name="diagnosis" value={formData.diagnosis} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Procedure done by:</label>
        <select name="procedureDoneBy" value={formData.procedureDoneBy} onChange={handleChange} style={{ gridColumn: 'span 1' }}>
          <option value="">Select Doctor</option>
          {doctors.map((doctor, index) => (
            <option key={index} value={doctor}>{doctor}</option>
          ))}
        </select>

        <label style={{ gridColumn: 'span 1' }}>Operation Theatre:</label>
        <select name="operationTheatre" value={formData.operationTheatre} onChange={handleChange} style={{ gridColumn: 'span 1' }}>
          <option value="">Select Theatre</option>
          {theatres.map((theatre, index) => (
            <option key={index} value={theatre}>{theatre}</option>
          ))}
        </select>

        {/* Row 4 */}
        <label style={{ gridColumn: 'span 1' }}>Outpatient Procedure:</label>
        <div style={{ gridColumn: 'span 1' }}>
          <label><input type="radio" name="outpatientProcedure" value="Yes" checked={formData.outpatientProcedure === 'Yes'} onChange={handleChange} /> Yes</label>
          <label><input type="radio" name="outpatientProcedure" value="No" checked={formData.outpatientProcedure === 'No'} onChange={handleChange} /> No</label>
        </div>

        <label style={{ gridColumn: 'span 1' }}>Scenario of Procedure:</label>
        <select name="scenarioProcedure" value={formData.scenarioProcedure} onChange={handleChange} style={{ gridColumn: 'span 1' }}>
          <option value="">Select Scenario</option>
          <option value="Elective">Elective</option>
          <option value="Emergency">Emergency</option>
        </select>

        <label style={{ gridColumn: 'span 1' }}>Wound Class:</label>
        <div style={{ gridColumn: 'span 1' }}>
          <label><input type="radio" name="woundClass" value="Clean" checked={formData.woundClass === 'Clean'} onChange={handleChange} /> Clean</label>
          <label><input type="radio" name="woundClass" value="Clean-contaminated" checked={formData.woundClass === 'Clean-contaminated'} onChange={handleChange} /> Clean-contaminated</label>
          <label><input type="radio" name="woundClass" value="Contaminated" checked={formData.woundClass === 'Contaminated'} onChange={handleChange} /> Contaminated</label>
          <label><input type="radio" name="woundClass" value="Dirty" checked={formData.woundClass === 'Dirty'} onChange={handleChange} /> Dirty</label>
        </div>

        <label style={{ gridColumn: 'span 1' }}>Pre/Peri-operative Antibiotic Prophylaxis (PAP) Given:</label>
        <div style={{ gridColumn: 'span 1' }}>
          <label><input type="radio" name="papGiven" value="Yes" checked={formData.papGiven === 'Yes'} onChange={handleChange} /> Yes</label>
          <label><input type="radio" name="papGiven" value="No" checked={formData.papGiven === 'No'} onChange={handleChange} /> No</label>
        </div>

        <label style={{ gridColumn: 'span 1' }}>If Yes, Antibiotics Given:</label>
        <input type="text" name="antibioticsGiven" value={formData.antibioticsGiven} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        <label style={{ gridColumn: 'span 1' }}>Duration of PAP (within 60 mins):</label>
        <select name="durationPAP" value={formData.durationPAP} onChange={handleChange} style={{ gridColumn: 'span 1' }}>
          <option value="">Select Duration</option>
          <option value="within 30 mins">within 30 mins</option>
          <option value="within 60 mins">within 60 mins</option>
          <option value="within 90 mins">within 90 mins</option>
          <option value="more than 90 mins">more than 90 mins</option>
        </select>

        {/* Diabetes */}
        <label style={{ gridColumn: 'span 1' }}>Diabetes:</label>
        <div style={{ gridColumn: 'span 1' }}>
          <label><input type="radio" name="diabeticPatient" value="High" checked={formData.diabeticPatient === 'High'} onChange={handleChange} /> High</label>
          <label><input type="radio" name="diabeticPatient" value="Low" checked={formData.diabeticPatient === 'Low'} onChange={handleChange} /> Low</label>
          <label><input type="radio" name="diabeticPatient" value="No" checked={formData.diabeticPatient === 'No'} onChange={handleChange} /> No</label>
        </div>

        {/* Patient on Steroids */}
        <label style={{ gridColumn: 'span 1' }}>Patient on Steroids:</label>
        <div style={{ gridColumn: 'span 1' }}>
          <label><input type="radio" name="patientOnSteroids" value="Yes" checked={formData.patientOnSteroids === 'Yes'} onChange={handleChange} /> Yes</label>
          <label><input type="radio" name="patientOnSteroids" value="No" checked={formData.patientOnSteroids === 'No'} onChange={handleChange} /> No</label>
        </div>

        {/* Alcohol Consumption */}
        <label style={{ gridColumn: 'span 1' }}>Alcohol Consumption:</label>
        <div style={{ gridColumn: 'span 1' }}>
          <label><input type="radio" name="alcoholConsumption" value="Yes" checked={formData.alcoholConsumption === 'Yes'} onChange={handleChange} /> Yes</label>
          <label><input type="radio" name="alcoholConsumption" value="No" checked={formData.alcoholConsumption === 'No'} onChange={handleChange} /> No</label>
        </div>

        {/* Tobacco Consumption */}
        <label style={{ gridColumn: 'span 1' }}>Tobacco Consumption:</label>
        <div style={{ gridColumn: 'span 1' }}>
          <label><input type="radio" name="tobaccoConsumption" value="Yes" checked={formData.tobaccoConsumption === 'Yes'} onChange={handleChange} /> Yes</label>
          <label><input type="radio" name="tobaccoConsumption" value="No" checked={formData.tobaccoConsumption === 'No'} onChange={handleChange} /> No</label>
        </div>

        {/* Patient Weight */}
        <label style={{ gridColumn: 'span 1' }}>Patient Weight (kg):</label>
        <input type="number" name="Weight" value={formData.Weight} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        {/* Patient Height */}
        <label style={{ gridColumn: 'span 1' }}>Patient Height (cm):</label>
        <input type="number" name="Height" value={formData.Height} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        {/* BMI (Read-only) */}
        <label style={{ gridColumn: 'span 1' }}>BMI:</label>
        <input type="text" name="BMI" value={formData.BMI} readOnly style={{ gridColumn: 'span 1', backgroundColor: '#e0e0e0' }} />

        {/* Length of Surgery */}
        <label style={{ gridColumn: 'span 1' }}>Length of Surgery (hours):</label>
        <input type="number" name="lengthOfSurgery" value={formData.lengthOfSurgery} onChange={handleChange} style={{ gridColumn: 'span 1' }} />

        {/* SSI Event Occurred */}
        <label style={{ gridColumn: 'span 1' }}>SSI Event Occurred:</label>
        <div style={{ gridColumn: 'span 1' }}>
          <label><input type="radio" name="ssiEventOccurred" value="Yes" checked={formData.ssiEventOccurred === 'Yes'} onChange={handleChange} /> Yes</label>
          <label><input type="radio" name="ssiEventOccurred" value="No" checked={formData.ssiEventOccurred === 'No'} onChange={handleChange} /> No</label>
        </div>

        {/* Date of Event */}
        {formData.ssiEventOccurred === 'Yes' && (
          <>
            <label style={{ gridColumn: 'span 1' }}>If Yes, Date of Event:</label>
            <input
              type="date"
              name="dateOfEvent"
              value={formData.dateOfEvent || ''}
              onChange={handleChange}
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
        </div>
      </form>
    </div>
  );
};

export default SurveillanceForm;