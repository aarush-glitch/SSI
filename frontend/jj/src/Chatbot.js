import ReactMarkdown from "react-markdown";
import React, { useState, useRef, useEffect } from "react";
import { FaRobot, FaPaperPlane } from "react-icons/fa";
import "./Chatbot.css";

const Chatbot = () => {
  const [awaitingMedicalTerm, setAwaitingMedicalTerm] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [checkedTasks, setCheckedTasks] = useState([]); // Track ticked checklist tasks
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! I'm MediBuddy. I can help you with Surgical Site Infection (SSI) detection and preparation. Type anything to get started!",
    },
  ]);
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  // Hardcoded dictionary of SSI-related medical terms
  const medicalTerms = {
    abscess: "An abscess is a pocket of pus caused by a bacterial infection, often appearing as a swollen, painful area. In SSI, it may form near the surgical site and requires medical attention, possibly drainage or antibiotics.",
    seroma: "A seroma is a buildup of clear fluid under the skin at the surgical site, often after procedures like mastectomy. It may cause swelling but usually resolves on its own; large seromas may need drainage.",
    dehiscence: "Dehiscence is when a surgical wound partially or fully opens along the incision, increasing infection risk. It’s often linked to poor healing, obesity, or strain. Immediate medical care is needed.",
    erythema: "Erythema refers to redness of the skin, often around a surgical incision, which may signal irritation or infection. Monitor for warmth, swelling, or fever and consult a doctor if it worsens.",
    hematoma: "A hematoma is a collection of blood under the skin, common after surgery. In SSIs, it may increase infection risk if untreated.",
    necrosis: "Necrosis is the death of tissue, sometimes occurring at a surgical site due to poor blood supply or infection. It requires urgent medical care.",
    fistula: "A fistula is an abnormal connection between organs or tissues, sometimes forming after surgery due to infection or poor healing. It may cause leakage and needs medical evaluation.",
    purulent: "Purulent describes pus-filled discharge from a surgical site, often a sign of infection. It may be thick, yellow, or green and requires immediate medical attention.",
    cellulitis: "Cellulitis is a bacterial skin infection that can occur around a surgical site, causing redness, swelling, and pain. It needs prompt antibiotic treatment.",
    sepsis: "Sepsis is a life-threatening infection response that can result from an SSI, causing fever, rapid heart rate, and organ dysfunction. Seek emergency care immediately.",
    anastomosis: "Anastomosis is the surgical connection of two structures, like blood vessels or intestines. In SSIs, leaks at the site can lead to infection and require urgent medical attention.",
    edema: "Edema is swelling caused by fluid buildup, often around a surgical site. In SSIs, it may indicate infection or poor healing and should be monitored.",
    serosanguinous: "Serosanguinous describes a type of wound drainage that is thin and pink or reddish, often normal in early healing. Persistent or foul-smelling drainage may indicate an SSI.",
    induration: "Induration is the hardening of tissue around a surgical site, which may signal infection or inflammation. It requires medical evaluation if accompanied by redness or pain.",
    fasciitis: "Fasciitis, such as necrotizing fasciitis, is a severe bacterial infection of the tissue layers, sometimes linked to SSIs. It causes rapid pain, swelling, and fever and is a medical emergency.",
  };

  const suggestedTerms = Object.keys(medicalTerms);

  const surgeryTypes = [
    "Abdominal aortic aneurysm repair",
    "Limb amputation",
    "Appendix surgery",
    "Shunt for dialysis",
    "Bile duct, liver, or pancreas surgery",
    "Carotid endarterectomy",
    "Gallbladder surgery",
    "Colon surgery",
    "Cesarean section",
    "Gastric surgery",
    "Heart transplant",
    "Abdominal hysterectomy",
    "Kidney transplant",
    "Laminectomy",
    "Liver transplant",
    "Neck surgery",
    "Kidney surgery",
    "Ovarian surgery",
    "Prostate surgery",
    "Rectal surgery",
    "Small bowel surgery",
    "Spleen surgery",
    "Thoracic surgery",
    "Thyroid and parathyroid surgery",
    "Vaginal hysterectomy",
    "Exploratory laparotomy",
    "Breast surgery",
    "Cardiac surgery",
    "Coronary artery bypass graft",
    "Craniotomy",
    "Spinal fusion",
    "Open reduction of fracture",
    "Hip prosthesis",
    "Knee prosthesis",
    "Pacemaker surgery",
    "Peripheral vascular bypass surgery",
    "Ventricular shunt",
    "Herniorrhaphy",
    "Laparotomy",
  ];

  const ssiGuidelines = {
    "Abdominal aortic aneurysm repair": `
      **Why it’s unique**: Involves a large abdominal or endovascular incision with a graft, risking deep infections near major blood vessels.
      **What to watch for**:
      - Redness, warmth, or pus at the abdominal incision.
      - Fever, chills, or groin pain (for endovascular approaches).
      - New abdominal pain or pulsating sensation (could indicate graft issues).
      **Personalized tips**:
      - If you have vascular disease, monitor for leg swelling or discoloration.
      - Avoid heavy lifting to protect the incision.
      **Action**: Contact your vascular surgeon immediately for fever or incision changes, as graft infections are serious.
    `,
    "Limb amputation": `
      **Why it’s unique**: High risk due to poor circulation (common in amputees) and stump exposure to pressure or prosthetics.
      **What to watch for**:
      - Stump redness, swelling, or foul-smelling discharge.
      - Increased stump pain or phantom pain worsening.
      - Fever or poor wound healing.
      **Personalized tips**:
      - **Diabetics**: Check blood sugar daily; poor control delays healing.
      - Keep the stump clean and dry; use a mirror to inspect.
      **Action**: Call your surgeon or prosthetist for stump changes. Infections may need imaging or revision surgery.
    `,
    "Appendix surgery": `
      **Why it’s unique**: Often laparoscopic, with small incisions, but open surgery carries higher risk of organ-space SSIs (e.g., abscess).
      **What to watch for**:
      - Redness or discharge at incision(s), especially laparoscopic ports.
      - Persistent abdominal pain, bloating, or nausea.
      - Fever beyond 48 hours post-op.
      **Personalized tips**:
      - If obese, check all port sites carefully.
      - Resume activity gradually to avoid wound stress.
      **Action**: Contact your surgeon for worsening pain or fever; imaging may be needed for abscesses.
    `,
    "Shunt for dialysis": `
      **Why it’s unique**: Involves a vascular access site, with high infection risk due to repeated use and compromised immunity in dialysis patients.
      **What to watch for**:
      - Redness, swelling, or pus at the shunt site.
      - Fever, chills, or pain during dialysis.
      - Reduced shunt flow or clotting signs.
      **Personalized tips**:
      - Keep the shunt site clean and dry; avoid trauma.
      - Monitor for systemic symptoms like fatigue or confusion.
      **Action**: Contact your nephrologist or surgeon immediately for shunt issues or fever.
    `,
    "Bile duct, liver, or pancreas surgery": `
      **Why it’s unique**: Complex procedures with deep incisions, risking organ-space SSIs like abscesses due to bile or pancreatic fluid leakage.
      **What to watch for**:
      - Yellowing skin (jaundice), dark urine, or fever.
      - Abdominal pain, swelling, or pus at incision.
      - Persistent nausea or vomiting.
      **Personalized tips**:
      - Monitor drains (if present) for cloudy or foul-smelling output.
      - Avoid fatty foods to reduce strain on healing tissues.
      **Action**: Call your surgeon for fever, jaundice, or drain changes; imaging may be required.
    `,
    "Carotid endarterectomy": `
      **Why it’s unique**: Neck incision near major arteries, with risk of superficial or deep SSIs affecting vascular structures.
      **What to watch for**:
      - Neck redness, swelling, or discharge.
      - Fever, neck pain, or difficulty swallowing.
      - Stroke-like symptoms (e.g., weakness, vision changes).
      **Personalized tips**:
      - Avoid neck strain or tight collars.
      - If you smoke, quit to improve healing.
      **Action**: Contact your vascular surgeon immediately for incision changes or neurological symptoms.
    `,
    "Gallbladder surgery": `
      **Why it’s unique**: Typically laparoscopic, but open surgery increases SSI risk due to bile leakage or obesity-related complications.
      **What to watch for**:
      - Redness or pus at laparoscopic port sites or main incision.
      - Fever, right upper abdominal pain, or nausea.
      - Yellowing skin or eyes (jaundice).
      **Personalized tips**:
      - If obese, inspect all port sites daily.
      - Avoid heavy meals to prevent wound stress.
      **Action**: Call your surgeon for fever, jaundice, or worsening pain; imaging may be needed.
    `,
    "Colon surgery": `
      **Why it’s unique**: High SSI risk due to bacterial load in the colon and potential for anastomotic leaks.
      **What to watch for**:
      - Abdominal redness, swelling, or discharge.
      - Fever, severe abdominal pain, or lack of bowel movements.
      - Foul-smelling wound drainage.
      **Personalized tips**:
      - Monitor for signs of dehydration or ileus (bowel obstruction).
      - Follow dietary restrictions to aid healing.
      **Action**: Contact your surgeon immediately for fever, no bowel activity, or drainage changes.
    `,
    "Cesarean section": `
      **Why it’s unique**: Abdominal incision with risk of superficial SSIs, compounded by hormonal changes and postpartum recovery.
      **What to watch for**:
      - Redness, warmth, or pus at the incision.
      - Fever, uterine tenderness, or foul-smelling lochia.
      - Increased pain not relieved by medication.
      **Personalized tips**:
      - Avoid heavy lifting or straining during recovery.
      - Keep the incision dry, especially after breastfeeding.
      **Action**: Call your obstetrician for fever, heavy bleeding, or incision changes.
    `,
    "Gastric surgery": `
      **Why it’s unique**: Involves stomach incisions or bypass, with high SSI risk due to obesity or malnutrition.
      **What to watch for**:
      - Redness, swelling, or discharge at incision.
      - Fever, nausea, or inability to tolerate food.
      - Abdominal pain or bloating.
      **Personalized tips**:
      - Follow dietary guidelines to prevent wound stress.
      - If obese, monitor incision folds carefully.
      **Action**: Contact your surgeon for fever, vomiting, or incision changes; imaging may be needed.
    `,
    "Heart transplant": `
      **Why it’s unique**: Sternotomy and immunosuppression increase deep SSI risk, including mediastinitis.
      **What to watch for**:
      - Chest redness, swelling, or pus at sternum.
      - Fever, chest pain, or shortness of breath.
      - Clicking or instability in sternum.
      **Personalized tips**:
      - Take immunosuppressants as prescribed; report signs of rejection.
      - Avoid crowds to reduce infection risk.
      **Action**: Call your transplant team immediately for fever or chest symptoms.
    `,
    "Abdominal hysterectomy": `
      **Why it’s unique**: Pelvic surgery with risk of deep or organ-space SSIs, especially in obese patients.
      **What to watch for**:
      - Abdominal or vaginal redness, discharge, or odor.
      - Fever, pelvic pain, or heavy bleeding.
      - Difficulty urinating or bowel changes.
      **Personalized tips**:
      - Avoid sexual activity or heavy lifting during recovery.
      - Monitor for urinary symptoms, which may indicate infection.
      **Action**: Contact your gynecologist for fever, bleeding, or incision changes.
    `,
    "Kidney transplant": `
      **Why it’s unique**: Immunosuppression and pelvic incision increase SSI risk, including deep infections near the graft.
      **What to watch for**:
      - Redness, swelling, or pus at incision.
      - Fever, decreased urine output, or graft tenderness.
      - Systemic symptoms like fatigue or chills.
      **Personalized tips**:
      - Take immunosuppressants as prescribed; report rejection signs.
      - Stay hydrated to support kidney function.
      **Action**: Call your transplant team immediately for fever or graft symptoms.
    `,
    "Laminectomy": `
      **Why it’s unique**: Spinal surgery with risk of deep SSIs affecting vertebrae or hardware.
      **What to watch for**:
      - Back redness, swelling, or discharge at incision.
      - Fever, worsening back pain, or neurological changes (e.g., numbness).
      - Wound drainage or hardware instability.
      **Personalized tips**:
      - Avoid bending or twisting to protect the incision.
      - If diabetic, control blood sugar to aid healing.
      **Action**: Contact your neurosurgeon for fever, neurological changes, or drainage.
    `,
    "Liver transplant": `
      **Why it’s unique**: Large abdominal incision and immunosuppression increase risk of deep SSIs or abscesses.
      **What to watch for**:
      - Abdominal redness, swelling, or pus.
      - Fever, jaundice, or dark urine.
      - Abdominal pain or drain output changes.
      **Personalized tips**:
      - Take immunosuppressants as prescribed; report rejection signs.
      - Avoid alcohol to support liver healing.
      **Action**: Call your transplant team immediately for fever, jaundice, or incision changes.
    `,
    "Neck surgery": `
      **Why it’s unique**: Small incisions but high visibility, with risk of superficial SSIs or deep infections near vital structures.
      **What to watch for**:
      - Neck redness, swelling, or discharge.
      - Fever, neck stiffness, or difficulty swallowing.
      - Voice changes or breathing issues.
      **Personalized tips**:
      - Avoid neck strain or tight clothing.
      - Monitor for airway symptoms, which are urgent.
      **Action**: Contact your surgeon for fever, swallowing issues, or incision changes.
    `,
    "Kidney surgery": `
      **Why it’s unique**: Flank or abdominal incision with risk of deep SSIs, especially in patients with kidney disease.
      **What to watch for**:
      - Flank redness, swelling, or pus.
      - Fever, decreased urine output, or flank pain.
      - Blood in urine or systemic symptoms.
      **Personalized tips**:
      - Stay hydrated to support kidney function.
      - Monitor for urinary tract infection signs.
      **Action**: Call your urologist for fever, urine changes, or incision issues.
    `,
    "Ovarian surgery": `
      **Why it’s unique**: Pelvic or abdominal incision with risk of organ-space SSIs, especially in cancer patients.
      **What to watch for**:
      - Abdominal redness, swelling, or discharge.
      - Fever, pelvic pain, or abnormal vaginal bleeding.
      - Nausea or bowel changes.
      **Personalized tips**:
      - Avoid heavy lifting or straining.
      - Monitor for chemotherapy-related immune suppression.
      **Action**: Contact your gynecologist for fever, bleeding, or incision changes.
    `,
    "Prostate surgery": `
      **Why it’s unique**: Pelvic or perineal incision with risk of urinary tract-related SSIs.
      **What to watch for**:
      - Perineal or abdominal redness, swelling, or pus.
      - Fever, difficulty urinating, or blood in urine.
      - Foul-smelling urine or pelvic pain.
      **Personalized tips**:
      - Monitor catheter (if present) for blockages or infection.
      - Stay hydrated to reduce UTI risk.
      **Action**: Call your urologist for fever, urinary issues, or incision changes.
    `,
    "Rectal surgery": `
      **Why it’s unique**: High SSI risk due to bacterial load and potential for anastomotic leaks or perineal infections.
      **What to watch for**:
      - Perineal or abdominal redness, swelling, or discharge.
      - Fever, rectal pain, or lack of bowel movements.
      - Foul-smelling drainage or bleeding.
      **Personalized tips**:
      - Follow dietary restrictions to aid healing.
      - Monitor for signs of fistula or abscess.
      **Action**: Contact your surgeon for fever, no bowel activity, or drainage changes.
    `,
    "Small bowel surgery": `
      **Why it’s unique**: High SSI risk due to bacterial load and potential for leaks at anastomotic sites.
      **What to watch for**:
      - Abdominal redness, swelling, or pus.
      - Fever, severe abdominal pain, or vomiting.
      - Lack of bowel sounds or distension.
      **Personalized tips**:
      - Monitor for dehydration or ileus.
      - Follow nutritional guidelines to support healing.
      **Action**: Contact your surgeon for fever, vomiting, or incision changes.
    `,
    "Spleen surgery": `
      **Why it’s unique**: Abdominal incision with risk of deep SSIs, compounded by immune compromise post-splenectomy.
      **What to watch for**:
      - Abdominal redness, swelling, or discharge.
      - Fever, left upper quadrant pain, or fatigue.
      - Signs of systemic infection (e.g., chills).
      **Personalized tips**:
      - Get vaccinated post-surgery to prevent infections.
      - Avoid crowds to reduce infection risk.
      **Action**: Call your surgeon for fever, pain, or incision changes.
    `,
    "Thoracic surgery": `
      **Why it’s unique**: Chest incision with risk of deep SSIs like empyema, especially in lung procedures.
      **What to watch for**:
      - Chest redness, swelling, or pus.
      - Fever, chest pain, or shortness of breath.
      - Foul-smelling drainage from chest tubes.
      **Personalized tips**:
      - Avoid smoking to improve lung healing.
      - Monitor chest tube output (if present).
      **Action**: Contact your thoracic surgeon for fever, breathing issues, or drainage changes.
    `,
    "Thyroid and parathyroid surgery": `
      **Why it’s unique**: Neck incision with risk of superficial SSIs or deep infections near vital structures.
      **What to watch for**:
      - Neck redness, swelling, or discharge.
      - Fever, neck pain, or voice changes.
      - Difficulty swallowing or breathing.
      **Personalized tips**:
      - Avoid neck strain or tight collars.
      - Monitor calcium levels if parathyroid was involved.
      **Action**: Contact your surgeon for fever, voice changes, or incision issues.
    `,
    "Vaginal hysterectomy": `
      **Why it’s unique**: Vaginal approach reduces skin SSIs, but pelvic infections are a risk.
      **What to watch for**:
      - Vaginal discharge with foul odor or pus.
      - Fever, pelvic pain, or heavy bleeding.
      - Difficulty urinating or bowel changes.
      **Personalized tips**:
      - Avoid sexual activity or douching during recovery.
      - Monitor for urinary symptoms.
      **Action**: Contact your gynecologist for fever, bleeding, or discharge changes.
    `,
    "Exploratory laparotomy": `
      **Why it’s unique**: Large abdominal incision with high SSI risk due to prolonged surgery or contamination.
      **What to watch for**:
      - Abdominal redness, swelling, or pus.
      - Fever, severe abdominal pain, or distension.
      - Persistent nausea or lack of bowel movements.
      **Personalized tips**:
      - Monitor drains (if present) for infection signs.
      - Follow dietary restrictions to aid recovery.
      **Action**: Contact your surgeon for fever, pain, or drainage changes.
    `,
    "Breast surgery": `
      **Why it’s unique**: Risk of superficial SSIs, especially in mastectomy with reconstruction or lymph node dissection.
      **What to watch for**:
      - Breast redness, swelling, or discharge.
      - Fever, breast pain, or seroma formation.
      - Arm swelling (lymphedema risk).
      **Personalized tips**:
      - Avoid tight bras or arm strain.
      - Monitor for chemotherapy-related immune issues.
      **Action**: Contact your surgeon for fever, swelling, or incision changes.
    `,
    "Cardiac surgery": `
      **Why it’s unique**: Sternotomy with risk of deep SSIs like mediastinitis, especially in bypass or valve procedures.
      **What to watch for**:
      - Chest redness, swelling, or pus.
      - Fever, chest pain, or sternal instability.
      - Shortness of breath or irregular heartbeat.
      **Personalized tips**:
      - Avoid heavy lifting to protect the sternum.
      - If diabetic, control blood sugar to aid healing.
      **Action**: Contact your cardiologist or surgeon for fever or chest symptoms.
    `,
    "Coronary artery bypass graft": `
      **Why it’s unique**: Sternotomy and leg vein harvest sites increase SSI risk, including deep infections.
      **What to watch for**:
      - Chest or leg incision redness, swelling, or pus.
      - Fever, chest pain, or leg swelling.
      - Sternal clicking or instability.
      **Personalized tips**:
      - Elevate legs to reduce swelling if veins were harvested.
      - Avoid smoking to improve healing.
      **Action**: Contact your cardiac surgeon for fever, leg, or chest symptoms.
    `,
    "Craniotomy": `
      **Why it’s unique**: Skull incision with risk of deep SSIs like meningitis or abscess, especially near brain tissue.
      **What to watch for**:
      - Scalp redness, swelling, or discharge.
      - Fever, headache, or neurological changes (e.g., seizures).
      - Clear fluid leakage from incision.
      **Personalized tips**:
      - Avoid scalp trauma or scratching.
      - Monitor for confusion or vision changes.
      **Action**: Contact your neurosurgeon immediately for fever or neurological symptoms.
    `,
    "Spinal fusion": `
      **Why it’s unique**: Deep incisions with hardware increase risk of SSIs affecting vertebrae or implants.
      **What to watch for**:
      - Back redness, swelling, or discharge.
      - Fever, worsening back pain, or neurological changes.
      - Hardware loosening or wound drainage.
      **Personalized tips**:
      - Avoid bending or heavy lifting.
      - If obese, monitor incision carefully.
      **Action**: Contact your neurosurgeon for fever, neurological changes, or drainage.
    `,
    "Open reduction of fracture": `
      **Why it’s unique**: Orthopedic hardware and trauma increase SSI risk, including deep infections like osteomyelitis.
      **What to watch for**:
      - Redness, swelling, or pus at incision.
      - Fever, bone pain, or reduced mobility.
      - Wound drainage or hardware issues.
      **Personalized tips**:
      - Keep the limb elevated to reduce swelling.
      - Avoid weight-bearing until cleared.
      **Action**: Contact your orthopedic surgeon for fever, pain, or drainage.
    `,
    "Hip prosthesis": `
      **Why it’s unique**: Deep joint surgery with hardware increases risk of prosthetic joint infections.
      **What to watch for**:
      - Hip redness, swelling, or discharge.
      - Fever, hip pain, or difficulty walking.
      - Wound drainage or joint instability.
      **Personalized tips**:
      - Follow physical therapy to avoid stress on incision.
      - If diabetic, control blood sugar.
      **Action**: Contact your orthopedic surgeon for fever, pain, or drainage.
    `,
    "Knee prosthesis": `
      **Why it’s unique**: Deep joint surgery with hardware increases risk of prosthetic joint infections.
      **What to watch for**:
      - Knee redness, swelling, or pus.
      - Fever, knee pain, or reduced range of motion.
      - Wound drainage or joint instability.
      **Personalized tips**:
      - Use assistive devices to avoid falls.
      - Keep the knee elevated to reduce swelling.
      **Action**: Contact your orthopedic surgeon for fever, pain, or drainage.
    `,
    "Pacemaker surgery": `
      **Why it’s unique**: Chest incision with implanted device increases risk of pocket infections.
      **What to watch for**:
      - Chest redness, swelling, or discharge near device.
      - Fever, chest pain, or device malfunction.
      - Swelling or pain at insertion site.
      **Personalized tips**:
      - Avoid arm strain on the device side.
      - Monitor for irregular heart rhythms.
      **Action**: Contact your cardiologist for fever, pain, or device issues.
    `,
    "Peripheral vascular bypass surgery": `
      **Why it’s unique**: Multiple incisions (e.g., groin, leg) with grafts increase SSI risk, especially in poor circulation.
      **What to watch for**:
      - Redness, swelling, or pus at incision sites.
      - Fever, leg pain, or reduced pulse in limb.
      - Graft site swelling or drainage.
      **Personalized tips**:
      - Elevate legs to reduce swelling.
      - If diabetic, control blood sugar.
      **Action**: Contact your vascular surgeon for fever, limb changes, or drainage.
    `,
    "Ventricular shunt": `
      **Why it’s unique**: Brain or abdominal incisions with tubing increase risk of SSIs like meningitis or peritonitis.
      **What to watch for**:
      - Scalp or abdominal redness, swelling, or discharge.
      - Fever, headache, or abdominal pain.
      - Shunt malfunction (e.g., seizures, vomiting).
      **Personalized tips**:
      - Avoid scalp trauma or pressure on shunt.
      - Monitor for neurological changes.
      **Action**: Contact your neurosurgeon immediately for fever or shunt issues.
    `,
    "Herniorrhaphy": `
      **Why it’s unique**: Inguinal or abdominal incision with mesh increases SSI risk, especially in obese patients.
      **What to watch for**:
      - Groin or abdominal redness, swelling, or pus.
      - Fever, groin pain, or bulge recurrence.
      - Wound drainage or mesh discomfort.
      **Personalized tips**:
      - Avoid heavy lifting or straining.
      - If obese, monitor incision folds.
      **Action**: Contact your surgeon for fever, pain, or incision changes.
    `,
    "Laparotomy": `
      **Why it’s unique**: Large abdominal incision with high SSI risk due to prolonged surgery or contamination.
      **What to watch for**:
      - Abdominal redness, swelling, or pus.
      - Fever, severe abdominal pain, or distension.
      - Persistent nausea or lack of bowel movements.
      **Personalized tips**:
      - Monitor drains (if present) for infection signs.
      - Follow dietary restrictions to aid recovery.
      **Action**: Contact your surgeon for fever, pain, or drainage changes.
    `,
  };

  const generalAdvice = `
    **General Advice for All Patients**:
    - **Wound care**: Follow your surgeon’s instructions (e.g., keep dry, avoid unauthorized creams). Change dressings as directed.
    - **Antibiotics**: Complete prescribed courses; report side effects like diarrhea, which can hide SSI clues.
    - **Lifestyle**: Eat nutritiously, stay hydrated, and avoid alcohol to support immunity.
    - **Documentation**: Photograph incision changes (date-stamped) for your doctor.
    - **Trust instincts**: Don’t dismiss symptoms as “normal recovery.” When in doubt, call your healthcare team.
    _Disclaimer: MediBuddy is not a doctor; please consult one for medical advice._
  `;

  // Preoperative Checklist tasks (based on provided measures)
  const checklistTasks = {
    "confirm patient identity": {
      name: "Confirm patient identity, procedure, and site",
      instruction: "Confirmed patient identity, procedure, and incision site via surgical time-out. Ensures correct surgery.",
    },
    "conduct mrsa screening": {
      name: "Conduct MRSA screening and decolonization",
      instruction: "Completed MRSA screening and decolonization if needed. Reduces infection risk.",
    },
    "assess allergies": {
      name: "Assess allergies to antiseptics/antibiotics",
      instruction: "Assessed patient allergies to antiseptics and antibiotics. Prevents adverse reactions.",
    },
    "instruct chlorhexidine bath": {
      name: "Instruct chlorhexidine bath before surgery",
      instruction: "Instructed patient to bathe with 4% chlorhexidine soap. Lowers skin bacteria.",
    },
    "remove jewelry": {
      name: "Remove jewelry and obstructive items",
      instruction: "Removed jewelry, nail polish, and obstructive clothing. Ensures clean surgical field.",
    },
    "perform fire risk assessment": {
      name: "Perform fire risk assessment in operating room.",
      instruction: "Completed fire risk assessment in operating room. Enhances safety.",
    },
    "administer antibiotics": {
      name: "Administer prophylactic antibiotics timely",
      instruction: "Administered antibiotics within 60 min (120 min for vancomycin/fluoroquinolones). Prevents SSI.",
    },
    "control blood glucose": {
      name: "Control blood glucose in diabetics",
      instruction: "Ensured blood glucose <150 mg/dL in diabetics. Supports healing.",
    },
    "consider minimally invasive": {
      name: "Consider minimally invasive alternatives",
      instruction: "Evaluated minimally invasive options. May reduce SSI risk.",
    },
  };

  const checklistTaskNames = Object.values(checklistTasks).map((task) => task.name);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleAutoReply = (userInput) => {
    const normalized = userInput.toLowerCase().trim();

    if (["hi", "hello", "hey", "start"].includes(normalized)) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "How can I assist you today?",
          type: "options",
          options: [
            "Guidelines for SSI Detection",
            "Search Medical Terms",
            "Preoperative Checklist",
          ],
        },
      ]);
      setAwaitingMedicalTerm(false);
      return true;
    }

    if (userInput === "Guidelines for SSI Detection") {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Sure. Can you tell me the type of surgery performed? Here are a few common examples:",
          type: "options",
          options: surgeryTypes,
        },
      ]);
      setAwaitingMedicalTerm(false);
      return true;
    }

    if (surgeryTypes.includes(userInput)) {
      const guideline = ssiGuidelines[userInput] || "No specific guidelines available for this surgery.";
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `**SSI Detection Guidelines for ${userInput}**:\n${guideline}\n${generalAdvice}`,
        },
        {
          sender: "bot",
          text: "Would you like to choose another option or exit?",
          type: "options",
          options: [
            "Choose Another Surgery",
            "Search Medical Terms",
            "Preoperative Checklist",
            "Exit",
          ],
        },
      ]);
      setAwaitingMedicalTerm(false);
      return true;
    }

    if (userInput === "Choose Another Surgery") {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Please choose a surgery type:",
          type: "options",
          options: surgeryTypes,
        },
      ]);
      setAwaitingMedicalTerm(false);
      return true;
    }

    if (userInput === "Search Medical Terms") {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Please enter a medical term (e.g., abscess, hematoma, cellulitis) to learn more about it.",
        },
      ]);
      setAwaitingMedicalTerm(true);
      return true;
    }

    if (userInput === "Preoperative Checklist") {
      const checklistText = "**Preoperative Checklist**\n" +
        Object.values(checklistTasks)
          .map((task) =>
            checkedTasks.includes(task.name)
              ? `- [x] ${task.name}`
              : `- [ ] ${task.name}`
          )
          .join("\n");
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: checklistText,
        },
        {
          sender: "bot",
          text: "Select a task to mark as completed or view options:",
          type: "options",
          options: [...checklistTaskNames, "View Checklist", "Main Menu", "Exit"],
        },
      ]);
      setAwaitingMedicalTerm(false);
      return true;
    }

    // Handle checklist task selection
    if (checklistTaskNames.includes(userInput)) {
      const taskKey = Object.keys(checklistTasks).find(
        (key) => checklistTasks[key].name === userInput
      );
      const task = checklistTasks[taskKey];
      if (!checkedTasks.includes(task.name)) {
        setCheckedTasks((prev) => [...prev, task.name]);
      }
      const checklistText = "**Preoperative Checklist**\n" +
        Object.values(checklistTasks)
          .map((t) =>
            checkedTasks.includes(t.name) || t.name === task.name
              ? `- [x] ${t.name}`
              : `- [ ] ${t.name}`
          )
          .join("\n");
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `Confirmed! ${task.instruction}`,
        },
        {
          sender: "bot",
          text: checklistText,
        },
        {
          sender: "bot",
          text: "Select another task to mark as completed or view options:",
          type: "options",
          options: [...checklistTaskNames, "View Checklist", "Main Menu", "Exit"],
        },
      ]);
      return true;
    }

    if (userInput === "View Checklist") {
      const checklistText = "**Preoperative Checklist**\n" +
        Object.values(checklistTasks)
          .map((task) =>
            checkedTasks.includes(task.name)
              ? `- [x] ${task.name}`
              : `- [ ] ${task.name}`
          )
          .join("\n");
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: checklistText,
        },
        {
          sender: "bot",
          text: "Select a task to mark as completed or view options:",
          type: "options",
          options: [...checklistTaskNames, "View Checklist", "Main Menu", "Exit"],
        },
      ]);
      return true;
    }

    if (userInput === "Exit") {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Goodbye! Feel free to return anytime for more assistance.",
        },
      ]);
      setIsOpen(false);
      setAwaitingMedicalTerm(false);
      setCheckedTasks([]); // Reset checklist
      return true;
    }

    if (userInput === "Search Another Term") {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Please enter another medical term (e.g., abscess, hematoma, cellulitis).",
        },
      ]);
      setAwaitingMedicalTerm(true);
      return true;
    }

    if (userInput === "Main Menu") {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "How can I assist you today?",
          type: "options",
          options: [
            "Guidelines for SSI Detection",
            "Search Medical Terms",
            "Preoperative Checklist",
          ],
        },
      ]);
      setAwaitingMedicalTerm(false);
      setCheckedTasks([]); // Reset checklist
      return true;
    }

    return false;
  };

  const sendMessage = async (customInput = null) => {
    const userText = customInput || input;
    if (!userText.trim()) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Please enter a valid message or term." },
      ]);
      return;
    }

    // Check if input is a control command first
    const intercepted = handleAutoReply(userText);
    if (intercepted) {
      setInput("");
      return;
    }

    // Add user message only for non-control inputs
    setMessages((prev) => [...prev, { sender: "user", text: userText }]);

    // Process medical term if awaiting one
    if (awaitingMedicalTerm) {
      const term = userText.trim().toLowerCase();

      // Check if term exists in hardcoded dictionary
      if (medicalTerms[term]) {
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: medicalTerms[term] },
          {
            sender: "bot",
            text: "Would you like to search another term or return to the main menu?",
            type: "options",
            options: ["Search Another Term", "Main Menu", "Exit"],
          },
        ]);
        setAwaitingMedicalTerm(false);
        setInput("");
        return;
      }

      // Validate input to avoid non-medical terms
      const nonMedicalWords = ["apple", "car", "house", "book", "tree"];
      if (nonMedicalWords.some((word) => term.includes(word))) {
        setMessages((prev) => [
          ...prev,
          {
            sender: "bot",
            text: `'${userText}' doesn’t seem to be a medical term. Please enter a medical term (e.g., hematoma, necrosis).`,
          },
          {
            sender: "bot",
            text: "Try again or return to the main menu.",
            type: "options",
            options: ["Search Another Term", "Main Menu", "Exit"],
          },
        ]);
        setAwaitingMedicalTerm(false);
        setInput("");
        return;
      }

      // Try NLM API first
      try {
        setIsTyping(true);
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: `Searching for "${userText}"...` },
        ]);

        const apiTerm = userText.trim();
        const nlmResponse = await fetch(
          `https://clinicaltables.nlm.nih.gov/api/conditions/v3/search?terms=${encodeURIComponent(apiTerm)}&df=primary_name,info_link_data,synonyms`
        );
        if (!nlmResponse.ok) {
          throw new Error(`NLM HTTP error! Status: ${nlmResponse.status}`);
        }
        const nlmData = await nlmResponse.json();
        console.log("NLM API Response:", nlmData);

        if (nlmData[0] > 0 && nlmData[2]?.primary_name?.length > 0) {
          const [primaryName, infoLink, synonyms] = [
            nlmData[2].primary_name[0],
            nlmData[2].info_link_data?.[0] || "",
            nlmData[2].synonyms?.[0] || "",
          ];
          const definition = infoLink
            ? `**${primaryName}**: See more at [MedlinePlus](${infoLink}). Synonyms: ${synonyms || "None"}.`
            : `**${primaryName}**: A medical condition. Synonyms: ${synonyms || "None"}.`;
          setMessages((prev) => [
            ...prev,
            { sender: "bot", text: definition },
            {
              sender: "bot",
              text: "Would you like to search another term or return to the main menu?",
              type: "options",
              options: ["Search Another Term", "Main Menu", "Exit"],
            },
          ]);
          setIsTyping(false);
          setAwaitingMedicalTerm(false);
          setInput("");
          return;
        }

        // Fall back to Wikipedia API if NLM returns no results
        try {
          const wikiResponse = await fetch(
            `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(apiTerm)}`
          );
          if (!wikiResponse.ok) {
            throw new Error(`Wikipedia HTTP error! Status: ${wikiResponse.status}`);
          }
          const wikiData = await wikiResponse.json();
          console.log("Wikipedia API Response:", wikiData);

          if (wikiData.extract) {
            const cleanExtract = wikiData.extract.replace(/\[.*?\]/g, "");
            const wikiUrl = `https://en.wikipedia.org/wiki/${encodeURIComponent(wikiData.title)}`;
            setMessages((prev) => [
              ...prev,
              {
                sender: "bot",
                text: `**${wikiData.title}**: ${cleanExtract.substring(0, 300)}... [Source: Wikipedia](${wikiUrl}). Consult a doctor for medical advice.`,
              },
              {
                sender: "bot",
                text: "Would you like to search another term or return to the main menu?",
                type: "options",
                options: ["Search Another Term", "Main Menu", "Exit"],
              },
            ]);
          } else {
            setMessages((prev) => [
              ...prev,
              {
                sender: "bot",
                text: `No information found for "${userText}". Try a term like cellulitis or sepsis.`,
              },
              {
                sender: "bot",
                text: "Try again or return to the main menu.",
                type: "options",
                options: ["Search Another Term", "Main Menu", "Exit"],
              },
            ]);
          }
        } catch (wikiError) {
          console.error("Wikipedia API Error:", wikiError.message);
          setMessages((prev) => [
            ...prev,
            {
              sender: "bot",
              text: `No information found for "${userText}". Try a term like cellulitis or sepsis.`,
            },
            {
              sender: "bot",
              text: "Try again or return to the main menu.",
              type: "options",
              options: ["Search Another Term", "Main Menu", "Exit"],
            },
          ]);
        }
      } catch (nlmError) {
        console.error("NLM API Error:", nlmError.message);
        // Try Wikipedia API on NLM error
        try {
          const wikiResponse = await fetch(
            `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(userText.trim())}`
          );
          if (!wikiResponse.ok) {
            throw new Error(`Wikipedia HTTP error! Status: ${wikiResponse.status}`);
          }
          const wikiData = await wikiResponse.json();
          console.log("Wikipedia API Response:", wikiData);

          if (wikiData.extract) {
            const cleanExtract = wikiData.extract.replace(/\[.*?\]/g, "");
            const wikiUrl = `https://en.wikipedia.org/wiki/${encodeURIComponent(wikiData.title)}`;
            setMessages((prev) => [
              ...prev,
              {
                sender: "bot",
                text: `**${wikiData.title}**: ${cleanExtract.substring(0, 300)}... [Source: Wikipedia](${wikiUrl}). Consult a doctor for medical advice.`,
              },
              {
                sender: "bot",
                text: "Would you like to search another term or return to the main menu?",
                type: "options",
                options: ["Search Another Term", "Main Menu", "Exit"],
              },
            ]);
          } else {
            setMessages((prev) => [
              ...prev,
              {
                sender: "bot",
                text: `No information found for "${userText}". Try a term like cellulitis or sepsis.`,
              },
              {
                sender: "bot",
                text: "Try again or return to the main menu.",
                type: "options",
                options: ["Search Another Term", "Main Menu", "Exit"],
              },
            ]);
          }
        } catch (wikiError) {
          console.error("Wikipedia API Error:", wikiError.message);
          setMessages((prev) => [
            ...prev,
            {
              sender: "bot",
              text: `No information found for "${userText}". Try a term like cellulitis or sepsis.`,
            },
            {
              sender: "bot",
              text: "Try again or return to the main menu.",
              type: "options",
              options: ["Search Another Term", "Main Menu", "Exit"],
            },
          ]);
        }
      } finally {
        setIsTyping(false);
      }
      setAwaitingMedicalTerm(false);
      setInput("");
      return;
    }

    // Fallback for unrecognized inputs
    setMessages((prev) => [
      ...prev,
      {
        sender: "bot",
        text: "I can help with SSI guidelines, medical terms, or preoperative preparation. Please select an option or try a medical term.",
        type: "options",
        options: [
          "Guidelines for SSI Detection",
          "Search Medical Terms",
          "Preoperative Checklist",
        ],
      },
    ]);
    setInput("");
  };

  return (
    <div className="chatbot-wrapper">
      {isOpen && (
        <div className="chatbot-container">
          <div className="chat-header">MediBuddy</div>
          <div className="chat-body">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
              >
                {msg.text && <ReactMarkdown>{msg.text}</ReactMarkdown>}
                {msg.type === "options" && (
                  <div className="chat-options">
                    {msg.options.map((option, idx) => (
                      <button
                        key={idx}
                        onClick={() => sendMessage(option)}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {isTyping && (
              <div className="typing-indicator">MediBuddy is typing...</div>
            )}
            <div ref={chatEndRef} />
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder={
                awaitingMedicalTerm
                  ? "Enter a medical term (e.g., abscess, hematoma)"
                  : "Type your message..."
              }
              list={awaitingMedicalTerm ? "medical-terms" : "surgery-list"}
            />
            <datalist id="medical-terms">
              {suggestedTerms.map((term, idx) => (
                <option key={idx} value={term} />
              ))}
            </datalist>
            <datalist id="surgery-list">
              {surgeryTypes.map((type, idx) => (
                <option key={idx} value={type} />
              ))}
            </datalist>
            <button onClick={() => sendMessage()}>
              <FaPaperPlane />
            </button>
          </div>
        </div>
      )}
      <button
        className="chatbot-toggle left"
        onClick={() => setIsOpen(!isOpen)}
      >
        <FaRobot size={24} />
      </button>
    </div>
  );
};

export default Chatbot;