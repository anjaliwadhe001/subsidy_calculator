from fpdf import FPDF
import pandas as pd

def generate_pdf(user_data, result, zone):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Subsidy Calculation Report", ln=True, align='C')

    # Add company information
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, txt="Subsidy4India, a venture of SCPL", ln=True)
    pdf.cell(0, 10, txt="305, Regent Chambers,", ln=True)
    pdf.cell(0, 10, txt="Nariman Point, Mumbai 400021 (INDIA)", ln=True)
    pdf.cell(0, 10, txt="Offices in New Delhi & New York", ln=True)
    pdf.cell(0, 10, txt=f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(0, 10, txt="", ln=True)  # Blank line

    # Add recipient information
    pdf.cell(0, 10, txt=f"Attn.: Mr. Ram Mehar (CFO)", ln=True)
    pdf.cell(0, 10, txt=f"Sub District: {user_data['Subdistrict']}, District: {user_data['District']}, State: {user_data['State']}", ln=True)
    pdf.cell(0, 10, txt="", ln=True)  # Blank line

    # Overview section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Overview", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, txt=(
        f"Subsidy4India has identified various subsidies available for your {user_data['Organization Name']} "
        f"for your manufacturing unit in {user_data['Subdistrict']}, {user_data['District']}, {user_data['State']} "
        f"and sharing the evaluation report for your perusal which is located in Zone {zone}."
    ))
    pdf.cell(0, 10, txt="", ln=True)  # Blank line

    # Subsidy details
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Name of Scheme:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, txt="(to be inserted based on the State where unit is being setup)", ln=True)
    pdf.cell(0, 10, txt="", ln=True)  # Blank line

    # Subsidy breakdown
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Subsidy Breakdown:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, txt=(
        "The subsidy period for each subsidy varies and the most important ones are mentioned below:\n"
        f"- Capital investment subsidy: One-time\n"
        f"- Stamp Duty exemption / reimbursement: {result['stamp_duty_exemption']} Rs.\n"
        f"- Interest subsidy (applicable only when a term loan is availed for the project): {result['interest_subsidy']} Rs.\n"
        f"- SGST reimbursement: {result['sgst_reimbursement']} Rs.\n"
    ))
    pdf.cell(0, 10, txt="", ln=True)  # Blank line

    # Costing in tabulated form
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Costing in Tabulated Form:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, txt="Subsidy Head\tTotal Subsidy Amount (Estimated)\tNo. of Times or Years\tAssumption", ln=True)
    pdf.cell(0, 10, txt=f"Stamp Duty reimbursement\t{result['stamp_duty_exemption']}\t1\tWill be availed once the production has commenced", ln=True)
    pdf.cell(0, 10, txt=f"Interest subsidy\t{result['interest_subsidy']}\t7\tWill be availed once the production has commenced", ln=True)
    pdf.cell(0, 10, txt=f"SGST reimbursement\t{result['sgst_reimbursement']}\t7\tSGST reimbursement is dependent on the SGST paid from cash ledger on yearly basis", ln=True)

    # Additional notes
    pdf.cell(0, 10, txt="", ln=True)  # Blank line
    pdf.cell(0, 10, txt="SGST reimbursement:", ln=True)
    pdf.multi_cell(0, 10, txt=(
        "Kindly note that you can avail SGST reimbursement for capital investment made to the tune of INR ___ crore "
        "and the same will be __% of the investment made which comes to INR ___ crore payable over __ years."
    ))

    # Closing remarks
    pdf.cell(0, 10, txt="", ln=True)  # Blank line
    pdf.cell(0, 10, txt="How will SCPL ensure the subsidy gets into your bank account?", ln=True)
    pdf.multi_cell(0, 10, txt=(
        "SCPL will work with the client to ensure that the last rupee of subsidy is received in your bank account "
        "and the contract is valid till we achieve the same."
    ))

    # Value Added Services
    pdf.cell(0, 10, txt="", ln=True)  # Blank line
    pdf.cell(0, 10, txt="Value Added Services:", ln=True)
    pdf.multi_cell(0, 10, txt=(
        "- Preparation of Detailed Project Report (DPR)\n"
        "- Market Research to plan your Go To Market Strategy\n"
        "- DSIR (R&D certification) project for accessing R&D funding including grants from Govt. agencies\n"
        "- Intellectual Property protection by filing patent, design registration, trademark and copyright in India and global jurisdictions"
    ))

    # Disclosure by SCPL
    pdf.cell(0, 10, txt="", ln=True)  # Blank line
    pdf.cell(0, 10, txt="Disclosure by SCPL:", ln=True)
    pdf.multi_cell(0, 10, txt=(
        "SCPL (parent company of Subsidy4India) Team has calculated the subsidy based on details provided by the client "
        "and the same can vary depending on the capital investment made by the client."
    ))

    file_path = "Subsidy_Calculation_Report.pdf"
    pdf.output(file_path)
    return file_path

