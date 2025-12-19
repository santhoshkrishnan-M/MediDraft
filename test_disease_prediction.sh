#!/bin/bash

# Disease Prediction Engine - Test Suite
# Tests various medical scenarios to validate the prediction engine

echo "🧪 Starting Disease Prediction Engine Test Suite"
echo "================================================"
echo ""

BASE_URL="http://localhost:3000/api/predict-disease"

# Test 1: Diabetes Detection
echo "Test 1: Diabetes Detection"
echo "--------------------------"
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 58, "gender": "male"},
    "scanInfo": {},
    "labValues": {
      "fastingBloodSugar": 145,
      "hba1c": 7.2
    }
  }' | python3 -c "import sys, json; data=json.load(sys.stdin); print('✅ PASS' if any('Diabetes' in d['name'] for d in data['prediction']['predicted_diseases']) else '❌ FAIL'); print('Diseases:', [d['name'] for d in data['prediction']['predicted_diseases']])"
echo ""

# Test 2: Brain Tumor Detection
echo "Test 2: Brain Tumor Detection"
echo "------------------------------"
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 45, "gender": "female"},
    "scanInfo": {
      "scanType": "MRI",
      "bodyPart": "Brain",
      "observedFindings": "mass detected",
      "severity": "severe"
    },
    "labValues": {}
  }' | python3 -c "import sys, json; data=json.load(sys.stdin); print('✅ PASS' if any('Tumor' in d['name'] for d in data['prediction']['predicted_diseases']) else '❌ FAIL'); print('Diseases:', [d['name'] for d in data['prediction']['predicted_diseases']])"
echo ""

# Test 3: Pneumonia Detection
echo "Test 3: Pneumonia Detection"
echo "---------------------------"
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 35, "gender": "male"},
    "scanInfo": {
      "scanType": "X-ray",
      "bodyPart": "Chest",
      "observedFindings": "opacity in right lung",
      "severity": "moderate"
    },
    "labValues": {
      "wbc": 15.0
    }
  }' | python3 -c "import sys, json; data=json.load(sys.stdin); print('✅ PASS' if any('Pneumonia' in d['name'] for d in data['prediction']['predicted_diseases']) else '❌ FAIL'); print('Diseases:', [d['name'] for d in data['prediction']['predicted_diseases']])"
echo ""

# Test 4: Anemia Detection
echo "Test 4: Anemia Detection"
echo "------------------------"
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 28, "gender": "female"},
    "scanInfo": {},
    "labValues": {
      "hemoglobin": 9.0
    }
  }' | python3 -c "import sys, json; data=json.load(sys.stdin); print('✅ PASS' if any('Anemia' in d['name'] for d in data['prediction']['predicted_diseases']) else '❌ FAIL'); print('Diseases:', [d['name'] for d in data['prediction']['predicted_diseases']])"
echo ""

# Test 5: Kidney Stone Detection
echo "Test 5: Kidney Stone Detection"
echo "-------------------------------"
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 42, "gender": "male"},
    "scanInfo": {
      "scanType": "CT",
      "bodyPart": "Kidney",
      "observedFindings": "stone in left kidney",
      "severity": "moderate"
    },
    "labValues": {
      "creatinine": 1.5
    }
  }' | python3 -c "import sys, json; data=json.load(sys.stdin); print('✅ PASS' if any('Kidney Stone' in d['name'] or 'Stone' in d['name'] for d in data['prediction']['predicted_diseases']) else '❌ FAIL'); print('Diseases:', [d['name'] for d in data['prediction']['predicted_diseases']])"
echo ""

# Test 6: Fatty Liver Detection
echo "Test 6: Fatty Liver Detection"
echo "------------------------------"
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 50, "gender": "male"},
    "scanInfo": {
      "scanType": "CT",
      "bodyPart": "Liver",
      "observedFindings": "fatty liver",
      "severity": "moderate"
    },
    "labValues": {
      "alt": 55,
      "ast": 48
    }
  }' | python3 -c "import sys, json; data=json.load(sys.stdin); print('✅ PASS' if any('Fatty Liver' in d['name'] for d in data['prediction']['predicted_diseases']) else '❌ FAIL'); print('Diseases:', [d['name'] for d in data['prediction']['predicted_diseases']])"
echo ""

# Test 7: Normal Patient (No Conditions)
echo "Test 7: Normal Patient"
echo "----------------------"
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 30, "gender": "female"},
    "scanInfo": {},
    "labValues": {
      "hemoglobin": 13.5,
      "wbc": 7.5,
      "fastingBloodSugar": 90,
      "cholesterol": 180
    }
  }' | python3 -c "import sys, json; data=json.load(sys.stdin); result='Normal' in data['prediction']['risk_category']; print('✅ PASS' if result else '❌ FAIL'); print('Risk:', data['prediction']['risk_category'])"
echo ""

# Test 8: Critical Case - Stroke
echo "Test 8: Critical Case - Stroke"
echo "-------------------------------"
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 65, "gender": "male"},
    "scanInfo": {
      "scanType": "CT",
      "bodyPart": "Brain",
      "observedFindings": "hemorrhage",
      "severity": "severe"
    },
    "labValues": {}
  }' | python3 -c "import sys, json; data=json.load(sys.stdin); result='Critical' in data['prediction']['risk_category']; print('✅ PASS' if result else '❌ FAIL'); print('Risk:', data['prediction']['risk_category']); print('Diseases:', [d['name'] for d in data['prediction']['predicted_diseases']])"
echo ""

echo "================================================"
echo "🎉 Test Suite Complete!"
echo ""
echo "Note: Each test validates specific disease detection rules."
echo "All predictions include medical disclaimers."
