import pandas as pd
import subprocess
import os

def generate_report_tamilnadu(user_data, result, zone):
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

    interest_eligibility_years = result.get('interest_eligibility_years', '')
    if interest_eligibility_years:
        interest_eligibility_years = f"{interest_eligibility_years} years"

    sgst_eligibility_years = result.get('sgst_eligibility_years', '')
    if sgst_eligibility_years:
        sgst_eligibility_years = f"{sgst_eligibility_years} years"

    tex_content = f"""
\\documentclass[11pt]{{article}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{enumitem}}

\\begin{{document}}

\\begin{{center}}
\\Huge\\textbf{{Subsidy4India, a venture of SCPL}}\\\\[0.5em]
\\large 305, Regent Chambers, Nariman Point, Mumbai 400021 (INDIA)\\\\
Offices in New Delhi \\& New York\\\\
\\end{{center}}

\\textbf{{Date: {pd.Timestamp.now().strftime('%d-%m-%Y')}}}

\\vspace{{1em}}
\\begin{{itemize}}
\\item {user_data['Organization Name']} \\\\
\\item {user_data['District']}, {user_data['State']} \\\\
\\textbf{{Attn.:}} {user_data['Name']}
\\end{{itemize}}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {user_data['District']}, {user_data['State']} and sharing the evaluation report for your perusal which is located in Zone \\textbf{{{zone}}}.
\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Name of Scheme:}} Tamil Nadu Industrial Policy 2021
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Within the policy period.
\\end{{itemize}}

\\section*{{Subsidy Breakdown}} 
\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{(a) Capital investment subsidy (One-time):}} According to Industrial Policy 2025, you can avail capital subsidy only once post production which is disbursed over eligible years.
  \\item \\textbf{{(b) SGST reimbursement:}} SGST reimbursement calculation will be strictly available on SGST paid from cash ledger as per GSTR9 filed annually. Eligible enterprises will get SGST reimbursement for 15 years.
  \\item \\textbf{{(c) Interest Subsidy (applicable only when a term loan is availed for the project):}} Interest subsidy is available for 5 years for MSMEs and 6 years for large/mega projects.
\\end{{itemize}}

\\section*{{Subsidy Snapshot}}
\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & Disbursed over 7 years & One-time post production \\\\
\\hline
SGST reimbursement & Rs. {result['sgst_reimbursement']} & {sgst_eligibility_years} & Not Available for MSMEs across all zones and Large in Zone A  \\\\
\\hline
Stamp Duty & Rs. {result['stamp_duty_subsidy']} & One Time & Sub-Large projects are generally not eligible for this incentive \\\\
\\hline
Interest Subsidy & Rs. {result['interest_subsidy']} & {interest_eligibility_years} & Quarterly reimbursements to financial institutions \\\\
\\hline
\\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {result['total_subsidy']}.}}  

\\section*{{Other Incentives}}
\\begin{{enumerate}}
  \\item \\textbf{{Training Subsidy}} 
    \\begin{{itemize}}
      \\item Rs. 4,000 per worker per month for 6 months (general category).
      \\item Rs. 6,000 per worker per month for 6 months (for women, transgender, SC/ST, and persons with benchmark disabilities).
    \\end{{itemize}}

  \\item \\textbf{{Electricity Tax Incentive}} 
    \\begin{{itemize}}
      \\item 100\\% exemption from electricity tax for 5 years.
      \\item Applicable to power purchased from TANGEDCO or captive sources.
    \\end{{itemize}}

  \\item \\textbf{{Green Industry Incentive}} 
    \\begin{{itemize}}
      \\item 25\\% subsidy on eco-friendly infrastructure (up to Rs. 1 crore).
      \\item Covers energy efficiency, water conservation, pollution control.
    \\end{{itemize}}

  \\item \\textbf{{Special Incentives for R\\&D Projects}} 
    \\begin{{itemize}}
      \\item Eligibility: Rs. 50 crore investment + 50 employees.
      \\item Benefits: 50\\% land cost, training subsidy, standard incentives.
    \\end{{itemize}}
\\end{{enumerate}}

\\section*{{Estimated Date of Receipt}}
Sanction typically within 90 days. Disbursement within 3–6 months post-sanction. SGST reimbursement is annual, post GSTR9 filing, and processed within 3–6 months.

\\section*{{SCPL Commitment}}
\\begin{{itemize}}
  \\item SCPL ensures subsidy reaches your bank account.
  \\item Regular updates in case of delays from government departments.
\\end{{itemize}}

\\section*{{Value Added Services}} 
\\begin{{itemize}}
  \\item Detailed Project Report (DPR)
  \\item Market research for Go-To-Market strategy
  \\item DSIR registration for R\\&D funding
  \\item Intellectual property services (patents, trademarks, etc.)
\\end{{itemize}}

\\section*{{Not Sure?}} 
Contact our satisfied clients for referrals.

\\section*{{Disclosure}}
SCPL (parent company of Subsidy4India) Team has calculated the subsidy based on details provided by the client and the same can vary depending on the capital investment made by the client, exact location of the land where the manufacturing unit is being set up, documents provided for registering the subsidy application, and any follow up documents required by the Central or State Government authorities. SCPL will not be liable for any reduction in subsidy amount applicable to the client including the client being determined as non-eligible to avail the subsidy due to lack of documentation, change of policy, or non-cooperation by the client.

\\end{{document}}
"""

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    compile_result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if compile_result.returncode != 0:
        log_file = os.path.join(output_dir, "pdflatex_error.log")
        with open(log_file, "w") as f:
            f.write("STDOUT:\n" + compile_result.stdout + "\n\nSTDERR:\n" + compile_result.stderr)
        raise Exception(f"PDF generation failed. Details saved to {log_file}")

    return pdf_path
