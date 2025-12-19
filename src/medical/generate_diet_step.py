import os
import json
import google.generativeai as genai

# Motia API configuration
config = {
    "name": "GenerateDietRecommendation",
    "type": "api",
    "path": "/api/generate-diet",
    "method": "POST",
    "description": "Generate personalized diet recommendations using Google Gemini API",
    "emits": [],
    "responseSchema": {
        200: {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "dietRecommendation": {"type": "object"}
            }
        }
    }
}

async def handler(req, context):
    """Motia API handler for diet recommendation generation"""
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
        
        result = generate_diet_recommendation(data)
        return {"status": 200, "body": result}
    except Exception as e:
        context.logger.error(f"Diet recommendation error: {str(e)}")
        return {
            "status": 500,
            "body": {"success": False, "error": str(e)}
        }

def generate_diet_recommendation(data):
    """Generate personalized diet recommendations using Google Gemini API"""
    
    try:
        patient_info = data.get('patientInfo', {})
        risk_indicators = data.get('riskIndicators', [])
        abnormalities = data.get('abnormalities', [])
        
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key or api_key == 'your_google_gemini_api_key_here':
            return {
                'success': False,
                'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in .env file'
            }
        
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = build_diet_prompt(patient_info, risk_indicators, abnormalities)
        
        response = model.generate_content(prompt)
        
        diet_recommendation = parse_gemini_response(response.text)
        
        return {
            'success': True,
            'dietRecommendation': diet_recommendation
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'fallback': generate_fallback_diet(data)
        }

def build_diet_prompt(patient_info, risk_indicators, abnormalities):
    """Build comprehensive prompt for Gemini API"""
    
    age = patient_info.get('age', 'Unknown')
    gender = patient_info.get('gender', 'Unknown')
    
    conditions_text = ''
    if len(risk_indicators) > 0:
        conditions_text = f"\n\nIdentified Health Concerns:\n" + '\n'.join([f"- {risk}" for risk in risk_indicators])
    
    abnormalities_text = ''
    if len(abnormalities) > 0:
        abnormalities_text = f"\n\nLaboratory Abnormalities:\n" + '\n'.join([f"- {abn}" for abn in abnormalities])
    
    prompt = f"""You are a certified clinical nutritionist creating a personalized diet plan for a patient.

Patient Profile:
- Age: {age} years
- Gender: {gender}{conditions_text}{abnormalities_text}

Please provide a comprehensive Indian diet plan with the following structure:

1. DIET OVERVIEW
Provide a brief 2-3 sentence overview of the dietary approach suitable for this patient.

2. RECOMMENDED FOODS (VEGETARIAN)
List 8-10 specific vegetarian Indian foods that are beneficial. Include:
- Whole grains (specify types)
- Vegetables (specify types)
- Lentils and legumes (specify types)
- Dairy products (if appropriate)
- Healthy fats and oils

3. RECOMMENDED FOODS (NON-VEGETARIAN)
List 5-7 non-vegetarian options that are healthy. Include:
- Lean protein sources
- Fish varieties
- Preparation methods

4. FOODS TO AVOID
List 8-10 specific foods or food categories to avoid or limit based on the health concerns.

5. LIFESTYLE & HYDRATION TIPS
Provide 5-7 practical tips including:
- Water intake recommendations
- Meal timing advice
- Portion control
- Exercise suggestions
- Sleep and stress management

Please format your response clearly with these exact section headings. Be specific with Indian food names and practical recommendations."""
    
    return prompt

def parse_gemini_response(response_text):
    """Parse Gemini response into structured format"""
    
    sections = {
        'overview': '',
        'vegetarianFoods': [],
        'nonVegetarianFoods': [],
        'foodsToAvoid': [],
        'lifestyleTips': []
    }
    
    current_section = None
    lines = response_text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        line_upper = line.upper()
        
        if 'DIET OVERVIEW' in line_upper or 'OVERVIEW' in line_upper and current_section is None:
            current_section = 'overview'
            continue
        elif 'RECOMMENDED FOODS (VEGETARIAN)' in line_upper or 'VEGETARIAN' in line_upper and 'RECOMMENDED' in line_upper:
            current_section = 'vegetarian'
            continue
        elif 'RECOMMENDED FOODS (NON-VEGETARIAN)' in line_upper or 'NON-VEGETARIAN' in line_upper and 'RECOMMENDED' in line_upper:
            current_section = 'nonvegetarian'
            continue
        elif 'FOODS TO AVOID' in line_upper or 'AVOID' in line_upper:
            current_section = 'avoid'
            continue
        elif 'LIFESTYLE' in line_upper or 'HYDRATION' in line_upper:
            current_section = 'lifestyle'
            continue
        
        if current_section == 'overview':
            if line and not line.startswith('#') and not line.startswith('*'):
                sections['overview'] += line + ' '
        
        elif current_section == 'vegetarian':
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                item = line.lstrip('-•* ').strip()
                if item and len(item) > 3:
                    sections['vegetarianFoods'].append(item)
        
        elif current_section == 'nonvegetarian':
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                item = line.lstrip('-•* ').strip()
                if item and len(item) > 3:
                    sections['nonVegetarianFoods'].append(item)
        
        elif current_section == 'avoid':
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                item = line.lstrip('-•* ').strip()
                if item and len(item) > 3:
                    sections['foodsToAvoid'].append(item)
        
        elif current_section == 'lifestyle':
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                item = line.lstrip('-•* ').strip()
                if item and len(item) > 3:
                    sections['lifestyleTips'].append(item)
    
    sections['overview'] = sections['overview'].strip()
    
    if not sections['overview']:
        sections['overview'] = 'A balanced diet plan tailored to your health needs, focusing on whole foods, adequate hydration, and mindful eating practices.'
    
    return sections

def generate_fallback_diet(data):
    """Generate fallback diet recommendation if Gemini fails"""
    
    patient_info = data.get('patientInfo', {})
    risk_indicators = data.get('riskIndicators', [])
    
    diet = {
        'overview': 'A balanced Indian diet focusing on whole foods, lean proteins, complex carbohydrates, and healthy fats to support overall health and address identified health concerns.',
        'vegetarianFoods': [
            'Brown rice, whole wheat chapati, and millets (jowar, bajra)',
            'Green leafy vegetables like spinach, methi, and amaranth',
            'Cruciferous vegetables like cauliflower, cabbage, and broccoli',
            'Lentils and legumes (moong dal, masoor dal, chickpeas)',
            'Low-fat dairy products (curd, buttermilk, paneer)',
            'Nuts and seeds (almonds, walnuts, flaxseeds, chia seeds)',
            'Fresh fruits (apple, guava, papaya, berries)',
            'Healthy oils (olive oil, mustard oil in moderation)'
        ],
        'nonVegetarianFoods': [
            'Grilled or baked chicken breast (skinless)',
            'Fish rich in omega-3 (salmon, mackerel, sardines)',
            'Eggs (boiled or scrambled)',
            'Lean meat in moderation',
            'Fish curry with minimal oil'
        ],
        'foodsToAvoid': [
            'Refined flour (maida) products and white bread',
            'Deep-fried foods (samosas, pakoras, puris)',
            'Excessive salt and pickles',
            'Sugary beverages and processed juices',
            'Full-fat dairy products and ghee in excess',
            'Processed and packaged snacks',
            'Red meat and organ meats',
            'Trans fats and margarine'
        ],
        'lifestyleTips': [
            'Drink 8-10 glasses of water throughout the day',
            'Eat small, frequent meals every 3-4 hours',
            'Practice portion control using smaller plates',
            'Include 30 minutes of moderate exercise daily',
            'Ensure 7-8 hours of quality sleep',
            'Manage stress through yoga or meditation',
            'Limit caffeine and avoid late-night eating'
        ]
    }
    
    if 'Diabetes Risk' in risk_indicators:
        diet['foodsToAvoid'].extend([
            'White rice and refined carbohydrates',
            'Sweets and desserts',
            'Honey and jaggery in excess'
        ])
    
    if 'Cardiovascular Risk' in risk_indicators or 'Hypertension' in risk_indicators:
        diet['foodsToAvoid'].extend([
            'High sodium foods',
            'Saturated fats',
            'Coconut oil in excess'
        ])
    
    return diet
