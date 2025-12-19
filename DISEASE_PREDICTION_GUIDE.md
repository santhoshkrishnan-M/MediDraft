# 🎯 Disease Prediction Engine - Quick Start Guide

## Step-by-Step Tutorial

### 1️⃣ Access the Application
Open your web browser and navigate to:
```
http://localhost:3000/medical
```

### 2️⃣ Switch to Disease Prediction Mode
At the top of the page, you'll see two buttons:
- **Report Generation** (blue)
- **Disease Prediction** (gray)

Click on **"Disease Prediction"** to switch modes.

---

## 📝 Filling Out the Form

### Required Information ⚠️
These fields MUST be filled:
- **Age**: Enter patient's age (e.g., 45)
- **Gender**: Select Male, Female, or Other

### Optional but Recommended

#### Scan Information
- **Scan Type**: Choose X-ray, MRI, or CT Scan
- **Body Part**: Specify the area examined (e.g., Brain, Chest, Abdomen)
- **Observed Findings**: Describe what was seen in the scan
  - Examples: "lesion", "mass", "opacity", "nodule", "stone", "fracture"
- **Severity**: Select Mild, Moderate, or Severe

#### Laboratory Values
Fill in any available blood test results. Common ones include:
- **Hemoglobin**: Normal range 12-17 g/dL
- **WBC**: Normal range 4-11 x10³/μL
- **Fasting Blood Sugar**: Normal <100 mg/dL
- **Cholesterol**: Normal <200 mg/dL
- **Creatinine**: Normal 0.7-1.3 mg/dL

💡 **Tip**: You don't need to fill all fields. The system works with whatever data you provide.

---

## 🔍 Getting Predictions

### Click "🔍 Predict Diseases"
The system will:
1. Analyze all provided data
2. Apply medical rules to identify patterns
3. Generate predictions with confidence levels
4. Provide personalized recommendations

This usually takes 2-3 seconds.

---

## 📊 Understanding the Results

### Medical Disclaimer ⚠️
At the top, you'll see a prominent red warning box:
> "This is an AI-assisted prediction for informational purposes only. It is NOT a medical diagnosis."

**Always read this carefully!**

### Risk Assessment
You'll see your overall risk category:
- 🟢 **Normal**: No significant findings
- 🟡 **At Risk**: Some concerns detected
- 🔴 **Critical**: Immediate medical attention needed

### Predicted Conditions
Each predicted disease shows:
- **Disease Name**: What condition is suspected
- **Confidence Level**: High, Medium, or Low
- **Category**: Medical specialty (Neurological, Cardiac, etc.)
- **Supporting Indicators**: Why this was predicted

Example:
```
🎯 Possible Pneumonia
   Confidence: High
   Category: Respiratory
   Indicators:
   - Lung opacity/consolidation
   - Elevated WBC
```

### Supporting Evidence
Two sections show the data used:
- **🔬 Scan Findings**: What was observed in imaging
- **🩸 Lab Abnormalities**: Which blood tests were out of range

### Recommended Next Steps
Personalized recommendations such as:
- Consult with healthcare professional
- Schedule appointment with specialist
- Repeat laboratory tests
- Urgent care recommendations (if critical)

---

## 💡 Example Scenarios

### Scenario 1: Checking for Diabetes
**Input:**
- Age: 55
- Gender: Male
- Fasting Blood Sugar: 135 mg/dL
- HbA1c: 6.9%

**Expected Result:**
- Diabetes Mellitus detected
- High confidence
- Recommendations to see endocrinologist

---

### Scenario 2: Brain Scan Analysis
**Input:**
- Age: 48
- Gender: Female
- Scan Type: MRI
- Body Part: Brain
- Observed Findings: "lesion in frontal lobe"
- Severity: Moderate
- WBC: 12.5
- CRP: 15 mg/L

**Expected Result:**
- Possible Encephalitis
- High confidence
- Recommendation to see neurologist urgently

---

### Scenario 3: Chest X-ray with Labs
**Input:**
- Age: 62
- Gender: Male
- Scan Type: X-ray
- Body Part: Chest
- Observed Findings: "opacity right lower lobe"
- WBC: 14.5
- CRP: 8.2

**Expected Result:**
- Possible Pneumonia
- High confidence
- At Risk category

---

## ❓ Frequently Asked Questions

### Q: Can I use this instead of seeing a doctor?
**A: NO!** This tool is for educational and informational purposes only. Always consult qualified healthcare professionals for diagnosis and treatment.

### Q: What if I don't have scan results?
**A:** You can still get predictions based on lab values alone. The system will work with whatever data you provide.

### Q: What if I don't have all lab values?
**A:** Fill in what you have. Leave the rest blank. The system adapts to available data.

### Q: How accurate are the predictions?
**A:** The system uses rule-based medical logic, but it's NOT a replacement for professional medical diagnosis. Accuracy depends on the quality and completeness of input data.

### Q: What does "Confidence: High" mean?
**A:** It means multiple strong indicators support this prediction. However, even high-confidence predictions require professional validation.

### Q: Can I save or print the results?
**A:** Currently, results are displayed on screen. You can take screenshots or use your browser's print function.

### Q: What if it shows "Critical"?
**A:** Seek immediate medical attention. Do not delay. The system has detected potentially life-threatening conditions that require urgent evaluation.

### Q: Why does it show "Anemia" for most tests?
**A:** If hemoglobin is not provided or is 0, the system defaults to checking for anemia. Always enter actual lab values when available.

---

## 🚨 Important Reminders

1. ✅ **DO** use this as a preliminary screening tool
2. ✅ **DO** share results with your doctor
3. ✅ **DO** provide accurate, complete information
4. ✅ **DO** seek professional medical advice

5. ❌ **DON'T** self-diagnose based solely on these results
6. ❌ **DON'T** delay seeing a doctor if symptoms are present
7. ❌ **DON'T** start or stop medications without consulting a doctor
8. ❌ **DON'T** ignore critical warnings

---

## 🛠️ Troubleshooting

### Problem: "Please fill in Age and Gender"
**Solution:** These are required fields. You must enter values before prediction can run.

### Problem: No diseases predicted but I have symptoms
**Solution:** 
- The system may not have detected patterns from the data provided
- This doesn't mean you're healthy - consult a doctor
- Try entering more complete lab values

### Problem: Too many diseases predicted
**Solution:**
- System is showing all possible matches
- Focus on high-confidence predictions
- Share complete results with healthcare provider

### Problem: Page won't load
**Solution:**
- Ensure server is running: `./start.sh`
- Check http://localhost:3000/medical is accessible
- Clear browser cache and reload

---

## 📞 Need Help?

- **Documentation**: See DISEASE_PREDICTION.md for technical details
- **General Usage**: See USAGE.md for overall system guide
- **GitHub**: https://github.com/santhoshkrishnan-M/MediDraft

---

## 🔬 Behind the Scenes

When you click "Predict Diseases", the system:

1. **Validates Input**: Checks age and gender are provided
2. **Normalizes Data**: Converts all values to standard formats
3. **Identifies Abnormalities**: Compares lab values to reference ranges
4. **Applies Rules**: Matches patterns against disease criteria
5. **Scores Confidence**: Evaluates strength of evidence
6. **Assesses Risk**: Determines urgency level
7. **Generates Recommendations**: Creates personalized next steps
8. **Formats Output**: Displays results in user-friendly format

All of this happens in under 3 seconds!

---

**Remember: This is a decision support tool, not a medical diagnosis system. Always consult qualified healthcare professionals for proper diagnosis and treatment.**

---

*Last Updated: December 19, 2025*
