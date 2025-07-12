import pandas as pd
import os

def generate_report_up(user_data, result, zone):
    sgst_years_display = result.get('sgst_eligible_years', '')
    if sgst_years_display:
        sgst_years_display = f"{sgst_years_display} years"

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

\\item {user_data['Organization Name']} \\
\\item {user_data['District']}, {user_data['State']} \\\\
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
    According to Uttar Pradesh Industrial Investment & Employment Promotion Policy 2022 for MSMEs, Capital investment subsidy is applicable only for Small and Micro Enterprises.

    \\item \\textbf{{Stamp duty exemption: }} For your zone \\textbf{{{zone}}}, 50\\% Stamp duty exemption is available. For Women-led enterprises 100\\% Stamp duty exemption is available statewide.

    \\item \\textbf{{Interest subsidy (applicable only when a term loan is availed for the project):}} Interest Subsidy is available 50\\% only for all micro enterprises and 60\\% for SC/ST & Women entrepreneurs across all the zones.

    \\item \\textbf{{SGST reimbursement:}}  \\\\
    Under the Uttar Pradesh Micro, Small and Medium Enterprises (MSME) Promotion Policy 2022, \\textbf{{SGST reimbursement is not available.}} \\\\
    However, SGST reimbursement is a feature of the Uttar Pradesh Industrial Investment & Employment Promotion Policy 2022, which applies to large, mega, super-mega, and ultra-mega industrial units, not MSMEs. Under this policy, eligible units can choose Net SGST Reimbursement as one of the mutually exclusive options for incentives, with reimbursement of 100\\% of the net SGST amount deposited in the State’s account, subject to policy conditions.
\\end{{itemize}}

\\section*{{Costing Table}}
\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & One Time & Post production \\
\\hline
Stamp Duty Subsidy  & Rs. {result['stamp_duty_exemption']} & One Time & Can be availed during purchase \\
\\hline
SGST reimbursement & Rs. {result['sgst_reimbursement']} & Disbursed equally over {{{sgst_years_display}}} & Post production \\
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
There will be a sanction provided for each of the subsidy application made which is sanctioned in up to 90 days and then disbursed as per funds availability with the Govt. Department and ranges from 3 months to 6 months from the date of sanction of the subsidy application. In the case of SGST reimbursement, the company needs to file for the same every year post filing of annual GST return (i.e. GSTR9), after which the SGST reimbursement is made ranging from 3 to 6 months from the date of filing the SGST reimbursement application.

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
  \\item SCPL (parent company of Subsidy4India) Team has calculated the subsidy based on details provided by the client and the same can vary depending on the capital investment made by the client, exact location of the land where the manufacturing unit is being set up, documents provided for registering the subsidy application, and any follow up documents required by the Central or State Government authorities. SCPL will not be liable for any reduction in subsidy amount applicable to the client including the client being determined as non-eligible to avail the subsidy due to lack of documentation, change of policy, or non-cooperation by the client.
\\end{{itemize}}

\\end{{document}}
"""
    with open("Subsidy_report_up.tex", "w", encoding="utf-8") as f:
        f.write(tex_content)

    os.system("pdflatex -interaction=nonstopmode Subsidy_report_up.tex")
    return "Subsidy_report_up.pdf"
