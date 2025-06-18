
from fpdf import FPDF
import pandas as pd
from tabulate import tabulate

# Dummy calculation functions (replace with actual logic)
def calculate_stamp_duty(): return 100000
def calculate_interest_subsidy(): return 700000
def calculate_electricity_waiver(): return 300000
def calculate_sgst_reimbursement(): return 500000

def generate_pdf(user_data, result, zone):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Subsidy Calculation Report", ln=True, align='C')

    # Company Info
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, txt="Subsidy4India, a venture of SCPL", ln=True)
    pdf.cell(0, 10, txt="305, Regent Chambers,", ln=True)
    pdf.cell(0, 10, txt="Nariman Point, Mumbai 400021 (INDIA)", ln=True)
    pdf.cell(0, 10, txt="Offices in New Delhi & New York", ln=True)
    pdf.cell(0, 10, txt=f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(0, 10, txt="", ln=True)

    # Recipient Info
    pdf.cell(0, 10, txt=f"Attn.: Mr. Ram Mehar (CFO)", ln=True)
    pdf.cell(0, 10, txt=f"Sub District: {user_data['Subdistrict']}, District: {user_data['District']}, State: {user_data['State']}", ln=True)
    pdf.cell(0, 10, txt="", ln=True)

    # Overview
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Overview", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, txt=(
        f"Subsidy4India has identified various subsidies available for your {user_data['Organization Name']} "
        f"for your manufacturing unit in {user_data['Subdistrict']}, {user_data['District']}, {user_data['State']} "
        f"and sharing the evaluation report for your perusal which is located in Zone {zone}."
    ))

    points = [
        "Name of Scheme: (to be inserted based on the State where unit is being setup)",
        "Base of subsidy: Subsidy schemes applicable to your company as a MSME / Large / Mega entity",
        "Estimated subsidy value: Each subsidy has been mentioned in detail in the proposal such as stamp duty reimbursement, interest subsidy, electricity duty exemption, SGST reimbursement etc.",
        "Date of start of commercial production: Within the policy period but as soon as commercial production has commenced else the benefits will be curtailed"
    ]
    for point in points:
        pdf.multi_cell(0, 10, txt=f"- {point}")
    pdf.cell(0, 10, txt="", ln=True)

    # Subsidy Breakdown
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Subsidy Breakdown:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, txt=(
        "The subsidy period for each subsidy varies and the most important ones are mentioned below:\n"
        f"- Capital investment subsidy (One-time): {result['capital_investment_subsidy']} \n"
        f"- Stamp Duty exemption / reimbursement: Rs.{result['stamp_duty_exemption']} \n"
        f"- Interest subsidy (if term loan is availed): Rs.{result['interest_subsidy']} \n"
        f"- Electricity Duty exemption: ___% exemption for {user_data.get('Loan Tenure', 'N/A')} for Zone {zone}\n"
        f"- SGST reimbursement: Rs.{result['sgst_reimbursement']}"
    ))
    pdf.cell(0, 10, txt="", ln=True)

    # Subsidy Table
    data = [
        {
            "Subsidy head": "Stamp Duty reimbursement",
            "Total subsidy amount (estimated)": f"Rs{calculate_stamp_duty():,}",
            "No. of times or years": "1",
            "Assumption": "Once production commences unless prior approval is taken"
        },
        {
            "Subsidy head": "Interest subsidy",
            "Total subsidy amount (estimated)": f"Rs{calculate_interest_subsidy():,}",
            "No. of times or years": "7 (from system)",
            "Assumption": "Available after production starts"
        },
        {
            "Subsidy head": "Electricity Duty waiver",
            "Total subsidy amount (estimated)": f"Rs{calculate_electricity_waiver():,}",
            "No. of times or years": "7 (from system)",
            "Assumption": "Available after production starts"
        },
        {
            "Subsidy head": "SGST reimbursement",
            "Total subsidy amount (estimated)": f"Rs{calculate_sgst_reimbursement():,}",
            "No. of times or years": "7 (from system)",
            "Assumption": "Depends on SGST paid from cash ledger yearly"
        }
    ]
    df = pd.DataFrame(data)
    table_text = tabulate(df, headers='keys', tablefmt='grid')
    pdf.set_font("Courier", size=9)
    pdf.multi_cell(0, 5, txt=table_text)
    pdf.cell(0, 10, txt="", ln=True)

    # SGST Note
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, txt=(
        "SGST reimbursement: Kindly note that you can avail SGST reimbursement for capital investment made "
        "to the tune of INR __ crore and the same will be __% of the investment made which comes to INR __ crore "
        "payable over __ years."
    ))
    pdf.cell(0, 10, txt="", ln=True)

    # SCPL Involvement
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="How will SCPL ensure the subsidy gets into your bank account?", ln=True)
    pdf.set_font("Arial", "", 11)
    items = [
        "SCPL will work with the client to ensure that the last rupee of subsidy is received in your bank account and the contract is valid till we achieve the same.",
        "If there is a delay due to operational or budget reasons, SCPL will keep the client informed at every step."
    ]
    for item in items:
        pdf.multi_cell(0, 10, txt=f"- {item}")
    pdf.cell(0, 10, txt="", ln=True)

    # Value Added Services
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Value Added Services:", ln=True)
    pdf.set_font("Arial", "", 11)
    services = [
        "Preparation of Detailed Project Report (DPR)",
        "Market Research to plan your Go To Market Strategy",
        "DSIR (R&D certification) project for accessing R&D funding",
        "IP protection via patent, design, trademark, and copyright filings"
    ]
    for service in services:
        pdf.multi_cell(0, 10, txt=f"- {service}")
    pdf.cell(0, 10, txt="", ln=True)

    # Disclosure
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Disclosure by SCPL:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, txt=(
        "SCPL (parent company of Subsidy4India) has calculated the subsidy based on client-provided details. "
        "Values may vary depending on capital investment, exact location, and documentation. SCPL will not be liable "
        "for changes in eligibility or amounts due to policy changes or lack of cooperation/documentation."
    ))

    file_path = "Subsidy_Calculation_Report.pdf"
    pdf.output(file_path)
    return file_path
