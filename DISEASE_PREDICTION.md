# 🔬 Disease Prediction Engine - Documentation

## Overview

The Disease Prediction Engine is an AI-powered diagnostic assistant that analyzes user-provided patient data, scan findings, and laboratory values to predict possible medical conditions. This system uses rule-based medical logic to identify patterns and correlations that may indicate specific diseases.

## ⚠️ CRITICAL MEDICAL DISCLAIMER

**THIS IS NOT A MEDICAL DIAGNOSIS TOOL**

- All predictions are AI-assisted suggestions for informational purposes only
- Predictions MUST be validated by qualified healthcare professionals
- Do NOT make medical decisions based solely on these predictions
- This tool is designed to assist doctors, not replace them
- Always consult with licensed medical practitioners for diagnosis and treatment

---

## Features

### 1. **Comprehensive Input Collection**
- Patient demographics (age, gender)
- Medical imaging findings (scan type, body part, observations)
- Complete blood work and laboratory values
- Severity assessment

### 2. **Multi-System Disease Detection**
The engine can identify conditions across multiple medical specialties:

#### Neurological
- Encephalitis
- Brain Tumors
- Hemorrhagic Stroke
- Ischemic Stroke

#### Cardiac
- Heart Disease / Cardiomyopathy
- Dyslipidemia

#### Respiratory
- Pneumonia
- Lung Tumors
- Pleural Effusion

#### Metabolic
- Diabetes Mellitus
- Pre-Diabetes
- Hyperlipidemia

#### Hepatic (Liver)
- Fatty Liver Disease
- Liver Cirrhosis

#### Renal (Kidney)
- Kidney Stones
- Renal Cysts
- Chronic Kidney Disease

#### Hematological (Blood)
- Anemia (various severities)
- Blood Disorders
- Leukemia (screening)

#### Inflammatory
- Systemic Inflammatory Conditions

#### Orthopedic
- Bone Fractures
- Arthritis

### 3. **Confidence Scoring**
Each prediction includes a confidence level:
- **High**: Multiple strong indicators present
- **Medium**: Moderate evidence supporting diagnosis
- **Low**: Limited or preliminary evidence

### 4. **Risk Categorization**
Patients are classified into risk categories:
- **Normal**: No significant findings
- **At Risk - Monitor and Consult Doctor**: Some concerns present
- **At Risk - Medical Consultation Recommended**: Multiple abnormalities
- **Critical - Requires Immediate Medical Attention**: Life-threatening conditions detected

### 5. **Explainable AI**
Every prediction includes:
- Supporting evidence from scans
- Lab abnormalities detected
- Specific indicators for each disease
- Personalized recommendations

---

## API Endpoint

### POST `/api/predict-disease`

**Request Body:**
```json
{
  "patientInfo": {
    "age": 55,
    "gender": "male"
  },
  "scanInfo": {
    "scanType": "MRI",
    "bodyPart": "Brain",
    "observedFindings": "lesion detected in frontal lobe",
    "severity": "moderate"
  },
  "labValues": {
    "hemoglobin": 13.5,
    "wbc": 12.5,
    "platelet": 250,
    "fastingBloodSugar": 130,
    "hba1c": 6.8,
    "totalCholesterol": 220,
    "ldl": 150,
    "hdl": 45,
    "triglycerides": 180,
    "crp": 12.0,
    "esr": 35,
    "creatinine": 1.2,
    "urea": 18,
    "alt": 45,
    "ast": 38
  }
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "predicted_diseases": [
      {
        "name": "Possible Encephalitis",
        "confidence": "High",
        "category": "Neurological",
        "indicators": [
          "Brain lesion on imaging",
          "Elevated inflammatory markers"
        ]
      }
    ],
    "confidence_level": "High",
    "supporting_evidence": {
      "scan_findings": [
        "MRI of Brain: lesion detected in frontal lobe (Severity: moderate)"
      ],
      "lab_abnormalities": [
        "High WBC (12.5 x10³/μL, possible infection)",
        "Very High CRP (12.0 mg/L, severe inflammation)"
      ]
    },
    "risk_category": "At Risk - Medical Consultation Recommended",
    "recommended_next_steps": [
      "Consult with a qualified healthcare professional for proper diagnosis",
      "Schedule appointment with neurologist",
      "Repeat laboratory tests to confirm abnormal values"
    ],
    "medical_disclaimer": "⚠️ IMPORTANT: This is an AI-assisted prediction..."
  }
}
```

---

## Input Parameters

### Required Fields
- `patientInfo.age` - Patient's age (number)
- `patientInfo.gender` - Patient's gender (male/female/other)

### Optional Scan Information
- `scanInfo.scanType` - X-ray, MRI, or CT
- `scanInfo.bodyPart` - Body region examined
- `scanInfo.observedFindings` - Free text description of findings
- `scanInfo.severity` - mild, moderate, or severe

### Optional Laboratory Values
All lab values are optional and measured in standard units:

| Parameter | Unit | Normal Range |
|-----------|------|--------------|
| hemoglobin | g/dL | 12-17 |
| wbc | x10³/μL | 4-11 |
| platelet | x10³/μL | 150-400 |
| fastingBloodSugar | mg/dL | 70-100 |
| hba1c | % | <5.7 |
| totalCholesterol | mg/dL | <200 |
| ldl | mg/dL | <100 |
| hdl | mg/dL | >40 |
| triglycerides | mg/dL | <150 |
| crp | mg/L | <3 |
| esr | mm/hr | <20 |
| creatinine | mg/dL | 0.7-1.3 |
| urea/bun | mg/dL | 7-20 |
| alt | U/L | <40 |
| ast | U/L | <40 |

---

## Disease Prediction Rules

### Rule-Based Logic Examples

#### Diabetes Detection
```
IF (fastingBloodSugar >= 126) OR (hba1c >= 6.5)
  THEN Diabetes Mellitus (High Confidence)
```

#### Pneumonia Detection
```
IF (chest_scan contains "opacity" OR "consolidation")
   AND (wbc > 11)
  THEN Possible Pneumonia (High Confidence)
```

#### Brain Tumor Detection
```
IF (brain_mri contains "mass" OR "tumor")
   AND (severity == "severe")
  THEN Possible Brain Tumor (High Confidence)
```

#### Kidney Stone Detection
```
IF (kidney_scan contains "stone" OR "calculus")
   AND (creatinine > 1.3)
  THEN Kidney Stone / Nephrolithiasis (High Confidence)
```

---

## How to Use (Web Interface)

1. **Access the Application**
   - Navigate to http://localhost:3000/medical
   - Click "Disease Prediction" button in the header

2. **Enter Patient Details** (Required)
   - Age
   - Gender

3. **Enter Scan Information** (Optional but recommended)
   - Select scan type (X-ray, MRI, CT)
   - Enter body part examined
   - Describe observed findings
   - Select severity level

4. **Enter Laboratory Values** (Optional but recommended)
   - Fill in any available blood test results
   - Leave blank any unavailable values

5. **Click "🔍 Predict Diseases"**
   - System will analyze all provided data
   - Results displayed with confidence levels

6. **Review Results**
   - Read medical disclaimer carefully
   - Review predicted conditions
   - Check supporting evidence
   - Follow recommended next steps

---

## Technical Architecture

### Backend: Motia Python API
- **File**: `src/medical/disease_prediction_step.py`
- **Type**: Motia API Step
- **Endpoint**: POST `/api/predict-disease`
- **Language**: Python 3.12

### Frontend: Vanilla JavaScript
- **Files**: 
  - `frontend/index.html` (UI components)
  - `frontend/app.js` (Prediction logic)
- **Framework**: Tailwind CSS
- **API Integration**: Fetch API

### Key Functions

#### Backend
- `predict_disease()` - Main orchestration function
- `normalize_lab_values()` - Converts and validates lab inputs
- `identify_lab_abnormalities()` - Detects out-of-range values
- `extract_scan_findings()` - Parses imaging data
- `apply_disease_rules()` - Core prediction logic
- `calculate_confidence_and_risk()` - Risk assessment
- `generate_recommendations()` - Personalized next steps

#### Frontend
- `predictDisease()` - Collects input and calls API
- `displayPredictionResults()` - Renders results with formatting
- `switchToPredictionMode()` - UI mode switching

---

## Extending the System

### Adding New Disease Rules

Edit `src/medical/disease_prediction_step.py` in the `apply_disease_rules()` function:

```python
# Example: Add Pulmonary Embolism detection
if 'lung' in body_part or 'chest' in body_part:
    if 'embolism' in observed or 'clot' in observed:
        diseases.append({
            "name": "Possible Pulmonary Embolism",
            "confidence": "High",
            "category": "Respiratory - CRITICAL",
            "indicators": ["Pulmonary embolism detected on imaging"]
        })
```

### Adding New Lab Parameters

1. Add input field to `frontend/index.html`
2. Collect value in `predictDisease()` function
3. Add reference range in `identify_lab_abnormalities()`
4. Use in disease rules in `apply_disease_rules()`

---

## Testing

### Manual Testing
```bash
curl -X POST http://localhost:3000/api/predict-disease \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 55, "gender": "male"},
    "scanInfo": {
      "scanType": "MRI",
      "bodyPart": "Brain",
      "observedFindings": "lesion",
      "severity": "moderate"
    },
    "labValues": {
      "wbc": 12.5,
      "crp": 12.0
    }
  }'
```

### Test Cases

#### Test Case 1: Diabetes Detection
**Input**: `fastingBloodSugar: 135, hba1c: 6.8`  
**Expected**: Diabetes Mellitus (High Confidence)

#### Test Case 2: Anemia Detection
**Input**: `hemoglobin: 9.5, gender: female`  
**Expected**: Anemia - Moderate to Severe (High Confidence)

#### Test Case 3: Stroke Detection
**Input**: `scanType: CT, bodyPart: Brain, observedFindings: hemorrhage`  
**Expected**: Possible Hemorrhagic Stroke (High Confidence, CRITICAL)

#### Test Case 4: Normal Patient
**Input**: All values within normal ranges  
**Expected**: No significant conditions detected (Normal risk)

---

## Limitations

1. **Rule-Based Logic Only**
   - Does not use machine learning models
   - Limited to programmed rules
   - May miss complex patterns

2. **No Image Processing**
   - Relies on user-entered findings, not actual image analysis
   - Radiologist interpretation still required

3. **Simplified Medical Logic**
   - Real diagnosis requires comprehensive clinical evaluation
   - Many factors not considered (symptoms, history, physical exam)

4. **Reference Range Simplification**
   - Uses general population ranges
   - Does not account for individual variations

5. **No Treatment Recommendations**
   - Only suggests next diagnostic steps
   - Does not prescribe medications or treatments

---

## Future Enhancements

1. **Machine Learning Integration**
   - Train models on medical datasets
   - Pattern recognition for complex conditions

2. **Medical Image Processing**
   - Automatic analysis of uploaded scans
   - Computer vision for abnormality detection

3. **Symptom Integration**
   - Include patient-reported symptoms
   - Combine with physical examination findings

4. **Drug Interaction Checker**
   - Analyze medication lists
   - Flag potential interactions

5. **Longitudinal Analysis**
   - Track changes over time
   - Trend analysis for chronic conditions

6. **Multi-Language Support**
   - Translate interface and results
   - Serve global populations

---

## Support & Contact

For questions, issues, or contributions:
- **GitHub**: https://github.com/santhoshkrishnan-M/MediDraft
- **Documentation**: See README.md and USAGE.md

---

## License & Legal

This is an educational and research tool. Not approved for clinical use without proper validation and regulatory clearance. Users assume all responsibility for how this tool is utilized.

**Last Updated**: December 19, 2025  
**Version**: 1.0.0
