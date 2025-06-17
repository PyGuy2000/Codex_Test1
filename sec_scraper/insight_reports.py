from fpdf import FPDF
import numpy as np
from search_module import results_2020, results_2024 # Assuming you have the documents loaded
from topic_modelling import topics_2020, topics_2024  # Assuming you have the topics loaded


# Compute ESG trend statistics
esg_changes = {
    'environmental': np.mean(results_2024['environmental']) - np.mean(results_2020['environmental']),
    'social': np.mean(results_2024['social']) - np.mean(results_2020['social']),
    'governance': np.mean(results_2024['governance']) - np.mean(results_2020['governance']),
    'overall': np.mean(results_2024['overall']) - np.mean(results_2020['overall'])
}

# Create PDF report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "Energy Sector ESG Trends Analysis: 2020 vs 2024", ln=True, align='C')
pdf.ln(10)

# Introduction
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, "This report analyzes ESG (Environmental, Social, and Governance) trends in the energy sector based on SEC filings from 2020 and 2024. The analysis examines keyword frequency, sentiment, and thematic shifts in corporate communications.")
pdf.ln(5)

# Key findings
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, "Key Findings", ln=True)
pdf.ln(5)

pdf.set_font("Arial", size=12)
findings = [
    f"Environmental themes: {'Increased' if esg_changes['environmental'] > 0 else 'Decreased'} by {abs(esg_changes['environmental']):.2f} mentions per 1000 words",
    f"Social themes: {'Increased' if esg_changes['social'] > 0 else 'Decreased'} by {abs(esg_changes['social']):.2f} mentions per 1000 words",
    f"Governance themes: {'Increased' if esg_changes['governance'] > 0 else 'Decreased'} by {abs(esg_changes['governance']):.2f} mentions per 1000 words",
    f"Overall ESG focus: {'Increased' if esg_changes['overall'] > 0 else 'Decreased'} by {abs(esg_changes['overall']):.2f} mentions per 1000 words"
]

for finding in findings:
    pdf.cell(10, 10, "•", ln=0)
    pdf.multi_cell(180, 10, finding)

# Include comparison chart
pdf.image("esg_comparison.png", x=10, y=None, w=180)
pdf.ln(5)

# Topic evolution
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, "Evolution of Key Themes", ln=True)
pdf.ln(5)

pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, "2020 Dominant Themes:")
for topic in topics_2020:
    pdf.cell(10, 10, "•", ln=0)
    pdf.multi_cell(180, 10, f"Theme {topic['topic_id']+1}: {', '.join(topic['top_words'][:5])}")
pdf.ln(5)

pdf.multi_cell(0, 10, "2024 Dominant Themes:")
for topic in topics_2024:
    pdf.cell(10, 10, "•", ln=0)
    pdf.multi_cell(180, 10, f"Theme {topic['topic_id']+1}: {', '.join(topic['top_words'][:5])}")
pdf.ln(5)

# Save the PDF
pdf.output("Energy_Sector_ESG_Trends_2020_vs_2024.pdf")
