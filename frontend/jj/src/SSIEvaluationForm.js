import React, { useState } from 'react';
import jsPDF from 'jspdf';
const SSIEvaluationForm = () => {
  const [formdata, setformdata] = useState({
    patient_name: '',
    patient_id: '',
    age: '',
    gender: '',
    procedure_name: '',
    procedure_date: '',
    evaluations: Array(26).fill({ yes: false, no: false, remarks: '' }),
  });

  const handleinputchange = (e) => {
    const { name, value } = e.target;
    setformdata({ ...formdata, [name]: value });
  };

  const handleevaluationchange = (index, field, value) => {
    const updatedevaluations = [...formdata.evaluations];

    if (field === 'yes' || field === 'no') {
      updatedevaluations[index] = {
        yes: field === 'yes',
        no: field === 'no',
        remarks: updatedevaluations[index].remarks,
      };
    } else {
      updatedevaluations[index] = { ...updatedevaluations[index], remarks: value };
    }

    setformdata({ ...formdata, evaluations: updatedevaluations });
  };

  const handlesubmit = (e) => {
    e.preventDefault();
    console.log('Form Data Submitted:', formdata);
  };
  const handleDownloadPDF = () => {
    const doc = new jsPDF();
    doc.text('SSI Evaluation Form', 10, 10);

    // Patient details
    doc.text('Patient Name: ' + formdata.patient_name, 10, 20);
    doc.text('Patient ID: ' + formdata.patient_id, 10, 30);
    doc.text('Age: ' + formdata.age, 10, 40);
    doc.text('Gender: ' + formdata.gender, 10, 50);
    doc.text('Procedure: ' + formdata.procedure_name, 10, 60);
    doc.text('Procedure Date: ' + formdata.procedure_date, 10, 70);

    // Evaluations Table
    let yPosition = 80;
    formdata.evaluations.forEach((evaluation, index) => {
      doc.text(`S.NO: ${index + 1} - ${evaluation.remarks || 'No remarks'}`, 10, yPosition);
      yPosition += 10;
      doc.text(`YES: ${evaluation.yes ? 'Yes' : 'No'} | NO: ${evaluation.no ? 'Yes' : 'No'}`, 10, yPosition);
      yPosition += 10;
      if (yPosition > 250) { // Prevent overflow in PDF
        doc.addPage();
        yPosition = 10;
      }
    });

    // Save the PDF
    doc.save('SSI_Evaluation_Form.pdf');
  };

  const formstyles = {
    container: { padding: '20px' },
    title: { marginBottom: '20px' },
    patientdetails: { marginBottom: '20px' },
    formgroup: { marginBottom: '10px' },
    label: { marginRight: '10px', fontWeight: 'bold' },
    input: { padding: '5px', width: '200px' },
    select: { padding: '5px', width: '210px' },
    table: { width: '100%', marginTop: '20px', borderCollapse: 'collapse' },
    th: { padding: '10px', border: '1px solid black', backgroundColor: '#f2f2f2' },
    td: { padding: '10px', border: '1px solid black' },
    submitbtn: { padding: '10px 20px', marginTop: '20px' },
  };

  const procedureoptions = [
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
  const handleDownloadExcel = () => {
    alert("Downloaded as Excel .");
  };

  return (
    <form style={formstyles.container} onSubmit={handlesubmit}>
      <h2 style={formstyles.title}>SSI Evaluation Tool</h2>

      <div style={formstyles.patientdetails}>
        <div style={formstyles.formgroup}>
          <label style={formstyles.label}>Patient's Name:</label>
          <input
            type="text"
            name="patient_name"
            value={formdata.patient_name}
            onChange={handleinputchange}
            required
            style={formstyles.input}
          />
        </div>

        <div style={formstyles.formgroup}>
          <label style={formstyles.label}>Patient's ID:</label>
          <input
            type="text"
            name="patient_id"
            value={formdata.patient_id}
            onChange={handleinputchange}
            required
            style={formstyles.input}
          />
        </div>

        <div style={formstyles.formgroup}>
          <label style={formstyles.label}>Age:</label>
          <input
            type="number"
            name="age"
            value={formdata.age}
            onChange={handleinputchange}
            required
            style={formstyles.input}
          />
        </div>

        <div style={formstyles.formgroup}>
          <label style={formstyles.label}>Gender:</label>
          <select
            name="gender"
            value={formdata.gender}
            onChange={handleinputchange}
            required
            style={formstyles.select}
          >
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div style={formstyles.formgroup}>
          <label style={formstyles.label}>Procedure Name:</label>
          <select
            name="procedure_name"
            value={formdata.procedure_name}
            onChange={handleinputchange}
            required
            style={formstyles.select}
          >
            <option value="">Select Procedure</option>
            {procedureoptions.map((procedure, index) => (
              <option key={index} value={procedure}>{procedure}</option>
            ))}
          </select>
        </div>

        <div style={formstyles.formgroup}>
          <label style={formstyles.label}>Date of Procedure:</label>
          <input
            type="date"
            name="procedure_date"
            value={formdata.procedure_date}
            onChange={handleinputchange}
            required
            style={formstyles.input}
          />
        </div>
      </div>

      {/* Table for SSI Evaluation Items */}
      <table style={formstyles.table}>
        <thead>
          <tr>
            <th style={formstyles.th}>S.NO</th>
            <th style={formstyles.th}>ITEMS</th>
            <th style={formstyles.th}>YES</th>
            <th style={formstyles.th}>NO</th>
            <th style={formstyles.th}>REMARKS</th>
          </tr>
        </thead>
        <tbody>
          {[
            'Administer antimicrobial prophylaxis in accordance with evidence-based standards and guidelines 9',
            'Administer antimicrobial prophylaxis within 1 hour prior to incision (2 hours for vanco and fluoroquinolones)',
            'Select antimicrobial prophylaxis agents on basis of surgical procedure',
            'Select antimicrobial prophylaxis agents on basis of most common SSI pathogens for the procedure',
            'Select antimicrobial prophylaxis agents on basis of published recommendations',
            'Discontinue antibiotics within 24 hours after surgery end time (48 hours for cardiac procedures)',
            'Redose antibiotic at the 3-hour interval in procedures with duration >3 hours',
            'Adjust antimicrobial prophylaxis dose for obese patients (BMI>30)',
            'Not remove hair at operative site unless it interferes with operation',
            'Use razors for hair removal at operative site',
            'Use of clippers or depilatory agent for hair removal at operative site',
            'Use appropriate antiseptic agent and technique for skin preparation',
            'Mechanically prepare the colon (enemas, cathartic agents)',
            'Administer non-absorbable oral antimicrobial agents in divided doses on the day before the operation',
            'Keep OR doors closed during surgery except as needed for passage of equipment, personnel and patient',
            'Maintain immediate post-op normothermia','Protect primary closure incisions with sterile dressing for 24-48 hours',
            'Control blood glucose level during the immediate post-operative period in cardiac procedures',
            'Measure blood glucose level at 6 AM on POD#1 and #2 with procedure day = POD#0 in cardiac procedures',
            'Maintain post-operative blood glucose levels at <200 mg/dL in cardiac procedures',
            'Screen preop blood glucose levels in patients undergoing select elective procedures (e.g. arthroplasties, spinal fusions)',
            'Maintain tight glucose control POD#1 and POD#2 in patients undergoing select elective procedures (e.g. arthroplasties, spinal fusions)',
            'Nasal screen and decolonize S. aureus carriers undergoing elective CABG procedures',
            'Nasal screen and decolonize S. aureus carriers undergoing other elective procedures',
            'Use increased (at least 50%) fraction of inspired oxygen intraoperatively and immediately postoperatively in select procedures',
            'Postpone operation until remote infection has resolved',
          ].map((item, index) => (
            <tr key={index}>
              <td style={formstyles.td}>{index + 1}</td>
              <td style={formstyles.td}>{item}</td>
              <td style={formstyles.td}>
                <input
                  type="radio"
                  name={`evaluation-${index}`}
                  value="yes"
                  checked={formdata.evaluations[index].yes}
                  onChange={() => handleevaluationchange(index, 'yes', true)}
                />
              </td>
              <td style={formstyles.td}>
                <input
                  type="radio"
                  name={`evaluation-${index}`}
                  value="no"
                  checked={formdata.evaluations[index].no}
                  onChange={() => handleevaluationchange(index, 'no', true)}
                />
              </td>
              <td style={formstyles.td}>
                <input
                  type="text"
                  name={`remarks-${index}`}
                  value={formdata.evaluations[index].remarks}
                  onChange={(e) => handleevaluationchange(index, 'remarks', e.target.value)}
                  style={formstyles.input}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
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
        onClick={handleDownloadPDF}
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
    </form>
  
  );
  
    };
    
export default SSIEvaluationForm;
