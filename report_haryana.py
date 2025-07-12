import pandas as pd
import os

def generate_report_haryana(user_data, result, zone, zone_info):
    # Extract scalar values for calculation in the report
    sgst_initial_percent_report = zone_info["SGST Initial (%)"].item()
    sgst_extended_percent_report = zone_info["SGST Extended (%)"].item()
    sgst_initial_years_report = zone_info["SGST Initial Years"].item()
    sgst_extended_years_report = zone_info["SGST Extended Years"].item()

    tex_content = f"""
\\documentclass[12pt]{{article}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}

\\begin{{document}}

\\begin{{center}}
\\Huge\\textbf{{Subsidy4India, a venture of SCPL}}\\\\[0.5em]
\\large 305, Regent Chambers, Nariman Point, Mumbai 400021 (INDIA)\\\\
Offices in New Delhi \\& New York\\\\
\\end{{center}}

\\textbf{{Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}}}

\\vspace{{1em}}

\\textbf{{Organization Name:}} {user_data['Organization Name']} \\\\
\\textbf{{Location:}} {user_data['Subdistrict']}, {user_data['District']}, {user_data['State']} \\\\
\\textbf{{Attn.:}} {user_data['Name']}

\\vspace{{1em}}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {user_data['District']}, {user_data['Subdistrict']} \\& {user_data['State']} and sharing the evaluation report for your perusal which is located in Zone \\textbf{{{zone}}}.

\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Name of Scheme:}} Haryana Enterprises \\& Employment Policy 2020
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Within the policy period.
\\end{{itemize}}

\\section*{{Subsidy Breakdown}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Capital investment subsidy (One-time):}} You can avail the capital subsidy only once after your unit starts commercial production, by applying online within three months.
  \\item \\textbf{{Stamp Duty exemption / reimbursement:}} Available during purchase of industrial land for the project. Reimbursement would be available only if the same entity bills the client when production starts.
  \\item \\textbf{{Interest subsidy (if term loan availed):}} Zone A \\& B receive 5\\% interest subsidy for 5 years, Zone C \\& D receive 6\\% for 7 years.
  \\item \\textbf{{SGST reimbursement:}} Available on SGST paid via cash ledger. Rate is {((sgst_initial_percent_report / 100) + (sgst_extended_percent_report / 100)) * 100:.2f}\\% of investment, totalling Rs. {result['sgst_reimbursement']} over {sgst_initial_years_report + sgst_extended_years_report} years.
  \\item \\textbf{{Estimated receipt timeline:}} Each subsidy is sanctioned within ~90 days, disbursed within 3–6 months depending on fund availability. SGST reimbursement is annual post-GSTR-9 filing.
\\end{{itemize}}

\\section*{{Costing Table}}
\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & One-time & Post production \\\\
\\hline
Stamp Duty reimbursement & Rs. {result['stamp_duty_exemption']} & One-time & Available during purchase \\\\
\\hline
Interest subsidy & Rs. {result['interest_subsidy']} & Disbursed over {zone_info['Interest Years'].item()} years & Post production \\\\
\\hline
SGST reimbursement & Rs. {result['sgst_reimbursement']} & Disbursed over {sgst_initial_years_report + sgst_extended_years_report} years & Paid from cash ledger \\\\
\\hline
\\end{{longtable}}

\\textbf{{Total estimated subsidy available: Rs. {result['total_subsidy']}.}}

\\section*{{How will SCPL ensure the subsidy gets into your bank account?}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item SCPL will work with the client to ensure that the last rupee of subsidy is received.
  \\item In case of delays due to government processes or budget allocations, SCPL will maintain transparency and keep the client updated at each step.
\\end{{itemize}}

\\section*{{Value Added Services}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Preparation of Detailed Project Report (DPR)
  \\item Market Research to plan your Go-To-Market strategy
  \\item DSIR (R\\&D certification) project for accessing R\\&D funding including grants
  \\item Intellectual Property protection (patent, trademark, design registration)
\\end{{itemize}}

\\section*{{Not sure?}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item We encourage you to speak with our existing clients for feedback and assurance.
\\end{{itemize}}

\\section*{{Disclosure}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Subsidy values are based on client-provided details. Actual eligibility and amount depend on documentation, government decisions, and compliance.
  \\item SCPL shall not be held responsible if any subsidy is reduced, delayed, or denied due to documentation issues or policy changes.
\\end{{itemize}}

\\end{{document}}
"""

    with open("Subsidy_report_haryana.tex", "w", encoding="utf-8") as f:
        f.write(tex_content)

    # Compile to PDF
    os.system("pdflatex -interaction=nonstopmode Subsidy_report_haryana.tex")
    return "Subsidy_report_haryana.pdf"
