from datetime import datetime

# Motia API configuration
config = {
    "name": "GenerateReport",
    "type": "api",
    "path": "/api/generate-report",
    "method": "POST",
    "description": "Generate comprehensive medical report combining imaging and lab findings",
    "emits": [],
    "responseSchema": {
        200: {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "report": {"type": "object"}
            }
        }
    }
}

async def handler(req, context):
    """Motia API handler for report generation"""
    try:
        # Motia passes request as dict with 'body' key containing actual data
        if isinstance(req, dict) and 'body' in req:
            body_content = req['body']
            # If body is a JSON string, parse it
            if isinstance(body_content, str):
                import json
                data = json.loads(body_content)
            else:
                data = body_content
        elif hasattr(req, 'body'):
            data = req.body
        elif isinstance(req, dict):
            data = req
        else:
            data = req
        
        if not isinstance(data, dict):
            return {
                "status": 400,
                "body": {'success': False, 'error': 'Invalid request format'}
            }
        
        result = generate_report(data)
        return {"status": 200, "body": result}
    except Exception as e:
        context.logger.error(f"Report generation error: {str(e)}")
        return {
            "status": 500,
            "body": {"success": False, "error": str(e)}
        }

def generate_report(data):
    """Generate comprehensive medical report combining all findings"""
    
    try:
        patient_info = data.get('patientInfo', {})
        imaging_findings = data.get('imagingFindings', {})
        lab_analysis = data.get('labAnalysis', {})
        
        report = {
            'reportId': generate_report_id(),
            'generatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'patientSummary': generate_patient_summary(patient_info),
            'imagingFindings': format_imaging_findings(imaging_findings),
            'labResults': format_lab_results(lab_analysis),
            'clinicalImpression': generate_clinical_impression(imaging_findings, lab_analysis),
            'riskIndicators': lab_analysis.get('riskIndicators', []),
            'recommendedNextSteps': generate_next_steps(imaging_findings, lab_analysis)
        }
        
        return {
            'success': True,
            'report': report
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def generate_report_id():
    """Generate unique report ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f'MR-{timestamp}'

def generate_patient_summary(patient_info):
    """Generate patient summary section"""
    return {
        'patientId': patient_info.get('patientId', 'N/A'),
        'patientName': patient_info.get('patientName', 'N/A'),
        'age': patient_info.get('age', 'N/A'),
        'gender': patient_info.get('gender', 'N/A'),
        'studyDate': patient_info.get('studyDate', 'N/A'),
        'imageType': patient_info.get('imageType', 'N/A')
    }

def format_imaging_findings(findings):
    """Format imaging findings section"""
    if not findings:
        return {
            'modality': 'Not Available',
            'quality': 'N/A',
            'findings': [],
            'impression': 'No imaging data available'
        }
    
    return {
        'modality': findings.get('modality', 'Unknown'),
        'quality': findings.get('quality', 'N/A'),
        'findings': findings.get('findings', []),
        'impression': findings.get('impression', 'No impression available')
    }

def format_lab_results(lab_analysis):
    """Format lab results section"""
    if not lab_analysis:
        return {
            'results': [],
            'abnormalities': [],
            'interpretation': 'No laboratory data available'
        }
    
    return {
        'results': lab_analysis.get('results', []),
        'abnormalities': lab_analysis.get('abnormalities', []),
        'interpretation': lab_analysis.get('interpretation', 'No interpretation available')
    }

def generate_clinical_impression(imaging_findings, lab_analysis):
    """Generate overall clinical impression"""
    
    impressions = []
    
    if imaging_findings and imaging_findings.get('impression'):
        impressions.append(f"Imaging: {imaging_findings['impression']}")
    
    if lab_analysis and lab_analysis.get('interpretation'):
        impressions.append(f"Laboratory: {lab_analysis['interpretation']}")
    
    abnormalities = lab_analysis.get('abnormalities', []) if lab_analysis else []
    
    if len(abnormalities) == 0:
        overall = "Overall clinical assessment indicates no significant acute pathology. Findings are within normal parameters for age and gender."
    elif len(abnormalities) <= 2:
        overall = "Overall clinical assessment reveals minor abnormalities that warrant monitoring and lifestyle modifications. Follow-up recommended."
    else:
        overall = "Overall clinical assessment indicates multiple abnormalities requiring medical attention. Comprehensive treatment plan and regular monitoring strongly recommended."
    
    impressions.append(overall)
    
    return ' '.join(impressions)

def generate_next_steps(imaging_findings, lab_analysis):
    """Generate recommended next steps"""
    
    steps = []
    
    abnormalities = lab_analysis.get('abnormalities', []) if lab_analysis else []
    risk_indicators = lab_analysis.get('riskIndicators', []) if lab_analysis else []
    
    if len(abnormalities) == 0:
        steps.append('Continue routine health monitoring and annual check-ups')
        steps.append('Maintain healthy lifestyle and balanced diet')
        steps.append('Regular physical activity recommended')
    else:
        steps.append('Consult with primary care physician for detailed evaluation')
        steps.append('Follow prescribed treatment plan and medications')
        steps.append('Repeat laboratory tests in 3-6 months to monitor trends')
        
        if 'Diabetes Risk' in risk_indicators or 'Pre-Diabetes Risk' in risk_indicators:
            steps.append('Dietary modification for blood sugar control')
            steps.append('Regular glucose monitoring')
        
        if 'Cardiovascular Risk' in risk_indicators or 'Hypertension' in risk_indicators:
            steps.append('Cardiovascular risk assessment')
            steps.append('Blood pressure monitoring')
            steps.append('Lipid profile management')
        
        if 'Anemia Risk' in risk_indicators:
            steps.append('Iron supplementation as advised')
            steps.append('Dietary iron intake optimization')
        
        if 'Kidney Function Risk' in risk_indicators:
            steps.append('Nephrology consultation recommended')
            steps.append('Kidney function monitoring')
    
    steps.append('Follow personalized diet recommendations provided')
    steps.append('Schedule follow-up appointment within 2-4 weeks')
    
    return steps
