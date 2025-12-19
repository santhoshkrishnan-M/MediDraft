let uploadedImageData = null;
let imagingFindings = null;
let labAnalysis = null;
let generatedReport = null;
let dietRecommendation = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('studyDate').value = today;
    
    setupFileUpload();
    setupEventListeners();
}

function setupFileUpload() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    
    dropZone.addEventListener('click', () => fileInput.click());
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('bg-blue-200');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('bg-blue-200');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('bg-blue-200');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        uploadedImageData = e.target.result;
        
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileSize').textContent = formatFileSize(file.size);
        document.getElementById('filePreview').classList.remove('hidden');
        document.getElementById('analyzeBtn').disabled = false;
        
        updateProgressStep(1, 'complete');
        
        showStatus('success', 'Image uploaded successfully');
    };
    
    reader.readAsDataURL(file);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function setupEventListeners() {
    document.getElementById('analyzeBtn').addEventListener('click', analyzeImage);
    document.getElementById('generateReportBtn').addEventListener('click', generateReport);
    document.getElementById('downloadPdfBtn').addEventListener('click', downloadPDF);
    
    // Mode switching
    document.getElementById('reportModeBtn').addEventListener('click', switchToReportMode);
    document.getElementById('predictionModeBtn').addEventListener('click', switchToPredictionMode);
    
    // Disease prediction
    document.getElementById('predictDiseaseBtn').addEventListener('click', predictDisease);
}

function switchToReportMode() {
    document.getElementById('reportMode').classList.remove('hidden');
    document.getElementById('predictionMode').classList.add('hidden');
    
    document.getElementById('reportModeBtn').classList.add('bg-blue-600', 'text-white');
    document.getElementById('reportModeBtn').classList.remove('bg-gray-200', 'text-gray-700');
    
    document.getElementById('predictionModeBtn').classList.add('bg-gray-200', 'text-gray-700');
    document.getElementById('predictionModeBtn').classList.remove('bg-blue-600', 'text-white');
}

function switchToPredictionMode() {
    document.getElementById('reportMode').classList.add('hidden');
    document.getElementById('predictionMode').classList.remove('hidden');
    
    document.getElementById('predictionModeBtn').classList.add('bg-blue-600', 'text-white');
    document.getElementById('predictionModeBtn').classList.remove('bg-gray-200', 'text-gray-700');
    
    document.getElementById('reportModeBtn').classList.add('bg-gray-200', 'text-gray-700');
    document.getElementById('reportModeBtn').classList.remove('bg-blue-600', 'text-white');
}

async function analyzeImage() {
    if (!validatePatientInfo()) {
        showError('Please fill in all patient information fields');
        return;
    }
    
    if (!uploadedImageData) {
        showError('Please upload an image first');
        return;
    }
    
    showStatus('loading', 'Analyzing Image and Generating Report...<br>Please wait.');
    updateProgressStep(2, 'active');
    
    try {
        const response = await fetch('/api/analyze-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: uploadedImageData,
                imageType: document.getElementById('imageType').value
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            imagingFindings = result.findings;
            
            updateProgressStep(2, 'complete');
            updateProgressStep(3, 'active');
            
            document.getElementById('labResultsCard').classList.remove('hidden');
            
            showStatus('success', 'Image Analysis Complete. Report Generated Successfully.');
            
            setTimeout(() => {
                document.getElementById('labResultsCard').scrollIntoView({ behavior: 'smooth' });
            }, 500);
        } else {
            throw new Error(result.error || 'Image analysis failed');
        }
    } catch (error) {
        console.error('Error analyzing image:', error);
        showError('Failed to analyze image: ' + error.message);
        updateProgressStep(2, 'inactive');
    }
}

async function generateReport() {
    showStatus('loading', 'Generating comprehensive medical report...<br>Please wait.');
    
    try {
        const labResults = getLabResults();
        
        const labResponse = await fetch('/api/analyze-lab-results', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                labResults: labResults
            })
        });
        
        const labResult = await labResponse.json();
        
        if (!labResult.success) {
            throw new Error(labResult.error || 'Lab analysis failed');
        }
        
        labAnalysis = labResult.analysis;
        
        const patientInfo = getPatientInfo();
        
        const reportResponse = await fetch('/api/generate-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                patientInfo: patientInfo,
                imagingFindings: imagingFindings,
                labAnalysis: labAnalysis
            })
        });
        
        const reportResult = await reportResponse.json();
        
        if (!reportResult.success) {
            throw new Error(reportResult.error || 'Report generation failed');
        }
        
        generatedReport = reportResult.report;
        
        showStatus('loading', 'Generating personalized diet recommendations using AI...<br>Please wait.');
        
        const dietResponse = await fetch('/api/generate-diet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                patientInfo: patientInfo,
                riskIndicators: labAnalysis.riskIndicators || [],
                abnormalities: labAnalysis.abnormalities || []
            })
        });
        
        const dietResult = await dietResponse.json();
        
        if (dietResult.success) {
            dietRecommendation = dietResult.dietRecommendation;
        } else {
            console.warn('Diet generation failed, using fallback:', dietResult.error);
            dietRecommendation = dietResult.fallback || generateBasicDiet();
        }
        
        updateProgressStep(3, 'complete');
        
        displayReport();
        
        showStatus('success', 'Complete medical report with AI-powered diet recommendations generated successfully!');
        
        setTimeout(() => {
            document.getElementById('reportCard').scrollIntoView({ behavior: 'smooth' });
        }, 500);
        
    } catch (error) {
        console.error('Error generating report:', error);
        showError('Failed to generate report: ' + error.message);
    }
}

function displayReport() {
    const reportContent = document.getElementById('reportContent');
    reportContent.innerHTML = '';
    
    const sections = [
        createPatientSummarySection(),
        createImagingFindingsSection(),
        createLabResultsSection(),
        createClinicalImpressionSection(),
        createRiskIndicatorsSection(),
        createDietRecommendationSection(),
        createNextStepsSection()
    ];
    
    sections.forEach(section => {
        if (section) {
            reportContent.appendChild(section);
        }
    });
    
    document.getElementById('reportCard').classList.remove('hidden');
}

function createPatientSummarySection() {
    const section = document.createElement('div');
    section.className = 'border-b pb-4';
    
    const summary = generatedReport.patientSummary;
    
    section.innerHTML = `
        <h3 class="text-xl font-bold text-blue-700 mb-3">Patient Summary</h3>
        <div class="grid grid-cols-2 gap-3 text-sm">
            <div><span class="font-semibold">Patient ID:</span> ${summary.patientId}</div>
            <div><span class="font-semibold">Study Date:</span> ${summary.studyDate}</div>
            <div><span class="font-semibold">Name:</span> ${summary.patientName}</div>
            <div><span class="font-semibold">Image Type:</span> ${summary.imageType}</div>
            <div><span class="font-semibold">Age:</span> ${summary.age} years</div>
            <div><span class="font-semibold">Gender:</span> ${summary.gender}</div>
        </div>
    `;
    
    return section;
}

function createImagingFindingsSection() {
    const section = document.createElement('div');
    section.className = 'border-b pb-4';
    
    const findings = generatedReport.imagingFindings;
    
    const findingsList = findings.findings.map(f => `<li class="mb-1">• ${f}</li>`).join('');
    
    section.innerHTML = `
        <h3 class="text-xl font-bold text-blue-700 mb-3">Imaging Findings</h3>
        <div class="text-sm space-y-2">
            <p><span class="font-semibold">Modality:</span> ${findings.modality}</p>
            <p><span class="font-semibold">Quality:</span> ${findings.quality}</p>
            <div>
                <p class="font-semibold mb-1">Findings:</p>
                <ul class="ml-4">${findingsList}</ul>
            </div>
            <p><span class="font-semibold">Impression:</span> ${findings.impression}</p>
        </div>
    `;
    
    return section;
}

function createLabResultsSection() {
    const section = document.createElement('div');
    section.className = 'border-b pb-4';
    
    const lab = generatedReport.labResults;
    
    let resultsTable = '';
    if (lab.results && lab.results.length > 0) {
        resultsTable = `
            <div class="overflow-x-auto">
                <table class="w-full text-sm border-collapse">
                    <thead>
                        <tr class="bg-blue-100">
                            <th class="border p-2 text-left">Test</th>
                            <th class="border p-2 text-left">Value</th>
                            <th class="border p-2 text-left">Normal Range</th>
                            <th class="border p-2 text-left">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${lab.results.map(r => `
                            <tr>
                                <td class="border p-2">${r.test}</td>
                                <td class="border p-2">${r.value} ${r.unit}</td>
                                <td class="border p-2">${r.normalRange}</td>
                                <td class="border p-2 ${r.status === 'Normal' ? 'text-green-600' : 'text-red-600'} font-semibold">${r.status}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }
    
    let abnormalitiesList = '';
    if (lab.abnormalities && lab.abnormalities.length > 0) {
        abnormalitiesList = `
            <div class="mt-3">
                <p class="font-semibold text-red-600 mb-1">Abnormalities Detected:</p>
                <ul class="ml-4">
                    ${lab.abnormalities.map(a => `<li class="mb-1">• ${a}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    section.innerHTML = `
        <h3 class="text-xl font-bold text-blue-700 mb-3">Lab Result Interpretation</h3>
        ${resultsTable}
        ${abnormalitiesList}
        <p class="mt-3 text-sm"><span class="font-semibold">Interpretation:</span> ${lab.interpretation}</p>
    `;
    
    return section;
}

function createClinicalImpressionSection() {
    const section = document.createElement('div');
    section.className = 'border-b pb-4';
    
    section.innerHTML = `
        <h3 class="text-xl font-bold text-blue-700 mb-3">Clinical Impression</h3>
        <p class="text-sm">${generatedReport.clinicalImpression}</p>
    `;
    
    return section;
}

function createRiskIndicatorsSection() {
    if (!generatedReport.riskIndicators || generatedReport.riskIndicators.length === 0) {
        return null;
    }
    
    const section = document.createElement('div');
    section.className = 'border-b pb-4';
    
    const risksList = generatedReport.riskIndicators.map(r => 
        `<span class="inline-block bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium mr-2 mb-2">⚠ ${r}</span>`
    ).join('');
    
    section.innerHTML = `
        <h3 class="text-xl font-bold text-blue-700 mb-3">Risk Indicators</h3>
        <div>${risksList}</div>
    `;
    
    return section;
}

function createDietRecommendationSection() {
    if (!dietRecommendation) {
        return null;
    }
    
    const section = document.createElement('div');
    section.className = 'border-b pb-4 bg-green-50 p-4 rounded';
    
    let content = `<h3 class="text-xl font-bold text-green-700 mb-3">🥗 Diet Recommendation (AI-Generated)</h3>`;
    
    if (dietRecommendation.overview) {
        content += `<p class="text-sm mb-3 italic">${dietRecommendation.overview}</p>`;
    }
    
    if (dietRecommendation.vegetarianFoods && dietRecommendation.vegetarianFoods.length > 0) {
        content += `
            <div class="mb-3">
                <p class="font-semibold text-sm mb-1">Recommended Foods (Vegetarian):</p>
                <ul class="ml-4 text-sm">
                    ${dietRecommendation.vegetarianFoods.map(f => `<li class="mb-1">• ${f}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (dietRecommendation.nonVegetarianFoods && dietRecommendation.nonVegetarianFoods.length > 0) {
        content += `
            <div class="mb-3">
                <p class="font-semibold text-sm mb-1">Recommended Foods (Non-Vegetarian):</p>
                <ul class="ml-4 text-sm">
                    ${dietRecommendation.nonVegetarianFoods.map(f => `<li class="mb-1">• ${f}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (dietRecommendation.foodsToAvoid && dietRecommendation.foodsToAvoid.length > 0) {
        content += `
            <div class="mb-3">
                <p class="font-semibold text-sm mb-1 text-red-600">Foods to Avoid:</p>
                <ul class="ml-4 text-sm">
                    ${dietRecommendation.foodsToAvoid.map(f => `<li class="mb-1">• ${f}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (dietRecommendation.lifestyleTips && dietRecommendation.lifestyleTips.length > 0) {
        content += `
            <div class="mb-3">
                <p class="font-semibold text-sm mb-1">Lifestyle & Hydration Tips:</p>
                <ul class="ml-4 text-sm">
                    ${dietRecommendation.lifestyleTips.map(t => `<li class="mb-1">• ${t}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    section.innerHTML = content;
    return section;
}

function createNextStepsSection() {
    const section = document.createElement('div');
    section.className = 'pb-4';
    
    const stepsList = generatedReport.recommendedNextSteps.map(s => `<li class="mb-2">• ${s}</li>`).join('');
    
    section.innerHTML = `
        <h3 class="text-xl font-bold text-blue-700 mb-3">Recommended Next Steps</h3>
        <ul class="ml-4 text-sm">${stepsList}</ul>
    `;
    
    return section;
}

async function downloadPDF() {
    showStatus('loading', 'Generating PDF report...');
    
    try {
        const response = await fetch('/api/generate-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                report: generatedReport,
                dietRecommendation: dietRecommendation
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            const link = document.createElement('a');
            link.href = 'data:application/pdf;base64,' + result.pdf;
            link.download = result.filename;
            link.click();
            
            showStatus('success', 'PDF downloaded successfully!');
        } else {
            throw new Error(result.error || 'PDF generation failed');
        }
    } catch (error) {
        console.error('Error generating PDF:', error);
        showError('Failed to generate PDF: ' + error.message);
    }
}

function getPatientInfo() {
    return {
        patientId: document.getElementById('patientId').value || 'N/A',
        patientName: document.getElementById('patientName').value || 'N/A',
        age: document.getElementById('age').value || 'N/A',
        gender: document.getElementById('gender').value || 'N/A',
        studyDate: document.getElementById('studyDate').value || 'N/A',
        imageType: document.getElementById('imageType').value || 'N/A'
    };
}

function getLabResults() {
    return {
        hemoglobin: document.getElementById('hemoglobin').value || 0,
        bloodSugar: document.getElementById('bloodSugar').value || 0,
        cholesterol: document.getElementById('cholesterol').value || 0,
        bpSystolic: document.getElementById('bpSystolic').value || 0,
        bpDiastolic: document.getElementById('bpDiastolic').value || 0,
        creatinine: document.getElementById('creatinine').value || 0
    };
}

function validatePatientInfo() {
    const patientId = document.getElementById('patientId').value;
    const patientName = document.getElementById('patientName').value;
    const age = document.getElementById('age').value;
    
    return patientId && patientName && age;
}

function updateProgressStep(step, status) {
    const stepElement = document.getElementById(`step${step}`);
    
    stepElement.classList.remove('step-inactive', 'step-active', 'step-complete');
    
    if (status === 'active') {
        stepElement.classList.add('step-active');
    } else if (status === 'complete') {
        stepElement.classList.add('step-complete');
    } else {
        stepElement.classList.add('step-inactive');
    }
}

function showStatus(type, message) {
    const statusArea = document.getElementById('statusArea');
    
    if (type === 'loading') {
        statusArea.innerHTML = `
            <div class="flex items-center gap-3 text-blue-600">
                <svg class="animate-spin h-8 w-8" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <div>
                    <p class="font-medium">${message}</p>
                </div>
            </div>
        `;
    } else if (type === 'success') {
        statusArea.innerHTML = `
            <div class="flex items-center gap-3 text-green-600">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <div>
                    <p class="font-medium">${message}</p>
                </div>
            </div>
        `;
    } else if (type === 'error') {
        statusArea.innerHTML = `
            <div class="flex items-center gap-3 text-red-600">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <div>
                    <p class="font-medium">${message}</p>
                </div>
            </div>
        `;
    }
}

function showError(message) {
    showStatus('error', message);
}

// ===================================
// DISEASE PREDICTION FUNCTIONALITY
// ===================================

async function predictDisease() {
    // Validate required fields
    const age = document.getElementById('predAge').value;
    const gender = document.getElementById('predGender').value;
    
    if (!age || !gender) {
        alert('Please fill in Age and Gender (required fields)');
        return;
    }
    
    // Collect patient info
    const patientInfo = {
        age: parseInt(age),
        gender: gender
    };
    
    // Collect scan info
    const scanInfo = {
        scanType: document.getElementById('predScanType').value,
        bodyPart: document.getElementById('predBodyPart').value,
        observedFindings: document.getElementById('predFindings').value,
        severity: document.getElementById('predSeverity').value
    };
    
    // Collect lab values
    const labValues = {
        hemoglobin: document.getElementById('predHb').value,
        hb: document.getElementById('predHb').value,
        wbc: document.getElementById('predWbc').value,
        platelet: document.getElementById('predPlatelet').value,
        fastingBloodSugar: document.getElementById('predFbs').value,
        bloodSugar: document.getElementById('predFbs').value,
        hba1c: document.getElementById('predHba1c').value,
        totalCholesterol: document.getElementById('predCholesterol').value,
        cholesterol: document.getElementById('predCholesterol').value,
        ldl: document.getElementById('predLdl').value,
        hdl: document.getElementById('predHdl').value,
        triglycerides: document.getElementById('predTriglycerides').value,
        crp: document.getElementById('predCrp').value,
        esr: document.getElementById('predEsr').value,
        creatinine: document.getElementById('predCreatinine').value,
        urea: document.getElementById('predUrea').value,
        bun: document.getElementById('predUrea').value,
        alt: document.getElementById('predAlt').value,
        ast: document.getElementById('predAst').value
    };
    
    // Show loading state
    const btn = document.getElementById('predictDiseaseBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="animate-spin inline-block mr-2">⏳</span> Analyzing...';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/predict-disease', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                patientInfo,
                scanInfo,
                labValues
            })
        });
        
        const result = await response.json();
        
        if (result.success && result.prediction) {
            displayPredictionResults(result.prediction);
        } else {
            alert('Prediction failed: ' + (result.error || 'Unknown error'));
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to predict diseases: ' + error.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function displayPredictionResults(prediction) {
    const resultsDiv = document.getElementById('predictionResults');
    const contentDiv = document.getElementById('predictionContent');
    
    let html = '';
    
    // Medical Disclaimer (Prominent)
    html += `
        <div class="bg-red-50 border-2 border-red-300 rounded-lg p-4 mb-6">
            <div class="flex gap-3">
                <svg class="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>
                <div>
                    <h3 class="font-bold text-red-800 text-lg mb-2">⚠️ MEDICAL DISCLAIMER</h3>
                    <p class="text-red-700 font-medium">${prediction.medical_disclaimer}</p>
                </div>
            </div>
        </div>
    `;
    
    // Risk Category Badge
    let riskColor = 'gray';
    if (prediction.risk_category.includes('Critical')) {
        riskColor = 'red';
    } else if (prediction.risk_category.includes('At Risk')) {
        riskColor = 'orange';
    } else {
        riskColor = 'green';
    }
    
    html += `
        <div class="flex items-center justify-between mb-6">
            <div>
                <h3 class="text-lg font-semibold text-gray-700">Risk Assessment</h3>
                <div class="mt-2">
                    <span class="px-4 py-2 bg-${riskColor}-100 text-${riskColor}-800 rounded-full font-bold text-lg">
                        ${prediction.risk_category}
                    </span>
                </div>
            </div>
            <div>
                <h3 class="text-lg font-semibold text-gray-700">Confidence Level</h3>
                <div class="mt-2">
                    <span class="px-4 py-2 bg-blue-100 text-blue-800 rounded-full font-bold text-lg">
                        ${prediction.confidence_level}
                    </span>
                </div>
            </div>
        </div>
    `;
    
    // Predicted Diseases
    if (prediction.predicted_diseases && prediction.predicted_diseases.length > 0) {
        html += `
            <div class="mb-6">
                <h3 class="text-xl font-bold text-gray-800 mb-4">🎯 Predicted Conditions</h3>
                <div class="space-y-4">
        `;
        
        prediction.predicted_diseases.forEach(disease => {
            const confColor = disease.confidence === 'High' ? 'red' : disease.confidence === 'Medium' ? 'yellow' : 'blue';
            const isCritical = disease.category.includes('CRITICAL');
            
            html += `
                <div class="border-2 ${isCritical ? 'border-red-400 bg-red-50' : 'border-gray-200 bg-white'} rounded-lg p-4">
                    <div class="flex items-start justify-between mb-2">
                        <div class="flex-1">
                            <h4 class="text-lg font-bold text-gray-800 ${isCritical ? 'text-red-700' : ''}">
                                ${isCritical ? '🚨 ' : ''}${disease.name}
                            </h4>
                            <p class="text-sm text-gray-600 mt-1">${disease.category}</p>
                        </div>
                        <span class="px-3 py-1 bg-${confColor}-100 text-${confColor}-800 rounded-full text-sm font-semibold">
                            ${disease.confidence} Confidence
                        </span>
                    </div>
                    <div class="mt-3">
                        <p class="text-sm font-semibold text-gray-700 mb-1">Supporting Indicators:</p>
                        <ul class="list-disc list-inside text-sm text-gray-600 space-y-1">
            `;
            
            disease.indicators.forEach(indicator => {
                if (indicator) {
                    html += `<li>${indicator}</li>`;
                }
            });
            
            html += `
                        </ul>
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    } else {
        html += `
            <div class="mb-6 p-6 bg-green-50 border border-green-200 rounded-lg">
                <div class="flex items-center gap-3">
                    <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <div>
                        <h3 class="text-lg font-bold text-green-800">No Significant Conditions Detected</h3>
                        <p class="text-green-700">Based on the provided data, no specific disease patterns were identified.</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Supporting Evidence
    html += `
        <div class="mb-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">📊 Supporting Evidence</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    `;
    
    // Scan Findings
    html += `
        <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
            <h4 class="font-bold text-gray-700 mb-2">🔬 Scan Findings</h4>
    `;
    if (prediction.supporting_evidence.scan_findings.length > 0) {
        html += '<ul class="list-disc list-inside text-sm text-gray-700 space-y-1">';
        prediction.supporting_evidence.scan_findings.forEach(finding => {
            html += `<li>${finding}</li>`;
        });
        html += '</ul>';
    } else {
        html += '<p class="text-sm text-gray-500 italic">No scan findings recorded</p>';
    }
    html += '</div>';
    
    // Lab Abnormalities
    html += `
        <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
            <h4 class="font-bold text-gray-700 mb-2">🩸 Lab Abnormalities</h4>
    `;
    if (prediction.supporting_evidence.lab_abnormalities.length > 0) {
        html += '<ul class="list-disc list-inside text-sm text-gray-700 space-y-1">';
        prediction.supporting_evidence.lab_abnormalities.forEach(abn => {
            html += `<li>${abn}</li>`;
        });
        html += '</ul>';
    } else {
        html += '<p class="text-sm text-gray-500 italic">All lab values within normal ranges</p>';
    }
    html += '</div>';
    
    html += `
            </div>
        </div>
    `;
    
    // Recommendations
    html += `
        <div class="mb-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">💡 Recommended Next Steps</h3>
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <ul class="space-y-2">
    `;
    
    prediction.recommended_next_steps.forEach(step => {
        const isUrgent = step.includes('🚨') || step.includes('URGENT');
        html += `
            <li class="flex items-start gap-2">
                <span class="${isUrgent ? 'text-red-600' : 'text-blue-600'} font-bold">•</span>
                <span class="text-gray-700 ${isUrgent ? 'font-bold text-red-700' : ''}">${step}</span>
            </li>
        `;
    });
    
    html += `
                </ul>
            </div>
        </div>
    `;
    
    contentDiv.innerHTML = html;
    resultsDiv.classList.remove('hidden');
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function generateBasicDiet() {
    return {
        overview: 'A balanced diet plan focusing on whole foods, adequate hydration, and healthy lifestyle practices.',
        vegetarianFoods: [
            'Whole grains like brown rice and wheat',
            'Green vegetables and salads',
            'Lentils and legumes',
            'Nuts and seeds'
        ],
        nonVegetarianFoods: [
            'Lean chicken',
            'Fish rich in omega-3',
            'Eggs'
        ],
        foodsToAvoid: [
            'Processed foods',
            'Excessive salt and sugar',
            'Deep fried items'
        ],
        lifestyleTips: [
            'Drink 8-10 glasses of water daily',
            'Exercise regularly',
            'Get adequate sleep'
        ]
    };
}
