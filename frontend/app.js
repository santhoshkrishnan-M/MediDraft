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
