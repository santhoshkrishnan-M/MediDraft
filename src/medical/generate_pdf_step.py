from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import base64

# Motia API configuration
config = {
    "name": "GeneratePDF",
    "type": "api",
    "path": "/api/generate-pdf",
    "method": "POST",
    "description": "Generate PDF report from medical data and diet recommendations",
    "emits": [],
    "responseSchema": {
        200: {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "pdf": {"type": "string"},
                "filename": {"type": "string"}
            }
        }
    }
}

async def handler(req, context):
    """Motia API handler for PDF generation"""
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
        
        result = generate_pdf(data)
        return {"status": 200, "body": result}
    except Exception as e:
        context.logger.error(f"PDF generation error: {str(e)}")
        return {
            "status": 500,
            "body": {"success": False, "error": str(e)}
        }

def generate_pdf(data):
    """Generate PDF report from medical data"""
    
    try:
        report = data.get('report', {})
        diet_recommendation = data.get('dietRecommendation', {})
        
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )
        
        story.append(Paragraph("MEDICAL REPORT", title_style))
        story.append(Paragraph("AI-Assisted Diagnostic Report", subtitle_style))
        story.append(Spacer(1, 0.2*inch))
        
        patient_summary = report.get('patientSummary', {})
        story.append(Paragraph("PATIENT INFORMATION", heading_style))
        
        patient_data = [
            ['Report ID:', report.get('reportId', 'N/A')],
            ['Patient ID:', patient_summary.get('patientId', 'N/A')],
            ['Patient Name:', patient_summary.get('patientName', 'N/A')],
            ['Age:', f"{patient_summary.get('age', 'N/A')} years"],
            ['Gender:', patient_summary.get('gender', 'N/A')],
            ['Study Date:', patient_summary.get('studyDate', 'N/A')],
            ['Image Type:', patient_summary.get('imageType', 'N/A')],
            ['Report Generated:', report.get('generatedDate', 'N/A')]
        ]
        
        patient_table = Table(patient_data, colWidths=[2*inch, 4.5*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 0.3*inch))
        
        imaging_findings = report.get('imagingFindings', {})
        story.append(Paragraph("IMAGING FINDINGS", heading_style))
        story.append(Paragraph(f"<b>Modality:</b> {imaging_findings.get('modality', 'N/A')}", normal_style))
        story.append(Paragraph(f"<b>Quality:</b> {imaging_findings.get('quality', 'N/A')}", normal_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph("<b>Findings:</b>", normal_style))
        
        for finding in imaging_findings.get('findings', []):
            story.append(Paragraph(f"• {finding}", normal_style))
        
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(f"<b>Impression:</b> {imaging_findings.get('impression', 'N/A')}", normal_style))
        story.append(Spacer(1, 0.3*inch))
        
        lab_results = report.get('labResults', {})
        if lab_results.get('results'):
            story.append(Paragraph("LABORATORY RESULTS", heading_style))
            
            lab_data = [['Test', 'Value', 'Normal Range', 'Status']]
            
            for result in lab_results.get('results', []):
                status_color = 'green' if result.get('status') == 'Normal' else 'red'
                lab_data.append([
                    result.get('test', ''),
                    f"{result.get('value', '')} {result.get('unit', '')}",
                    result.get('normalRange', ''),
                    result.get('status', '')
                ])
            
            lab_table = Table(lab_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            lab_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            
            story.append(lab_table)
            story.append(Spacer(1, 0.2*inch))
            
            if lab_results.get('abnormalities'):
                story.append(Paragraph("<b>Abnormalities Detected:</b>", normal_style))
                for abnormality in lab_results.get('abnormalities', []):
                    story.append(Paragraph(f"• {abnormality}", normal_style))
                story.append(Spacer(1, 0.1*inch))
            
            story.append(Paragraph(f"<b>Interpretation:</b> {lab_results.get('interpretation', 'N/A')}", normal_style))
            story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("CLINICAL IMPRESSION", heading_style))
        story.append(Paragraph(report.get('clinicalImpression', 'No clinical impression available'), normal_style))
        story.append(Spacer(1, 0.3*inch))
        
        risk_indicators = report.get('riskIndicators', [])
        if risk_indicators:
            story.append(Paragraph("RISK INDICATORS", heading_style))
            for risk in risk_indicators:
                story.append(Paragraph(f"• {risk}", normal_style))
            story.append(Spacer(1, 0.3*inch))
        
        if diet_recommendation:
            story.append(PageBreak())
            story.append(Paragraph("PERSONALIZED DIET RECOMMENDATIONS", heading_style))
            story.append(Paragraph("<i>Generated by AI-powered nutrition analysis</i>", normal_style))
            story.append(Spacer(1, 0.2*inch))
            
            if diet_recommendation.get('overview'):
                story.append(Paragraph("<b>Overview:</b>", normal_style))
                story.append(Paragraph(diet_recommendation.get('overview'), normal_style))
                story.append(Spacer(1, 0.2*inch))
            
            if diet_recommendation.get('vegetarianFoods'):
                story.append(Paragraph("<b>Recommended Foods (Vegetarian):</b>", normal_style))
                for food in diet_recommendation.get('vegetarianFoods', []):
                    story.append(Paragraph(f"• {food}", normal_style))
                story.append(Spacer(1, 0.2*inch))
            
            if diet_recommendation.get('nonVegetarianFoods'):
                story.append(Paragraph("<b>Recommended Foods (Non-Vegetarian):</b>", normal_style))
                for food in diet_recommendation.get('nonVegetarianFoods', []):
                    story.append(Paragraph(f"• {food}", normal_style))
                story.append(Spacer(1, 0.2*inch))
            
            if diet_recommendation.get('foodsToAvoid'):
                story.append(Paragraph("<b>Foods to Avoid:</b>", normal_style))
                for food in diet_recommendation.get('foodsToAvoid', []):
                    story.append(Paragraph(f"• {food}", normal_style))
                story.append(Spacer(1, 0.2*inch))
            
            if diet_recommendation.get('lifestyleTips'):
                story.append(Paragraph("<b>Lifestyle & Hydration Tips:</b>", normal_style))
                for tip in diet_recommendation.get('lifestyleTips', []):
                    story.append(Paragraph(f"• {tip}", normal_style))
                story.append(Spacer(1, 0.2*inch))
        
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("RECOMMENDED NEXT STEPS", heading_style))
        for step in report.get('recommendedNextSteps', []):
            story.append(Paragraph(f"• {step}", normal_style))
        
        story.append(Spacer(1, 0.5*inch))
        
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#dc2626'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("⚠ IMPORTANT DISCLAIMER ⚠", disclaimer_style))
        story.append(Paragraph(
            "This AI-generated report is for clinical assistance and educational purposes only. "
            "It must be reviewed, verified, and interpreted by a licensed medical professional. "
            "This report does not constitute a medical diagnosis and should not be used as the sole basis for medical decisions.",
            normal_style
        ))
        
        doc.build(story)
        
        pdf_data = buffer.getvalue()
        buffer.close()
        
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        
        return {
            'success': True,
            'pdf': pdf_base64,
            'filename': f"Medical_Report_{report.get('reportId', 'Unknown')}.pdf"
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
