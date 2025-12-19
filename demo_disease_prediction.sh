#!/bin/bash

# Comprehensive Demo - Disease Prediction Engine
# This script demonstrates various medical scenarios

echo "╔════════════════════════════════════════════════════════╗"
echo "║   Disease Prediction Engine - Live Demo               ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

API_URL="http://localhost:3000/api/predict-disease"

# Function to display formatted results
display_result() {
    echo "$1" | python3 -m json.tool 2>/dev/null | grep -E "(\"name\"|\"confidence\"|\"risk_category\"|\"medical_disclaimer\")" | head -20
}

# Demo 1: Critical Emergency Case
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚨 DEMO 1: CRITICAL EMERGENCY - Hemorrhagic Stroke"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Patient: 68-year-old male"
echo "Scan: CT Brain - Hemorrhage detected"
echo "Severity: Severe"
echo ""
echo "Analysis:"

RESULT=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 68, "gender": "male"},
    "scanInfo": {
      "scanType": "CT",
      "bodyPart": "Brain",
      "observedFindings": "hemorrhage",
      "severity": "severe"
    },
    "labValues": {}
  }')

echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
pred = data['prediction']
print(f\"🎯 Predicted Disease: {pred['predicted_diseases'][0]['name']}\")
print(f\"⚠️  Risk Level: {pred['risk_category']}\")
print(f\"📊 Confidence: {pred['confidence_level']}\")
print(f\"\\n💡 First Recommendation: {pred['recommended_next_steps'][0]}\")
"
echo ""
sleep 2

# Demo 2: Chronic Condition
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 DEMO 2: CHRONIC CONDITION - Type 2 Diabetes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Patient: 52-year-old female"
echo "Labs: Fasting Blood Sugar 142 mg/dL, HbA1c 7.3%"
echo ""
echo "Analysis:"

RESULT=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 52, "gender": "female"},
    "scanInfo": {},
    "labValues": {
      "fastingBloodSugar": 142,
      "hba1c": 7.3
    }
  }')

echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
pred = data['prediction']
for disease in pred['predicted_diseases']:
    if 'Diabetes' in disease['name']:
        print(f\"🎯 Predicted Disease: {disease['name']}\")
        print(f\"📊 Confidence: {disease['confidence']}\")
        print(f\"🔬 Indicators: {', '.join(disease['indicators'])}\")
print(f\"\\n⚠️  Risk Level: {pred['risk_category']}\")
print(f\"\\n📋 Lab Abnormalities Detected:\")
for abn in pred['supporting_evidence']['lab_abnormalities'][:3]:
    print(f\"   - {abn}\")
"
echo ""
sleep 2

# Demo 3: Respiratory Infection
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🫁 DEMO 3: RESPIRATORY INFECTION - Pneumonia"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Patient: 38-year-old male"
echo "Scan: Chest X-ray - Right lower lobe opacity"
echo "Labs: WBC 16.2, CRP 25.5"
echo ""
echo "Analysis:"

RESULT=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 38, "gender": "male"},
    "scanInfo": {
      "scanType": "X-ray",
      "bodyPart": "Chest",
      "observedFindings": "right lower lobe opacity",
      "severity": "moderate"
    },
    "labValues": {
      "wbc": 16.2,
      "crp": 25.5,
      "esr": 45
    }
  }')

echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
pred = data['prediction']
for disease in pred['predicted_diseases']:
    if 'Pneumonia' in disease['name']:
        print(f\"🎯 Predicted Disease: {disease['name']}\")
        print(f\"📊 Confidence: {disease['confidence']}\")
        print(f\"🔬 Supporting Evidence:\")
        for indicator in disease['indicators']:
            print(f\"   ✓ {indicator}\")
print(f\"\\n⚠️  Risk Level: {pred['risk_category']}\")
"
echo ""
sleep 2

# Demo 4: Multi-System Dysfunction
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏥 DEMO 4: MULTI-SYSTEM - Complex Case"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Patient: 61-year-old male"
echo "Scan: CT Abdomen - Fatty liver"
echo "Labs: ALT 68, AST 72, Cholesterol 245, LDL 165, Blood Sugar 118"
echo ""
echo "Analysis:"

RESULT=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 61, "gender": "male"},
    "scanInfo": {
      "scanType": "CT",
      "bodyPart": "Liver",
      "observedFindings": "fatty liver",
      "severity": "moderate"
    },
    "labValues": {
      "alt": 68,
      "ast": 72,
      "totalCholesterol": 245,
      "ldl": 165,
      "fastingBloodSugar": 118,
      "triglycerides": 210
    }
  }')

echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
pred = data['prediction']
print(f\"🎯 Multiple Conditions Detected:\")
for disease in pred['predicted_diseases'][:4]:
    print(f\"   • {disease['name']} ({disease['confidence']} confidence)\")
print(f\"\\n⚠️  Risk Level: {pred['risk_category']}\")
print(f\"\\n📋 Key Lab Abnormalities:\")
for abn in pred['supporting_evidence']['lab_abnormalities'][:4]:
    print(f\"   - {abn}\")
print(f\"\\n💡 Recommendations:\")
for rec in pred['recommended_next_steps'][:3]:
    print(f\"   → {rec}\")
"
echo ""
sleep 2

# Demo 5: Healthy Patient
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ DEMO 5: NORMAL PATIENT - No Conditions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Patient: 32-year-old female"
echo "Labs: All within normal ranges"
echo ""
echo "Analysis:"

RESULT=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "patientInfo": {"age": 32, "gender": "female"},
    "scanInfo": {},
    "labValues": {
      "hemoglobin": 13.8,
      "wbc": 7.2,
      "fastingBloodSugar": 88,
      "cholesterol": 175,
      "ldl": 95,
      "hdl": 58,
      "triglycerides": 110,
      "crp": 1.2
    }
  }')

echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
pred = data['prediction']
print(f\"🎯 Status: {pred['risk_category']}\")
if len(pred['predicted_diseases']) == 0:
    print(f\"✅ No significant conditions detected\")
else:
    print(f\"⚠️  Conditions detected: {len(pred['predicted_diseases'])}\")
print(f\"\\n💡 First Recommendation: {pred['recommended_next_steps'][0]}\")
"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Demo Complete!"
echo ""
echo "Key Features Demonstrated:"
echo "  ✓ Critical emergency detection (Stroke)"
echo "  ✓ Chronic disease identification (Diabetes)"
echo "  ✓ Acute infection diagnosis (Pneumonia)"
echo "  ✓ Multi-system analysis (Liver + Metabolic)"
echo "  ✓ Normal patient handling"
echo ""
echo "⚠️  REMEMBER: All predictions require professional validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
