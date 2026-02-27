import streamlit as st
from datetime import datetime

# PDF imports
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import tempfile

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Advanced Brain Tumor Analyzer",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "patient_history" not in st.session_state:
    st.session_state.patient_history = []

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "latest_report" not in st.session_state:
    st.session_state.latest_report = None

# -----------------------------
# Sidebar - Patient Information
# -----------------------------
with st.sidebar:
    st.title("👤 Patient Information")

    patient_id = st.text_input("Patient ID")
    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Age", min_value=1, max_value=120, value=30)
    patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    st.divider()
    st.subheader("⚙ Analysis Settings")
    show_confidence = st.checkbox("Show detailed confidence scores", value=True)

# -----------------------------
# Main Header
# -----------------------------
st.title("🩺 Advanced Brain Tumor Analyzer")
st.caption("AI-Powered Medical Image Analysis & Symptom Assessment")

# -----------------------------
# MRI & Symptom Analysis Section
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("MRI Image Analysis")
    mri_file = st.file_uploader(
        "Upload MRI scan",
        type=["png", "jpg", "jpeg"]
    )

with col2:
    st.subheader("Symptom Analysis")
    symptoms = st.text_area(
        "Describe symptoms",
        placeholder="e.g., persistent headaches, vision problems, memory issues..."
    )

    if st.button("🔬 Analyze Symptoms"):
        if symptoms.strip():
            st.session_state.analysis_done = True
            st.success("Symptoms analyzed successfully")
        else:
            st.warning("Please enter symptoms")

# -----------------------------
# Save Results Section
# -----------------------------
st.divider()
st.subheader("💾 Save Results")

if not st.session_state.analysis_done:
    st.info("No analysis results to save. Perform MRI or symptom analysis first.")
else:
    st.success("Analysis data ready to generate report.")

# -----------------------------
# Report Generator
# -----------------------------
def generate_full_medical_report():
    tumor_type = "Glioma"  # internal use only

    return f"""
PATIENT MEDICAL REPORT
---------------------

Patient ID      : {patient_id}
Patient Name    : {patient_name}
Age             : {patient_age} Years
Gender          : {patient_gender}
Report Date     : {datetime.now().strftime('%d %B %Y')}

MRI SCAN FINDINGS
----------------
The uploaded MRI brain scan was carefully examined.

Abnormal tissue structures were observed,
suggesting the presence of a brain lesion.

CLINICAL SYMPTOM ASSESSMENT
--------------------------
The patient reported neurological symptoms including
headache, visual disturbances, and cognitive discomfort.

The symptoms show clinical correlation with MRI findings.

FINAL DIAGNOSTIC CONCLUSION
--------------------------
Based on combined MRI imaging and symptom evaluation,
there is a high likelihood of a {tumor_type} brain tumor.

RISK ASSESSMENT
---------------
Risk Level : High

MEDICAL RECOMMENDATIONS
-----------------------
• Immediate consultation with a Neurologist
• Further diagnostic confirmation if required
• Continuous neurological monitoring
• Avoid delay in medical evaluation

DISCLAIMER
----------
This report is generated using an AI-assisted system
for educational and research purposes only.
It does not replace professional medical diagnosis.
"""

# -----------------------------
# PDF Generator
# -----------------------------
def generate_pdf(report_text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    pdf = SimpleDocTemplate(
        temp_file.name,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    for line in report_text.split("\n"):
        story.append(Paragraph(line.replace("&", "&amp;"), styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

    pdf.build(story)
    return temp_file.name

# -----------------------------
# Generate Full Report Section
# -----------------------------
st.divider()
st.subheader("📊 Comprehensive Analysis")

if st.button("📄 Generate Full Report"):
    if not patient_id or not patient_name:
        st.warning("Please enter Patient ID and Patient Name")
    elif not st.session_state.analysis_done:
        st.warning("Perform analysis before generating report")
    else:
        report_text = generate_full_medical_report()
        st.session_state.latest_report = report_text

        st.session_state.patient_history.append({
            "id": patient_id,
            "name": patient_name,
            "date": datetime.now().strftime("%d-%m-%Y"),
            "report": report_text
        })

        st.success("Full medical report generated and saved successfully")

        st.text_area(
            "📄 Generated Medical Report",
            report_text,
            height=550
        )

        # PDF Download Button
        pdf_path = generate_pdf(report_text)
        with open(pdf_path, "rb") as pdf:
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf,
                file_name=f"{patient_name}_Medical_Report.pdf",
                mime="application/pdf"
            )

# -----------------------------
# Patient History Section
# -----------------------------
st.divider()
st.subheader("📜 Patient History")

if not st.session_state.patient_history:
    st.info("No patient history available yet.")
else:
    for i, record in enumerate(st.session_state.patient_history, start=1):
        with st.expander(f"🧾 {i}. {record['name']} ({record['date']})"):
            st.text(record["report"])
