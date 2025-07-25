import pandas as pd
import subprocess
import os

def generate_report_karnataka(user_data, result, zone):
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    # A safe filename based on user's information
    safe_name = user_data.get("Organisation Name", "user").replace(" ", "_")
    safe_name1 = user_data.get("State", "user").replace(" ", "_")
    safe_name2 = user_data.get("Enterprise Size", "user").replace(" ", "_")
    filename = f"{safe_name}_{safe_name1}_{safe_name2}_Subsidy_Report.pdf"
    tex_filename = f"{safe_name}_{safe_name1}_{safe_name2}_Subsidy_Report.tex"

    tex_path = os.path.join(output_dir, tex_filename)
    pdf_path = os.path.join(output_dir, filename)

    tex_content = f"""
\\documentclass[11pt]{{article}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{enumitem}}
\\usepackage{{textcomp}}

\\begin{{document}}

\\begin{{center}}
\\Huge\\textbf{{Subsidy4India, a venture of SCPL}}\\\\[0.5em]
\\large 305, Regent Chambers, Nariman Point, Mumbai 400021 (INDIA)\\\\
Offices in New Delhi \\& New York\\\\
\\end{{center}}

\\textbf{{Date: {pd.Timestamp.now().strftime('%d-%m-%Y')}}}

\\vspace{{1em}}

{user_data['Organization Name']} \\\\
{user_data['Subdistrict']}, {user_data['District']}, {user_data['State']} \\\\
\\textbf{{Attn.:}} {user_data['Name']}

\\vspace{{1em}}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {user_data['District']}, {user_data['Subdistrict']} \\& {user_data['State']}, located in Zone \\textbf{{{zone}}}.

\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Name of Scheme:}} Karnataka Industrial Policy 2025--30
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega entity
  \\item \\textbf{{Estimated subsidy value:}} As detailed in the subsidy breakdown below
  \\item \\textbf{{Production Start:}} Subsidies are applicable for the investments made within policy period (2025--2030).
\\end{{itemize}}

\\section*{{Subsidy Breakdown}}
\\begin{{itemize}}[leftmargin=1.5em]
    \\textbf{{1. Asset Creation Incentives (You can choose only one of the following)}}
    \\textbf{{(a) Capital investment subsidy (One-time):}} According to MSME Policy 2024, Plastic alternative, Agricultural and Food processing industries will get subsidy 50\\% of their capital investment with the cap of Rs. 40 lakhs and Rs. 1.5 Crore respectively.
    \\textbf{{(b) SGST reimbursement:}} Kindly note that you can avail SGST reimbursement on the capital iinvestment for 7 years. SGST reimbursement calculation (will be strictly available on SGST paid from cash ledger as per GSTR9 filed annually).
\\end{{itemize}}

\\begin{{longtable}}{{|p{{4.5cm}}|p{{4.5cm}}|p{{2.5cm}}|p{{4.5cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{Years}} & \\textbf{{Remarks}} \\\\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & 7 years & One-time disbursed annually \\\\
\\hline
SGST Reimbursement & Rs. {result['sgst_reimbursement']} & 7 years & Post production, via GSTR9 \\\\
\\hline
Interest Subsidy & Rs. {result['interest_subsidy']} & 5 years & Only for loans in Zones A \\& B \\\\
\\hline
Stamp Duty Subsidy & Rs. {result['stamp_duty_subsidy']} & One-time & Based on zone classification \\\\
\\hline
\\end{{longtable}}

\\begin{{itemize}}[leftmargin=1.5em]
    \\textbf{{2. Other incentives:}}
    \\textbf{{(a) Interest Subsidy (applicable only when a term loan is availed for the project):}} In Karnataka, interest subsidy is provided to MSMEs in Zone A and Zone B only to promote technology adoption and reduce the cost of finance for new and expanding enterprises.
    \\textbf{{(b) Stamp Duty Subsidy:}} The Karnataka Industrial Policy 2025--30 provides differentiated stamp duty exemptions based on the industrial zone classification.
\\end{{itemize}}

\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
Interest subsidy & Rs. {result['interest_subsidy']} & 5 years & Post production \\\\
\\hline
Stamp Duty Subsidy & Rs. {result['stamp_duty_subsidy']} & One Time & Post production \\\\
\\hline
\\end{{longtable}}

\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Total Estimated Subsidy: Rs. {result['total_subsidy']}}}
\\end{{itemize}}

\\section*{{Other Key Subsidies \\& Incentives}}
\\begin{{itemize}}[leftmargin=1.5em]
    \\textbf{{1. Reimbursement of Land Conversion Fee}}
        \\begin{{itemize}}
            \\item Zone 1: 100\\% reimbursement after commencement of commercial production
            \\item Zone 2: 100\\% reimbursement after commencement of commercial production
            \\item Zone 3: NIL
        \\end{{itemize}}

  \\item Eligible Entities: Proprietorships, partnerships, companies, LLPs, co-operatives, etc.

    \\textbf{{2. Employment Generation Booster}}
    \\begin{{itemize}}
        \\item Incentive for Extra Employment:
            \\begin{{itemize}}
              \\item 3x--4x minimum required employment: 7.5\\% booster on eligible incentive amount
              \\item 4x--5x: 10\\% booster
              \\item 5x: 15\\% booster
            \\end{{itemize}}
    \\item Applicability: All zones, for projects exceeding minimum employment thresholds
  \\end{{itemize}}

    \\textbf{{3. Women Workforce Participation Incentive}}
    \\begin{{itemize}}
        \\item For Large, Mega, and Ultra Mega Enterprises:
        \\begin{{itemize}}
          \\item $\\geq$ 50\\% women employees: 7.5\\% booster on eligible incentive amount
          \\item $\\geq$ 60\\% women: 10\\% booster
          \\item $\\geq$ 70\\% women: 15\\% booster
        \\end{{itemize}}
        \\item Objective: Promote gender diversity in industrial workforce
  \\end{{itemize}}
\\end{{itemize}}

\\section*{{Estimated Date of Receipt}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item There will be a sanction provided for each of the subsidy applications made, which is sanctioned within 90 days and then disbursed as per funds availability with the Govt. Department and ranges from 3 months to 6 months from the date of sanction of the subsidy application.
  \\item In the case of SGST reimbursement, the company needs to file for the same every year post filing of annual GST return i.e. GSTR9, after which the SGST reimbursement is made ranging from 3 months to 6 months from the date of filing SGST reimbursement application.
\\end{{itemize}}

\\section*{{How SCPL Supports You}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item SCPL will work with the client to ensure that the last rupee of subsidy is received in your bank account and the contract is valid till we achieve the same.
  \\item If there is a delay in receipt of the subsidy amount due to operational reasons or budget allocation delay with the respective Govt. Department, SCPL will keep the client informed at every step.
\\end{{itemize}}

\\section*{{Value-Added Services}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Preparation of Detailed Project Report (DPR)
  \\item Market Research to plan your Go To Market Strategy
  \\item DSIR (R\\&D certification) project for accessing R\\&D funding including grants from Govt. agencies
  \\item Intellectual Property protection by filing patent, design registration, trademark and copyright in India and global jurisdictions
\\end{{itemize}}

\\section*{{Not sure}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Conduct a referral check by asking to get in touch with our happy customers
\\end{{itemize}}

\\section*{{Disclosure}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item SCPL (parent company of Subsidy4India) Team has calculated the subsidy based on details provided by the client and the same can vary depending on the capital investment made by the client, exact location of the land where the manufacturing unit is being setup, documents provided for registering the subsidy application and any follow-up documents required by the Central or State Government authorities. 
  SCPL will not be liable for any reduction in subsidy amount applicable to the client including the client being determined as non-eligible to avail the subsidy due to lack of documentation, change of policy and non-cooperation by client.
\\end{{itemize}}

\\end{{document}}
"""

    with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_content)

    result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    if result.returncode != 0:
        print("PDF generation failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise Exception("PDF generation error")

    return pdf_path
