# Medical Report Drafting System - Usage Guide

## 🚀 Quick Start

### Start the Application
```bash
cd "/home/santhosh-krishnan-m/Desktop/Gen2 report/medical-report-motia-clean"
npm run dev
```

### Access the Application
Open your browser and navigate to: **http://localhost:3000/medical**

---

## 📋 How to Use

### Step 1: Upload Medical Image
1. Click the **"Click to upload or drag and drop"** area
2. Select a medical diagnostic image:
   - X-Ray (Chest, Bone, etc.)
   - MRI (Brain, Spine, etc.)
   - CT Scan (various types)
3. Supported formats: JPG, PNG, DICOM
4. Image preview will appear once uploaded

### Step 2: Enter Patient Information
Fill in the following required fields:
- **Patient ID**: Unique identifier (e.g., P001)
- **Patient Name**: Full name
- **Age**: Patient's age in years
- **Gender**: Male/Female/Other
- **Study Date**: Date of examination
- **Image Type**: Select from dropdown (X-Ray, MRI, CT Scan variants)

### Step 3: Enter Laboratory Results
Input the following lab values:
- **Hemoglobin (g/dL)**: Normal range 12-16 for females, 13-17 for males
- **Blood Sugar (mg/dL)**: Normal fasting <100
- **Cholesterol (mg/dL)**: Normal <200
- **Blood Pressure (mmHg)**: Format: 120/80
- **Creatinine (mg/dL)**: Normal 0.7-1.3

### Step 4: Generate Report
1. Click **"Start Analysis"** button
2. System will process:
   - ✅ Image analysis
   - ✅ Lab results interpretation
   - ✅ Comprehensive report generation
   - ✅ AI-powered diet recommendations
3. Wait for processing (typically 5-10 seconds)

### Step 5: View and Download Report
1. Review the comprehensive medical report with:
   - Patient summary
   - Imaging findings
   - Laboratory results
   - Clinical impressions
   - Risk indicators
   - Personalized diet plan (AI-generated)
2. Click **"Download PDF Report"** to save the report

---

## 🔌 API Endpoints

All endpoints are available at `http://localhost:3000`

### Frontend
- `GET /medical` - Main application interface
- `GET /app.js` - Application JavaScript

### Medical APIs
- `POST /api/analyze-image` - Analyze diagnostic images
- `POST /api/analyze-lab-results` - Analyze laboratory test results
- `POST /api/generate-report` - Generate comprehensive medical report
- `POST /api/generate-diet` - Generate AI-powered diet recommendations
- `POST /api/generate-pdf` - Generate PDF report

---

## 🔧 System Requirements

### Runtime
- Node.js 18+ with npm
- Python 3.12+
- Redis server (running on port 6379)

### Python Dependencies
- google-generativeai (AI diet recommendations)
- Pillow (image processing)
- reportlab (PDF generation)
- pydantic, httpx, python-multipart, python-dotenv

### Environment Variables
Create `.env` file with:
```
GEMINI_API_KEY=your_google_gemini_api_key
```

---

## ⚙️ Configuration

### Redis Setup
System uses Redis for background job processing:
- Host: 127.0.0.1
- Port: 6379
- Configured in `motia.config.ts`

### Motia Framework
Built on Motia 0.17.9-beta.191:
- Python API steps for medical processing
- Endpoint plugin for REST APIs
- Observability and logging enabled

---

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check if port 3000 is in use
lsof -i :3000

# Check if Redis is running
sudo systemctl status redis-server

# Restart Redis if needed
sudo systemctl restart redis-server
```

### Image Upload Fails
- Check browser console for JavaScript errors (F12)
- Ensure image file size is reasonable (<10MB)
- Supported formats: JPG, PNG

### API Errors
- Check server logs in terminal
- Verify `.env` file contains valid GEMINI_API_KEY
- Ensure all Python dependencies are installed

### Diet Recommendations Not Working
- Verify Gemini API key is valid
- Check internet connectivity
- Review server logs for API errors

---

## 📊 Features

### ✅ Completed Features
1. **Image Analysis**: Analyzes medical diagnostic images
2. **Lab Results Processing**: Interprets laboratory test values
3. **Report Generation**: Creates comprehensive medical reports
4. **AI Diet Recommendations**: Uses Google Gemini AI for personalized nutrition plans
5. **PDF Export**: Professional PDF report generation
6. **Real-time Progress**: Visual progress tracking during analysis
7. **Error Handling**: Comprehensive error messages and validation

### 🎨 User Interface
- Modern, responsive design with Tailwind CSS
- Drag-and-drop image upload
- Real-time status updates
- Progress indicators
- Professional report display

---

## 🔐 Security Notes

- System runs locally (localhost:3000)
- No data is stored permanently
- Gemini API key should be kept secure
- Patient data processed in memory only

---

## 📝 Sample Test Data

### Test Patient Info
- Patient ID: P12345
- Name: John Doe
- Age: 45
- Gender: Male
- Study Date: Today's date

### Test Lab Results
- Hemoglobin: 14.5 g/dL
- Blood Sugar: 95 mg/dL
- Cholesterol: 185 mg/dL
- Blood Pressure: 120/80 mmHg
- Creatinine: 1.0 mg/dL

---

## 💡 Tips for Best Results

1. **Image Quality**: Use clear, high-resolution medical images
2. **Accurate Data**: Enter precise lab values for accurate analysis
3. **Complete Information**: Fill all fields for comprehensive reports
4. **Review Reports**: Always review AI-generated recommendations with medical professionals
5. **Regular Updates**: Keep the system updated for latest features

---

## 📞 Support

For issues or questions:
- Check server logs in terminal
- Review browser console (F12) for errors
- Verify all dependencies are installed
- Ensure Redis server is running

---

## ⚠️ Medical Disclaimer

This system is for educational and demonstration purposes only. All medical analyses, reports, and recommendations should be reviewed by qualified healthcare professionals. Do not use for actual medical diagnosis or treatment decisions.

---

**Version**: 1.0.0  
**Framework**: Motia 0.17.9-beta.191  
**Last Updated**: December 2025
