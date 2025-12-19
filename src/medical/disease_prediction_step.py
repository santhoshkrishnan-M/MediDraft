import json
from typing import Dict, List, Any, Tuple

# Motia API configuration
config = {
    "name": "DiseasePrediction",
    "type": "api",
    "path": "/api/predict-disease",
    "method": "POST",
    "description": "AI-powered disease prediction based on user-provided scan findings and lab values",
    "emits": [],
    "responseSchema": {
        200: {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "prediction": {"type": "object"}
            }
        }
    }
}

async def handler(req, context):
    """Motia API handler for disease prediction"""
    try:
        # Parse request body
        if isinstance(req, dict) and 'body' in req:
            body_content = req['body']
            if isinstance(body_content, str):
                data = json.loads(body_content)
            else:
                data = body_content
        elif hasattr(req, 'body'):
            data = req.body
        else:
            data = req
        
        if not isinstance(data, dict):
            return {
                "status": 400,
                "body": {'success': False, 'error': 'Invalid request format'}
            }
        
        # Perform disease prediction
        result = predict_disease(data, context)
        
        return {"status": 200, "body": result}
        
    except Exception as e:
        context.logger.error(f"Disease prediction error: {str(e)}")
        return {
            "status": 500,
            "body": {"success": False, "error": str(e)}
        }


def predict_disease(data: Dict[str, Any], context) -> Dict[str, Any]:
    """Main disease prediction function"""
    
    try:
        # Extract user input
        patient_info = data.get('patientInfo', {})
        scan_info = data.get('scanInfo', {})
        lab_values = data.get('labValues', {})
        
        context.logger.info(f"Predicting diseases for patient age: {patient_info.get('age')}")
        
        # Initialize prediction results
        predicted_diseases = []
        supporting_evidence = {
            "scan_findings": [],
            "lab_abnormalities": []
        }
        
        # Normalize and validate lab values
        normalized_labs = normalize_lab_values(lab_values)
        
        # Identify lab abnormalities
        lab_abnormalities = identify_lab_abnormalities(normalized_labs, patient_info)
        supporting_evidence["lab_abnormalities"] = lab_abnormalities
        
        # Extract scan findings
        scan_findings = extract_scan_findings(scan_info)
        supporting_evidence["scan_findings"] = scan_findings
        
        # Apply disease prediction rules
        predicted_diseases = apply_disease_rules(
            patient_info,
            scan_findings,
            lab_abnormalities,
            normalized_labs,
            scan_info
        )
        
        # Calculate overall confidence and risk
        confidence_level, risk_category = calculate_confidence_and_risk(
            predicted_diseases,
            lab_abnormalities,
            scan_findings
        )
        
        # Generate recommendations
        recommendations = generate_recommendations(
            predicted_diseases,
            risk_category,
            lab_abnormalities
        )
        
        # Build response
        return {
            "success": True,
            "prediction": {
                "predicted_diseases": predicted_diseases,
                "confidence_level": confidence_level,
                "supporting_evidence": supporting_evidence,
                "risk_category": risk_category,
                "recommended_next_steps": recommendations,
                "medical_disclaimer": "⚠️ IMPORTANT: This is an AI-assisted prediction for informational purposes only. It is NOT a medical diagnosis. All predictions must be validated by a qualified healthcare professional. Do not make medical decisions based solely on this prediction."
            }
        }
        
    except Exception as e:
        context.logger.error(f"Error in disease prediction: {str(e)}")
        return {
            "success": False,
            "error": f"Prediction failed: {str(e)}"
        }


def normalize_lab_values(lab_values: Dict[str, Any]) -> Dict[str, float]:
    """Normalize and convert lab values to float"""
    normalized = {}
    
    for key, value in lab_values.items():
        if value is None or value == '':
            continue
        try:
            normalized[key] = float(value)
        except (ValueError, TypeError):
            continue
    
    return normalized


def identify_lab_abnormalities(labs: Dict[str, float], patient_info: Dict[str, Any]) -> List[str]:
    """Identify abnormal lab values based on reference ranges"""
    abnormalities = []
    gender = patient_info.get('gender', '').lower()
    age = int(patient_info.get('age', 0)) if patient_info.get('age') else 0
    
    # Hemoglobin
    if 'hemoglobin' in labs or 'hb' in labs:
        hb = labs.get('hemoglobin', labs.get('hb', 0))
        if hb > 0:
            if gender == 'male':
                if hb < 13.0:
                    abnormalities.append(f"Low Hemoglobin ({hb} g/dL, normal: 13-17)")
                elif hb > 17.0:
                    abnormalities.append(f"High Hemoglobin ({hb} g/dL)")
            elif gender == 'female':
                if hb < 12.0:
                    abnormalities.append(f"Low Hemoglobin ({hb} g/dL, normal: 12-16)")
                elif hb > 16.0:
                    abnormalities.append(f"High Hemoglobin ({hb} g/dL)")
    
    # White Blood Cell Count
    if 'wbc' in labs:
        wbc = labs['wbc']
        if wbc < 4.0:
            abnormalities.append(f"Low WBC ({wbc} x10³/μL, normal: 4-11)")
        elif wbc > 11.0:
            abnormalities.append(f"High WBC ({wbc} x10³/μL, possible infection)")
        elif wbc > 20.0:
            abnormalities.append(f"Very High WBC ({wbc} x10³/μL, CRITICAL)")
    
    # Platelet Count
    if 'platelet' in labs:
        plt = labs['platelet']
        if plt < 150:
            abnormalities.append(f"Low Platelet Count ({plt} x10³/μL, normal: 150-400)")
        elif plt > 400:
            abnormalities.append(f"High Platelet Count ({plt} x10³/μL)")
    
    # Fasting Blood Sugar
    if 'fastingBloodSugar' in labs or 'bloodSugar' in labs:
        fbs = labs.get('fastingBloodSugar', labs.get('bloodSugar', 0))
        if fbs >= 126:
            abnormalities.append(f"High Fasting Blood Sugar ({fbs} mg/dL, diabetes range)")
        elif fbs >= 100:
            abnormalities.append(f"Elevated Fasting Blood Sugar ({fbs} mg/dL, pre-diabetes)")
    
    # HbA1c
    if 'hba1c' in labs:
        hba1c = labs['hba1c']
        if hba1c >= 6.5:
            abnormalities.append(f"High HbA1c ({hba1c}%, diabetes range)")
        elif hba1c >= 5.7:
            abnormalities.append(f"Elevated HbA1c ({hba1c}%, pre-diabetes)")
    
    # Total Cholesterol
    if 'totalCholesterol' in labs or 'cholesterol' in labs:
        chol = labs.get('totalCholesterol', labs.get('cholesterol', 0))
        if chol >= 240:
            abnormalities.append(f"High Total Cholesterol ({chol} mg/dL, normal: <200)")
        elif chol >= 200:
            abnormalities.append(f"Borderline High Cholesterol ({chol} mg/dL)")
    
    # LDL Cholesterol
    if 'ldl' in labs:
        ldl = labs['ldl']
        if ldl >= 160:
            abnormalities.append(f"High LDL ({ldl} mg/dL, normal: <100)")
        elif ldl >= 130:
            abnormalities.append(f"Borderline High LDL ({ldl} mg/dL)")
    
    # HDL Cholesterol
    if 'hdl' in labs:
        hdl = labs['hdl']
        if hdl < 40:
            abnormalities.append(f"Low HDL ({hdl} mg/dL, normal: >40)")
    
    # Triglycerides
    if 'triglycerides' in labs:
        trig = labs['triglycerides']
        if trig >= 200:
            abnormalities.append(f"High Triglycerides ({trig} mg/dL, normal: <150)")
        elif trig >= 150:
            abnormalities.append(f"Borderline High Triglycerides ({trig} mg/dL)")
    
    # CRP (C-Reactive Protein)
    if 'crp' in labs:
        crp = labs['crp']
        if crp > 10:
            abnormalities.append(f"Very High CRP ({crp} mg/L, severe inflammation)")
        elif crp > 3:
            abnormalities.append(f"Elevated CRP ({crp} mg/L, inflammation present)")
    
    # ESR (Erythrocyte Sedimentation Rate)
    if 'esr' in labs:
        esr = labs['esr']
        if esr > 30:
            abnormalities.append(f"Elevated ESR ({esr} mm/hr, inflammation/infection)")
    
    # Creatinine
    if 'creatinine' in labs:
        creat = labs['creatinine']
        if creat > 1.3:
            abnormalities.append(f"High Creatinine ({creat} mg/dL, possible kidney dysfunction)")
    
    # Urea/BUN
    if 'urea' in labs or 'bun' in labs:
        urea = labs.get('urea', labs.get('bun', 0))
        if urea > 20:
            abnormalities.append(f"Elevated Urea/BUN ({urea} mg/dL, kidney function concern)")
    
    # ALT (Liver enzyme)
    if 'alt' in labs:
        alt = labs['alt']
        if alt > 40:
            abnormalities.append(f"Elevated ALT ({alt} U/L, possible liver issue)")
    
    # AST (Liver enzyme)
    if 'ast' in labs:
        ast = labs['ast']
        if ast > 40:
            abnormalities.append(f"Elevated AST ({ast} U/L, possible liver issue)")
    
    return abnormalities


def extract_scan_findings(scan_info: Dict[str, Any]) -> List[str]:
    """Extract and format scan findings from user input"""
    findings = []
    
    scan_type = scan_info.get('scanType', '')
    body_part = scan_info.get('bodyPart', '')
    observed = scan_info.get('observedFindings', '')
    severity = scan_info.get('severity', '')
    
    if scan_type and body_part:
        finding_text = f"{scan_type} of {body_part}"
        if observed:
            finding_text += f": {observed}"
        if severity:
            finding_text += f" (Severity: {severity})"
        findings.append(finding_text)
    
    return findings


def apply_disease_rules(
    patient_info: Dict[str, Any],
    scan_findings: List[str],
    lab_abnormalities: List[str],
    labs: Dict[str, float],
    scan_info: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Apply rule-based disease prediction logic"""
    
    diseases = []
    
    # Extract key information
    observed = scan_info.get('observedFindings', '').lower()
    severity = scan_info.get('severity', '').lower()
    scan_type = scan_info.get('scanType', '').lower()
    body_part = scan_info.get('bodyPart', '').lower()
    
    # NEUROLOGICAL DISEASES
    if 'brain' in body_part:
        if 'lesion' in observed and any('crp' in abn.lower() or 'esr' in abn.lower() for abn in lab_abnormalities):
            diseases.append({
                "name": "Possible Encephalitis",
                "confidence": "High" if severity == "severe" else "Medium",
                "category": "Neurological",
                "indicators": ["Brain lesion on imaging", "Elevated inflammatory markers"]
            })
        
        if 'mass' in observed or 'tumor' in observed:
            diseases.append({
                "name": "Possible Brain Tumor",
                "confidence": "High" if severity == "severe" else "Medium",
                "category": "Neurological",
                "indicators": ["Mass/tumor detected on imaging"]
            })
        
        if 'bleed' in observed or 'hemorrhage' in observed:
            diseases.append({
                "name": "Possible Hemorrhagic Stroke",
                "confidence": "High",
                "category": "Neurological - CRITICAL",
                "indicators": ["Brain hemorrhage detected"]
            })
        
        if 'infarct' in observed or 'ischemic' in observed:
            diseases.append({
                "name": "Possible Ischemic Stroke",
                "confidence": "High",
                "category": "Neurological - CRITICAL",
                "indicators": ["Ischemic changes detected"]
            })
    
    # CARDIAC DISEASES
    if 'heart' in body_part or 'cardiac' in body_part or ('chest' in body_part and 'x-ray' in scan_type):
        if 'enlarged' in observed or 'cardiomegaly' in observed:
            chol_high = any('cholesterol' in abn.lower() for abn in lab_abnormalities)
            diseases.append({
                "name": "Possible Heart Disease / Cardiomyopathy",
                "confidence": "High" if chol_high else "Medium",
                "category": "Cardiac",
                "indicators": ["Enlarged heart on imaging"] + (["High cholesterol"] if chol_high else [])
            })
    
    # Check for dyslipidemia from labs alone
    if labs.get('ldl', 0) >= 160 or labs.get('triglycerides', 0) >= 200:
        diseases.append({
            "name": "Dyslipidemia",
            "confidence": "High",
            "category": "Metabolic",
            "indicators": ["Significantly elevated lipid levels"]
        })
    
    # RESPIRATORY DISEASES
    if 'lung' in body_part or 'chest' in body_part:
        if 'opacity' in observed or 'consolidation' in observed or 'infiltrate' in observed:
            wbc_high = any('wbc' in abn.lower() and 'high' in abn.lower() for abn in lab_abnormalities)
            diseases.append({
                "name": "Possible Pneumonia",
                "confidence": "High" if wbc_high else "Medium",
                "category": "Respiratory",
                "indicators": ["Lung opacity/consolidation"] + (["Elevated WBC"] if wbc_high else [])
            })
        
        if 'nodule' in observed or 'mass' in observed:
            diseases.append({
                "name": "Possible Lung Tumor / Malignancy",
                "confidence": "Medium",
                "category": "Respiratory",
                "indicators": ["Lung nodule/mass detected - requires biopsy"]
            })
        
        if 'effusion' in observed:
            diseases.append({
                "name": "Pleural Effusion",
                "confidence": "High",
                "category": "Respiratory",
                "indicators": ["Fluid in pleural space"]
            })
    
    # METABOLIC DISEASES - DIABETES
    fbs = labs.get('fastingBloodSugar', labs.get('bloodSugar', 0))
    hba1c = labs.get('hba1c', 0)
    
    if fbs >= 126 or hba1c >= 6.5:
        diseases.append({
            "name": "Diabetes Mellitus",
            "confidence": "High",
            "category": "Metabolic",
            "indicators": [
                f"Fasting Blood Sugar: {fbs} mg/dL" if fbs >= 126 else "",
                f"HbA1c: {hba1c}%" if hba1c >= 6.5 else ""
            ]
        })
    elif fbs >= 100 or hba1c >= 5.7:
        diseases.append({
            "name": "Pre-Diabetes",
            "confidence": "High",
            "category": "Metabolic",
            "indicators": ["Elevated blood sugar in pre-diabetic range"]
        })
    
    # LIVER DISEASES
    if 'liver' in body_part or 'hepatic' in body_part:
        if 'fatty' in observed or 'steatosis' in observed:
            alt_high = labs.get('alt', 0) > 40
            ast_high = labs.get('ast', 0) > 40
            diseases.append({
                "name": "Fatty Liver Disease",
                "confidence": "High" if (alt_high or ast_high) else "Medium",
                "category": "Hepatic",
                "indicators": ["Fatty liver on imaging"] + (["Elevated liver enzymes"] if (alt_high or ast_high) else [])
            })
        
        if 'cirrhosis' in observed:
            diseases.append({
                "name": "Liver Cirrhosis",
                "confidence": "High",
                "category": "Hepatic",
                "indicators": ["Cirrhotic changes on imaging"]
            })
    
    # KIDNEY DISEASES
    if 'kidney' in body_part or 'renal' in body_part:
        if 'stone' in observed or 'calculus' in observed:
            creat_high = labs.get('creatinine', 0) > 1.3
            diseases.append({
                "name": "Kidney Stone / Nephrolithiasis",
                "confidence": "High",
                "category": "Renal",
                "indicators": ["Kidney stone detected"] + (["Elevated creatinine"] if creat_high else [])
            })
        
        if 'cyst' in observed:
            diseases.append({
                "name": "Renal Cyst",
                "confidence": "High",
                "category": "Renal",
                "indicators": ["Kidney cyst detected"]
            })
    
    # Kidney dysfunction from labs
    if labs.get('creatinine', 0) > 1.5 or labs.get('urea', 0) > 25:
        diseases.append({
            "name": "Renal Dysfunction / Chronic Kidney Disease",
            "confidence": "Medium",
            "category": "Renal",
            "indicators": ["Elevated kidney function markers"]
        })
    
    # HEMATOLOGICAL DISEASES
    hb = labs.get('hemoglobin', labs.get('hb', 0))
    if hb > 0 and hb < 10:
        diseases.append({
            "name": "Anemia (Moderate to Severe)",
            "confidence": "High",
            "category": "Hematological",
            "indicators": [f"Low Hemoglobin: {hb} g/dL"]
        })
    elif hb < 12:
        diseases.append({
            "name": "Mild Anemia",
            "confidence": "Medium",
            "category": "Hematological",
            "indicators": [f"Low Hemoglobin: {hb} g/dL"]
        })
    
    # Blood disorder - extremely high WBC
    if labs.get('wbc', 0) > 20:
        diseases.append({
            "name": "Possible Blood Disorder / Leukemia (CRITICAL)",
            "confidence": "Medium",
            "category": "Hematological - REQUIRES URGENT EVALUATION",
            "indicators": [f"Very High WBC: {labs['wbc']} x10³/μL"]
        })
    
    # INFLAMMATORY CONDITIONS
    if labs.get('crp', 0) > 10 or labs.get('esr', 0) > 50:
        if not any(d['category'] == 'Neurological' for d in diseases):
            diseases.append({
                "name": "Systemic Inflammatory Condition",
                "confidence": "Medium",
                "category": "Inflammatory",
                "indicators": ["Significantly elevated inflammatory markers"]
            })
    
    # BONE/JOINT DISEASES
    if 'bone' in body_part or 'joint' in body_part or 'spine' in body_part:
        if 'fracture' in observed:
            diseases.append({
                "name": "Bone Fracture",
                "confidence": "High",
                "category": "Orthopedic",
                "indicators": ["Fracture detected on imaging"]
            })
        
        if 'arthritis' in observed or 'degeneration' in observed:
            diseases.append({
                "name": "Arthritis / Degenerative Joint Disease",
                "confidence": "High",
                "category": "Orthopedic",
                "indicators": ["Arthritic changes on imaging"]
            })
    
    return diseases


def calculate_confidence_and_risk(
    diseases: List[Dict[str, Any]],
    lab_abnormalities: List[str],
    scan_findings: List[str]
) -> Tuple[str, str]:
    """Calculate overall confidence level and risk category"""
    
    if not diseases:
        return "N/A", "Normal"
    
    # Count critical indicators
    critical_count = sum(1 for d in diseases if 'CRITICAL' in d.get('category', ''))
    high_conf_count = sum(1 for d in diseases if d.get('confidence') == 'High')
    
    # Determine confidence
    if high_conf_count >= 2:
        confidence = "High"
    elif high_conf_count == 1 or len(diseases) >= 2:
        confidence = "Medium"
    else:
        confidence = "Low"
    
    # Determine risk
    if critical_count > 0:
        risk = "Critical - Requires Immediate Medical Attention"
    elif high_conf_count >= 2 or len(lab_abnormalities) >= 5:
        risk = "At Risk - Medical Consultation Recommended"
    elif len(diseases) > 0:
        risk = "At Risk - Monitor and Consult Doctor"
    else:
        risk = "Normal"
    
    return confidence, risk


def generate_recommendations(
    diseases: List[Dict[str, Any]],
    risk_category: str,
    lab_abnormalities: List[str]
) -> List[str]:
    """Generate personalized next steps based on predictions"""
    
    recommendations = []
    
    if 'Critical' in risk_category:
        recommendations.append("🚨 URGENT: Seek immediate medical attention")
        recommendations.append("Visit emergency department or call emergency services")
    
    if diseases:
        recommendations.append("Consult with a qualified healthcare professional for proper diagnosis")
        recommendations.append("Share this prediction report with your doctor")
        
        # Category-specific recommendations
        categories = set(d['category'].split(' - ')[0] for d in diseases)
        
        if 'Neurological' in categories:
            recommendations.append("Schedule appointment with neurologist")
        
        if 'Cardiac' in categories:
            recommendations.append("Consult cardiologist for cardiac evaluation")
        
        if 'Respiratory' in categories:
            recommendations.append("Pulmonologist consultation recommended")
        
        if 'Metabolic' in categories:
            recommendations.append("Endocrinologist consultation for metabolic management")
            recommendations.append("Lifestyle modifications: diet and exercise")
        
        if 'Hepatic' in categories:
            recommendations.append("Hepatologist or gastroenterologist consultation")
        
        if 'Renal' in categories:
            recommendations.append("Nephrologist consultation recommended")
        
        if 'Hematological' in categories:
            recommendations.append("Hematologist consultation for blood disorder evaluation")
    
    if len(lab_abnormalities) >= 3:
        recommendations.append("Repeat laboratory tests to confirm abnormal values")
    
    if not diseases:
        recommendations.append("Continue routine health check-ups")
        recommendations.append("Maintain healthy lifestyle")
    
    recommendations.append("Follow medical advice and prescribed treatment plans")
    recommendations.append("⚠️ Remember: This is an AI prediction, not a diagnosis")
    
    return recommendations
