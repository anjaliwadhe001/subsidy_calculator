# report_generator file
import pandas as pd
import os
import subprocess

def generate_report_mp(user_data, result):
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
  \\item \\textbf{{Name of Scheme:}}The Madhya Pradesh Industrial Promotion Policy 2025 
  \\item \\textbf{{Base of subsidy:}}Subsidy schemes applicable to your company as a MSME / Large / Mega / Super mega / Ultra Mega entity
  \\item \\textbf{{Estimated subsidy value:}}Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Subsidies apply only to investments made by 2028-29.\\\\
This framework aims to attract Rs. 5.4–5.9 lakh crore in industrial investment by 2028–29 while generating Rs. 20 lakh 
jobs. For updates, refer to the latest notifications from the Department of Industrial Policy and Investment 
Promotion.
\\end{{itemize}}

\\section*{{Subsidy Breakdown}}
  \\begin{{itemize}}[leftmargin=1.5em]
  \\textbf{{1. Capital investment subsidy (One-time):}} The Basic Investment Promotion Assistance (BIPA) under the Madhya Pradesh Industrial Promotion Policy 2025 is a capital subsidy provided as a percentage of Eligible Fixed Capital Investment (EFCI). \\\\
        \\item The BIPA subsidy ranges from 40\\% down to 10\\% of EFCI for large units, depending on the investment amount.\\\\
        \\item The maximum subsidy amount is Rs. 200 crore, disbursed in 7 equal annual installments.
    
  \\textbf{{2. Interest subsidy(applicable only when a term loan is availed for the project):}} Interest Subsidy is available 6\\% interest reimbursement on term loans,or the actual interest paid whichever is lowerwith the cap of Rs 10 crores per unit over period of 7 years.\\\\
        \\item Term loans taken for capital expenditure (plant, machinery, infrastructure, and technology upgrades) are covered.\\\\
        \\itemm Special emphasis is given to women-led businesses, green-tech, and sectors like IT/ITeS, semiconductors, textiles, and EVs, which may have tailored rates or additional support. \\\\
  \\end{{itemize}}

\\section*{{Costing Table}}
\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{3cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & One Time & Post production \\\\
\\hline
Interest subsidy & Rs. {result['interest_subsidy']} & 7 years & Rs.10 Cr per unit over the eligible period  \\\\
\\hline
\\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {result['total_subsidy']}.}}

\\section*{{Other Subsidies \\& Incentives Framework}}

\\textbf{{1. Infrastructure Development Assistance}}
  \\begin{{itemize}}
    \\item 50\\% subsidy (up to Rs. 5 crore) for infrastructure development up to the factory gate (includes power, water, roads, etc.).
    \\item Applicable if the unit is established on private or undeveloped government land.
    \\item Separate infrastructure development subsidy of 50\\% (up to Rs. 1 crore each) for water, electricity, and roads for private/undeveloped government land.
  \\end{{itemize}}

\\textbf{{2. Green Industrialization Assistance}}
  \\begin{{itemize}}
    \\item 50\\% subsidy (up to Rs. 5 crore) for installing waste management systems (e.g., Effluent Treatment Plant, Sewage Treatment Plant).
    \\item For units with Zero Liquid Discharge systems, the subsidy cap increases to Rs. 10 crore.
    \\item 25\\% additional capex subsidy for green-certified plants (recognized sustainability standards).
  \\end{{itemize}}

\\textbf{{3. Special Incentives for Priority Sectors \\& Zones}}
  \\begin{{itemize}}
    \\item \\textbf{{Sector-Specific Tailored Incentives:}} Enhanced support for Electric Vehicles, Green Hydrogen, Data Centres, Agro \\& Food Processing, Pharmaceuticals, etc.
    \\item \\textbf{{Zone-Based Multipliers:}} Higher subsidies for units in backward or priority blocks (e.g., Bundelkhand, Chambal).
  \\end{{itemize}}

\\section*{{Estimated Date of receipt: }}There will be a sanction provided for each of the subsidy 
application made which is sanctioned in upto 90 days and then disbursed as per funds 
availability with the Govt. Department and ranges from 3 months to 6 months from the 
date of sanction of the subsidy application. \\\\ 
In the case of SGST reimbursement, the company needs to file for the same every 
year post filing of annual GST return i.e. GSTR9 after which the SGST reimbursement 
is made ranging from 3 months to 6 months from the date of filing SGST 
reimbursement application. 
\\end{{itemize}}

\\section*{{How will SCPL ensure the subsidy gets into your bank account? }}
  \\begin{{itemize}}[leftmargin=1.5em]
      \\item SCPL will work with the client to ensure that the last rupee of subsidy is received in your 
      bank account and the contract is valid till we achieve the same  
      \\item If there is a delay in receipt of the subsidy amount due to operational reasons or budget 
      allocation delay with the respective Govt. Department, SCPL will keep the client informed at 
      every step
  \\end{{itemize}}

\\section*{{Value Added Services }} 
  \\begin{{itemize}}[leftmargin=1.5em]
      \\item  Preparation of Detailed Project Report (DPR)  
      \\item  Market Research to plan your Go To Market Strategy  
      \\item  DSIR (R\\&D certification) project for accessing R\\&D funding including grants from Govt. agencies  
      \\item  Intellectual Property protection by filing patent, design registration, trademark and copyright in India and global jurisdictions 
  \\end{{itemize}}

\\section*{{Not sure}} 
\\item Conduct a referral check by asking to get in touch with our happy customers

\\section*{{Disclosure}}
\\item SCPL (parent company of Subsidy4India) Team has calculated the subsidy based on 
details provided by the client and the same can vary depending on the capital investment 
made by the client. exact location of the land where the manufacturing unit is being 
setup, documents provided for registering the subsidy application and any follow up 
documents required by the Central or State Government authorities and will not be liable 
for any reduction in subsidy amount applicable to the client including the client being 
determined as non-eligible to avail the subsidy due to lack of documentation, change of 
policy and non-cooperation by client

\\end{{document}}
"""
    with open("Subsidy_Report.tex", "w", encoding="utf-8") as f:
        f.write(tex_content)

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "Subsidy_Report.tex"],
        capture_output=True, # Changed to capture_output=True
        text=True # Changed to text=True for string output
    )

    if result.returncode != 0:
        print("LaTeX compilation failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise Exception(f"LaTeX compilation failed. Check .log file for details. Error: {result.stderr}")

    return "Subsidy_Report.pdf"