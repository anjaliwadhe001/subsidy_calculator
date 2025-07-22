import pandas as pd
import os
import traceback
import subprocess

def generate_report_up_msme(user_data, result, zone):
    
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    safe_name = user_data.get("Name", "user").replace(" ", "_")
    filename = f"{safe_name}_Subsidy_Report.pdf"
    tex_filename = f"{safe_name}_Subsidy_Report.tex"

    tex_path = os.path.join(output_dir, tex_filename)
    pdf_path = os.path.join(output_dir, filename)

    capital_subsidy_rate = result.get('capital_subsidy_rate', '')
    if capital_subsidy_rate:
        capital_subsidy_rate = f"{capital_subsidy_rate} \\%"
    tex_content = f"""
\\documentclass[12pt]{{article}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{enumitem}}

\\begin{{document}}

\\begin{{center}}
\\Huge\\textbf{{Subsidy4India, a venture of SCPL}}\\\\[0.5em]
\\large 305, Regent Chambers, Nariman Point, Mumbai 400021 (INDIA)\\\\
Offices in New Delhi \\& New York\\
\\end{{center}}

\\textbf{{Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}}}

\\vspace{{1em}}
\\begin{{itemize}}
  \item {user_data['Organization Name']} \\
  \item {user_data['District']}, {user_data['State']} \\
\\end{{itemize}}
\\textbf{{Attn.:}} {user_data['Name']}

\\vspace{{1em}}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {user_data['District']}, {user_data['State']} and sharing the evaluation report for your perusal which is located in Zone \\textbf{{{zone}}}.

\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Name of Scheme:}} Industrial Investment & Employment Promotion Policy 2022
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega / Super mega / Ultra Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Subsidies apply only to investments made during the policy period (2022–2027)
\\end{{itemize}}

\\section*{{Subsidy Breakdown}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Capital investment subsidy (One-time):}} You can avail the capital subsidy only once after your unit starts commercial production, by applying online within three months. 
  According to Uttar Pradesh Industrial Investment & Employment Promotion Policy 2022 for MSMEs, For your enterprise size \\textbf{{{{{capital_subsidy_rate}}}}} Capital investment subsidy is available.

  \\item \\textbf{{Stamp duty exemption: }} For your zone \\textbf{{{zone}}}, 50\\% Stamp duty exemption is available. For Women-led enterprises 100\\% Stamp duty exemption is available statewide.

  \\item \\textbf{{Interest subsidy (applicable only when a term loan is availed for the project):}} Interest Subsidy is available 50\\% for all \\textbf{{micro}} enterprises only and 60\\% for SC/ST & Women entrepreneurs across all the zones.

  \\item \\textbf{{SGST reimbursement:}}  \\\\
  Under the Uttar Pradesh Micro, Small and Medium Enterprises (MSME) Promotion Policy 2022, SGST reimbursement is \\textbf{{not available.}}\\\\
  \\end{{itemize}}

\\section*{{Costing Table}}
\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']}  & One-time  &  Post production \\
\\hline
Stamp Duty Subsidy  & Rs. {result['stamp_duty_exemption']} & One time & Can be availed during purchase \\
\\hline
Interest subsidy & Rs. {result['interest_subsidy']} & Equally disbursed over 5 years & Post production \\
\\hline
\\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {result['total_subsidy']}.}}

\\section*{{I. Employment-Linked Incentives}}

\\textbf{{1. EPF Reimbursement}}\\
\\begin{{itemize}}[leftmargin=1.5em]
\\item Rate:
  \\begin{{itemize}}[leftmargin=1.5em]
    \\item Industrial Policy: 50\\% of employer’s contribution for 5 years.
    \\item MSME Policy: 100\\% of employer’s contribution for 5 years.
  \\end{{itemize}}
\\item Eligibility: All industrial units generating formal employment.
\\item Documentation: Proof of EPF registration and monthly contributions.
\\end{{itemize}}

\\textbf{{2. Employment Generation Incentive}}\\
\\begin{{itemize}}[leftmargin=1.5em]
\\item Rate:
  \\begin{{itemize}}[leftmargin=1.5em]
    \\item Large: Rs. 10,000/employee/year
    \\item Mega: Rs. 15,000/employee/year
    \\item Super-Mega: Rs. 20,000/employee/year
    \\item Ultra-Mega: Rs. 25,000/employee/year
  \\end{{itemize}}
\\item Boosters: +10\\% for hiring women/SC/ST workers.
\\item Conditions: Minimum employment thresholds (e.g., 200 for Large).
\\end{{itemize}}

\\section*{{II. Sector-Specific Subsidies}}
\\textbf{{1. Food Processing Units}}\\
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Mandi Fee Exemption: 100\\% exemption for 5 years.
  \\item Infrastructure Support: Subsidies for cold chains, packaging units.
\\end{{itemize}}

\\textbf{{2. Bio-Energy Enterprises}}\\
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Electricity Duty Exemption: 100\\% for 10 years.
  \\item Capital Subsidy:
    \\begin{{itemize}}[leftmargin=1.5em]
      \\item Compressed Bio-gas: Rs. 75 lakh/ton (max Rs. 20 crore).
      \\item Bio-coal: Rs. 75,000/ton (max Rs. 20 crore)
    \\end{{itemize}}
\\end{{itemize}}

\\section*{{III. Environmental & Sustainability Incentives}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Common Effluent Treatment Plant (CETP): 50\\% of project cost (capped at Rs. 10 crore).
  \\item Zero Liquid Discharge (ZLD): 50\\% of project cost (max Rs.75 lakh).
  \\item Green Initiatives:
    \\begin{{itemize}}[leftmargin=1.5em]
      \\item Audits: 75\\% reimbursement (max Rs. 50,000).
      \\item Equipment: 50\\% reimbursement for eco-friendly tech (max Rs. 20 lakh)
    \\end{{itemize}}
\\end{{itemize}}

\\section*{{Estimated Date of Receipt}}
There will be a sanction provided for each of the subsidy application made which is sanctioned in up to 90 days and then disbursed as per funds availability with the Govt. Department and ranges from 
3 months to 6 months from the date of sanction of the subsidy application. \\\\
\\\\
In the case of SGST reimbursement, the company needs to file for the same every year post filing of annual GST return (i.e. GSTR9), after which the SGST reimbursement is made ranging from 3 to 6 months 
from the date of filing the SGST reimbursement application. \\\\

\\section*{{How will SCPL ensure the subsidy gets into your bank account?}}
  \\begin{{itemize}}[leftmargin=1.5em]
    \\item SCPL will work with the client to ensure that the last rupee of subsidy is received in your bank account and the contract is valid till we achieve the same.
    \\item If there is a delay in receipt of the subsidy amount due to operational reasons or budget allocation delay with the respective Govt. Department, SCPL will keep the client informed at every step.
  \\end{{itemize}}

\\section*{{Value Added Services}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Preparation of Detailed Project Report (DPR)
  \\item Market Research to plan your Go To Market Strategy
  \\item DSIR (R\\&D certification) project for accessing R\\&D funding including grants from Govt. agencies
  \\item Intellectual Property protection by filing patent, design registration, trademark and copyright in India and global jurisdictions
\\end{{itemize}}

\\section*{{Not sure?}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Conduct a referral check by asking to get in touch with our happy customers
\\end{{itemize}}

\\section*{{Disclosure}}
\\begin{{itemize}}[leftmargin=1.5em]
    \\item SCPL (parent company of Subsidy4India) Team has calculated the subsidy based on details provided by the client and the same can vary depending 
    on the capital investment made by the client, exact location of the land where the manufacturing unit is being set up, documents provided for registering 
    the subsidy application, and any follow up documents required by the Central or State Government authorities. SCPL will not be liable for any reduction in 
    subsidy amount applicable to the client including the client being determined as non-eligible to avail the subsidy due to lack of documentation, change of policy, 
    or non-cooperation by the client. \\\\
\\end{{itemize}}

\\end{{document}}
"""

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print("Running pdflatex on:", tex_path)

    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print("===== PDF GENERATION FAILED =====")
            print("STDOUT:\n", result.stdout)
            print("STDERR:\n", result.stderr)
            print("PDFLaTeX returned non-zero code. Checking if PDF was generated anyway...")
            if not os.path.exists(pdf_path):
                raise Exception("PDF generation failed. LaTeX error logged to console.")
            else:
                print("PDF was generated despite warnings.")


    except FileNotFoundError:
        raise Exception("pdflatex command not found. Is LaTeX installed in your container?")

    except Exception as e:
        print("Unexpected error while generating PDF:", str(e))
        traceback.print_exc()
        raise

    return pdf_path
