from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime
import os


def generate_report_pdf(user_data, result, zone, zone_info):
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    safe_name = user_data.get("Name", "user").replace(" ", "_")
    filename = f"{safe_name}_Subsidy_Report.pdf"
    pdf_path = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []

    # Header
    story.append(Paragraph("Subsidy4India, a venture of SCPL", styles["Title"]))
    story.append(Paragraph("305, Regent Chambers, Nariman Point, Mumbai 400021 (INDIA)<br/>Offices in New Delhi & New York", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Date and basic details
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Organization Name:</b> {user_data['Organization Name']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Location:</b> {user_data['Subdistrict']}, {user_data['District']}, {user_data['State']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Attn.:</b> {user_data['Name']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Overview
    story.append(Paragraph("Overview", styles["Heading2"]))
    story.append(Paragraph(
        f"Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {user_data['District']}, {user_data['Subdistrict']} & {user_data['State']} located in Zone <b>{zone}</b>.",
        styles["Normal"]
    ))
    for item in [
        "Name of Scheme: Haryana Enterprises & Employment Policy 2020",
        "Base of subsidy: MSME / Large / Mega entity",
        "Estimated subsidy value: Each subsidy detailed below.",
        "Start of production: Within the policy period."
    ]:
        story.append(Paragraph(f"• {item}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Breakdown
    sgst_initial = zone_info["SGST Initial (%)"].item()
    sgst_extended = zone_info["SGST Extended (%)"].item()
    sgst_years = zone_info["SGST Initial Years"].item() + zone_info["SGST Extended Years"].item()

    story.append(Paragraph("Subsidy Breakdown", styles["Heading2"]))
    breakdown_items = [
        "Capital investment subsidy (One-time): Apply within 3 months after production.",
        "Stamp Duty exemption: During purchase of industrial land.",
        "Interest subsidy: Zone A & B get 5% for 5 years, Zone C & D get 6% for 7 years.",
        f"SGST reimbursement: Total {sgst_initial + sgst_extended:.2f}% on cash ledger. Rs. {result['sgst_reimbursement']} over {sgst_years} years.",
        "Disbursement: 90-day approval, 3–6 months fund release."
    ]
    for item in breakdown_items:
        story.append(Paragraph(f"• {item}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Table
    story.append(Paragraph("Costing Table", styles["Heading2"]))
    table_data = [
        ["Subsidy head", "Total subsidy", "No. of years", "Assumption"],
        ["Capital Investment", f"Rs. {result['capital_investment_subsidy']}", "One-time", "Post production"],
        ["Stamp Duty", f"Rs. {result['stamp_duty_exemption']}", "One-time", "Land purchase"],
        ["Interest subsidy", f"Rs. {result['interest_subsidy']}", f"{zone_info['Interest Years'].item()} years", "Post production"],
        ["SGST reimbursement", f"Rs. {result['sgst_reimbursement']}", f"{sgst_years} years", "Cash ledger"]
    ]
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table)
    story.append(Paragraph(f"<b>Total estimated subsidy: Rs. {result['total_subsidy']}</b>", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Additional sections
    sections = {
        "How will SCPL ensure the subsidy gets into your bank account?": [
            "We work closely to ensure full subsidy disbursal.",
            "Transparent updates on delays or fund issues."
        ],
        "Value Added Services": [
            "DPR preparation", "Market research", "DSIR projects", "IP protection (patent, trademark)"
        ],
        "Not sure?": [
            "You may speak to our clients for feedback."
        ],
        "Disclosure": [
            "Subsidy based on info provided by client.",
            "SCPL not liable for delays or denial due to documentation/policy."
        ]
    }
    for heading, bullets in sections.items():
        story.append(Paragraph(heading, styles["Heading2"]))
        for line in bullets:
            story.append(Paragraph(f"• {line}", styles["Normal"]))
        story.append(Spacer(1, 12))

    doc.build(story)
    return pdf_path
