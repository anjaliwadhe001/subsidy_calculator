import pandas as pd
import subprocess
import os

def generate_report_punjab(user_data, result):
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    safe_name = user_data.get("Name", "user").replace(" ", "_")
    filename = f"{safe_name}_Subsidy_Report.pdf"
    tex_filename = f"{safe_name}_Subsidy_Report.tex"

    tex_path = os.path.join(output_dir, tex_filename)
    pdf_path = os.path.join(output_dir, filename)

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
Offices in New Delhi \\& New York
\\end{{center}}

\\textbf{{Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}}}

\\vspace{{1em}}

\\begin{{itemize}}[leftmargin=1.5em]
  \\item {user_data['Organization Name']}
  \\item {user_data['District']}, {user_data['State']}
  \\item \\textbf{{Attn.:}} {user_data['Name']}
\\end{{itemize}}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {user_data['District']}, {user_data['State']}.

\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Name of Scheme:}} Punjab Industrial and Business Development Policy 2022
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Within the policy period.
\\end{{itemize}}

\\section*{{Subsidy Breakdown}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Capital investment subsidy (One-time):}} Based on Fixed Capital Investment and scheme parameters.
  \\item \\textbf{{Stamp Duty exemption / reimbursement:}} 100\\% exemption/reimbursement on eligible transactions.
  \\item \\textbf{{Interest subsidy:}} Applicable based on enterprise type and location.
  \\item \\textbf{{SGST reimbursement:}} Calculated on net SGST paid from cash ledger as per GSTR9.
\\end{{itemize}}

\\section*{{Costing Table}}
\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & One time & Post production \\\\
\\hline
Interest subsidy & Rs. {result['interest_subsidy']} & 3 years & With cap of Rs. 10 Lakhs \\\\
\\hline
Stamp Duty Subsidy & Rs. {result['stamp_duty_subsidy']} & One time & Post production \\\\
\\hline
SGST Reimbursement & Rs. {result['sgst_reimbursement']} & 5 years & Post production \\\\
\\hline
\\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {result['total_subsidy']}.}}

\\section*{{Other Key Subsidies and Incentives}}

\\begin{{itemize}}[leftmargin=1.5em]

  \\item \\textbf{{Electricity Duty (ED) Exemption:}} Up to 100\\% exemption for eligible units for 10–15 years based on location and size.

  \\item \\textbf{{Property Tax Exemption:}} Full waiver for 5–10 years. Application via Form-PT on Invest Punjab portal.

  \\item \\textbf{{Employment Generation Subsidy:}} Rs. 36,000/year per male, Rs. 48,000/year per female/SC/BC/OBC employee for up to 5 years.

  \\item \\textbf{{Marketing and Vendor Development Support:}} 50\\% (up to Rs.10L) for international, 25\\% (up to Rs.3L) for domestic fairs; Rs. 5Cr support for MSME cluster events.

  \\item \\textbf{{Non-Fiscal Incentives:}} PAPRA exemption, liberal FAR, flatted factories for MSMEs.

  \\item \\textbf{{Sector-Specific Incentives:}} e.g., 100\\% tax reimbursement for food processing units, Rs.10Cr top-up under M-SIPS for electronics.

\\end{{itemize}}

\\section*{{Estimated Disbursement Timeline}}
Sanction within 90 days. Disbursal between 3–6 months depending on department funds. SGST reimbursements are annual post-GSTR9 filing.

\\section*{{How SCPL Helps}}

\\begin{{itemize}}[leftmargin=1.5em]
  \\item End-to-end support until subsidy is received.
  \\item Regular follow-up and updates in case of delays.
\\end{{itemize}}

\\section*{{Value Added Services}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item DPR preparation
  \\item Market research
  \\item DSIR (R\\&D certification) grant support
  \\item IP protection: patents, trademarks, copyrights
\\end{{itemize}}

\\section*{{Not Sure?}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Ask for references from our happy customers.
\\end{{itemize}}

\\section*{{Disclosure}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Estimates based on client input; actuals may vary.
  \\item Government decisions and document quality may impact eligibility or amount.
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
      log_file = os.path.join(output_dir, "pdflatex_error.log")
      with open(log_file, "w") as f:
        f.write("STDOUT:\n" + result.stdout + "\n\nSTDERR:\n" + result.stderr)
      raise Exception(f"PDF generation failed. Details saved to {log_file}")

    
    return pdf_path
