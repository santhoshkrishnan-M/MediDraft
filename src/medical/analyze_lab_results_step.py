config = {
    "name": "AnalyzeLabResults",
    "type": "api",
    "path": "/api/analyze-lab-results",
    "method": "POST",
    "description": "Analyze laboratory test results and detect abnormalities",
    "emits": [],
    "responseSchema": {
        200: {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "analysis": {"type": "object"}
            }
        }
    }
}

async def handler(req, context):
    """Analyze laboratory test results and detect abnormalities"""
    
    try:
        # Motia passes request as dict with 'body' key
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
            context.logger.error(f"Invalid data format: {type(data)}")
            return {
                "status": 400,
                "body": {'success': False, 'error': 'Invalid request format'}
            }
            
        lab_results = data.get('labResults', {})
        
        analysis = {
            'results': [],
            'abnormalities': [],
            'riskIndicators': [],
            'interpretation': ''
        }
        
        hemoglobin = float(lab_results.get('hemoglobin', 0))
        if hemoglobin > 0:
            status = 'Normal'
            flag = ''
            if hemoglobin < 12:
                status = 'Low'
                flag = 'Anemia indicated'
                analysis['abnormalities'].append('Low hemoglobin - possible anemia')
                analysis['riskIndicators'].append('Anemia Risk')
            elif hemoglobin > 17:
                status = 'High'
                flag = 'Polycythemia concern'
                analysis['abnormalities'].append('High hemoglobin - polycythemia concern')
            
            analysis['results'].append({
                'test': 'Hemoglobin',
                'value': hemoglobin,
                'unit': 'g/dL',
                'normalRange': '12-17 g/dL',
                'status': status,
                'flag': flag
            })
        
        blood_sugar = float(lab_results.get('bloodSugar', 0))
        if blood_sugar > 0:
            status = 'Normal'
            flag = ''
            if blood_sugar < 70:
                status = 'Low'
                flag = 'Hypoglycemia'
                analysis['abnormalities'].append('Low blood sugar - hypoglycemia risk')
                analysis['riskIndicators'].append('Hypoglycemia Risk')
            elif blood_sugar > 100 and blood_sugar < 126:
                status = 'Borderline'
                flag = 'Pre-diabetic range'
                analysis['abnormalities'].append('Elevated blood sugar - pre-diabetic range')
                analysis['riskIndicators'].append('Pre-Diabetes Risk')
            elif blood_sugar >= 126:
                status = 'High'
                flag = 'Diabetic range'
                analysis['abnormalities'].append('High blood sugar - diabetic range')
                analysis['riskIndicators'].append('Diabetes Risk')
            
            analysis['results'].append({
                'test': 'Fasting Blood Sugar',
                'value': blood_sugar,
                'unit': 'mg/dL',
                'normalRange': '70-100 mg/dL',
                'status': status,
                'flag': flag
            })
        
        cholesterol = float(lab_results.get('cholesterol', 0))
        if cholesterol > 0:
            status = 'Normal'
            flag = ''
            if cholesterol > 200 and cholesterol < 240:
                status = 'Borderline'
                flag = 'Borderline high'
                analysis['abnormalities'].append('Borderline high cholesterol')
                analysis['riskIndicators'].append('Cardiovascular Risk')
            elif cholesterol >= 240:
                status = 'High'
                flag = 'High cholesterol'
                analysis['abnormalities'].append('High cholesterol - cardiovascular risk')
                analysis['riskIndicators'].append('High Cardiovascular Risk')
            
            analysis['results'].append({
                'test': 'Total Cholesterol',
                'value': cholesterol,
                'unit': 'mg/dL',
                'normalRange': '<200 mg/dL',
                'status': status,
                'flag': flag
            })
        
        bp_systolic = float(lab_results.get('bpSystolic', 0))
        bp_diastolic = float(lab_results.get('bpDiastolic', 0))
        if bp_systolic > 0 and bp_diastolic > 0:
            status = 'Normal'
            flag = ''
            if bp_systolic >= 120 and bp_systolic < 130:
                status = 'Elevated'
                flag = 'Elevated BP'
                analysis['abnormalities'].append('Elevated blood pressure')
                analysis['riskIndicators'].append('Hypertension Risk')
            elif bp_systolic >= 130 or bp_diastolic >= 80:
                status = 'High'
                flag = 'Hypertension'
                analysis['abnormalities'].append('Hypertension detected')
                analysis['riskIndicators'].append('Hypertension')
            
            analysis['results'].append({
                'test': 'Blood Pressure',
                'value': f'{bp_systolic}/{bp_diastolic}',
                'unit': 'mmHg',
                'normalRange': '<120/80 mmHg',
                'status': status,
                'flag': flag
            })
        
        creatinine = float(lab_results.get('creatinine', 0))
        if creatinine > 0:
            status = 'Normal'
            flag = ''
            if creatinine > 1.2:
                status = 'High'
                flag = 'Kidney function concern'
                analysis['abnormalities'].append('Elevated creatinine - kidney function evaluation needed')
                analysis['riskIndicators'].append('Kidney Function Risk')
            
            analysis['results'].append({
                'test': 'Serum Creatinine',
                'value': creatinine,
                'unit': 'mg/dL',
                'normalRange': '0.6-1.2 mg/dL',
                'status': status,
                'flag': flag
            })
        
        if len(analysis['abnormalities']) == 0:
            analysis['interpretation'] = 'All laboratory parameters are within normal limits. No significant abnormalities detected.'
        else:
            analysis['interpretation'] = f'Laboratory analysis reveals {len(analysis["abnormalities"])} abnormal finding(s) requiring clinical attention and possible intervention.'
        
        analysis['riskIndicators'] = list(set(analysis['riskIndicators']))
        
        return {
            "status": 200,
            "body": {
                'success': True,
                'analysis': analysis
            }
        }
        
    except Exception as e:
        context.logger.error(f"Error analyzing lab results: {str(e)}")
        return {
            "status": 200,
            "body": {
                'success': False,
                'error': str(e)
            }
        }
