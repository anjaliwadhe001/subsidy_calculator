import pandas as pd
import subprocess
import os 

def generate_report_mp(user_data, result):
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    # Construct a safe filename based on user's name
    safe_name = user_data.get("Name", "user").replace(" ", "_")
    filename = f"{safe_name}_Subsidy_Report.pdf"
    tex_filename = f"{safe_name}_Subsidy_Report.tex"

    # Full paths
    tex_path = os.path.join(output_dir, tex_filename)
    pdf_path = os.path.join(output_dir, filename)

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
Offices in New Delhi \\& New York\\\\
\\end{{center}}

\\textbf{{Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}}}

\\vspace{{1em}}

{user_data['Organization Name']} \\\\
{user_data['District']}, {user_data['State']} \\\\
\\textbf{{Attn.:}} {user_data['Name']}

\\vspace{{1em}}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {user_data['District']}, {user_data['State']} and sharing the evaluation report for your organization.

\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Name of Scheme:}} The Madhya Pradesh Industrial Promotion Policy 2025
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega / Super mega / Ultra Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Subsidies apply only to investments made by 2028-29. \\\\
  This framework aims to attract Rs. 5.4–5.9 lakh crore in industrial investment by 2028–29 while generating Rs. 20 lakh jobs.
  For updates, refer to the latest notifications from the Department of Industrial Policy and Investment Promotion.
\\end{{itemize}}

\\section*{{Subsidy Breakdown}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Capital investment subsidy (One-time):}} The Basic Investment Promotion Assistance (BIPA) under the Madhya Pradesh Industrial Promotion Policy 2025 is a capital subsidy provided as a percentage of Eligible Fixed Capital Investment (EFCI).
  \\item The BIPA subsidy ranges from 40\\% down to 10\\% of EFCI for large units, depending on the investment amount.
  \\item The maximum subsidy amount is Rs. 200 crore, disbursed in 7 equal annual installments.
  \\item \\textbf{{Interest subsidy (term loan-based):}} Interest Subsidy is available — 6\\% interest reimbursement on term loans, or the actual interest paid whichever is lower, with a cap of Rs. 10 crores per unit over 7 years.
  \\item Term loans taken for capital expenditure (plant, machinery, infrastructure, and technology upgrades) are covered.
  \\item Special emphasis is given to women-led businesses, green-tech, and sectors like IT/ITeS, semiconductors, textiles, and EVs, which may have tailored rates or additional support.
\\end{{itemize}}

\\section*{{Costing Table}}
\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{3cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & One Time & Post production \\\\
\\hline
Interest subsidy & Rs. {result['interest_subsidy']} & 7 years & Rs.10 Cr per unit over the eligible period \\\\
\\hline
\\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {result['total_subsidy']}.}}

\\section*{{Other Subsidies \\& Incentives Framework}}

\\textbf{{1. Infrastructure Development Assistance}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item 50\\% subsidy (up to Rs. 5 crore) for infrastructure development up to the factory gate (includes power, water, roads, etc.).
  \\item Applicable if the unit is established on private or undeveloped government land.
  \\item Separate infrastructure development subsidy of 50\\% (up to Rs. 1 crore each) for water, electricity, and roads for private/undeveloped government land.
\\end{{itemize}}

\\textbf{{2. Green Industrialization Assistance}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item 50\\% subsidy (up to Rs. 5 crore) for installing waste management systems (e.g., Effluent Treatment Plant, Sewage Treatment Plant).
  \\item For units with Zero Liquid Discharge systems, the subsidy cap increases to Rs. 10 crore.
  \\item 25\\% additional capex subsidy for green-certified plants (recognized sustainability standards).
\\end{{itemize}}

\\textbf{{3. Special Incentives for Priority Sectors \\& Zones}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Sector-Specific Tailored Incentives:}} Enhanced support for Electric Vehicles, Green Hydrogen, Data Centres, Agro \\& Food Processing, Pharmaceuticals, etc.
  \\item \\textbf{{Zone-Based Multipliers:}} Higher subsidies for units in backward or priority blocks (e.g., Bundelkhand, Chambal).
\\end{{itemize}}

\\section*{{Estimated Date of Receipt}}
There will be a sanction provided for each of the subsidy applications made, which is sanctioned within up to 90 days and then disbursed as per funds availability with the Govt. Department — ranging from 3 to 6 months from the date of sanction. \\\\
In the case of SGST reimbursement, the company must file annually post-GSTR9 filing; reimbursement then takes 3 to 6 months.

\\section*{{How will SCPL ensure the subsidy gets into your bank account?}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item SCPL will work with the client to ensure that the last rupee of subsidy is received in your bank account, and the contract is valid till we achieve the same.
  \\item In case of delays due to operational or budget allocation issues, SCPL will keep the client informed at every step.
\\end{{itemize}}

\\section*{{Value Added Services}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Preparation of Detailed Project Report (DPR)
  \\item Market Research to plan your Go-To-Market Strategy
  \\item DSIR (R\\&D certification) project for accessing R\\&D funding including government grants
  \\item IP protection via patent, design registration, trademark, and copyright (India + global)
\\end{{itemize}}

\\section*{{Not sure?}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item Conduct a referral check by getting in touch with our happy customers.
\\end{{itemize}}

\\section*{{Disclosure}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item SCPL (parent company of Subsidy4India) has calculated the subsidy based on client-submitted data, which may vary depending on investment amount, location, and documentation. SCPL is not liable for ineligibility, changes in policy, or insufficient documentation.
\\end{{itemize}}

\\end{{document}}
"""
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("LaTeX compilation failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise Exception("PDF generation failed. See error log.")

    return pdf_path