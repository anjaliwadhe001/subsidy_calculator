#Ask for stamp duty eligibility 

# report_generator file
import pandas as pd
import subprocess
import os

def generate_report_tamilnadu(user_data, result, zone):
    interest_eligibility_years = result.get('interest_eligibility_years', '')
    if interest_eligibility_years:
        interest_eligibility_years = f"{interest_eligibility_years} years"

    sgst_eligibility_years = result.get('sgst_eligibility_years', '')
    if sgst_eligibility_years:
        sgst_eligibility_years = f"{sgst_eligibility_years} years"
    
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
Offices in New Delhi \\& New York\\\\

\\end{{center}}

\\textbf{{Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}}}

\\vspace{{1em}}
\\item {user_data['Organization Name']} \\\\
\\item {user_data['District']}, {user_data['State']} \\\\
\\textbf{{Attn.:}} {user_data['Name']}

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

  \\textbf{{(a)Capital investment subsidy (One-time):}} According to Industrial policy 2025, You can avail capital subsidy only once post production which is disbursed over eligible years.
  \\textbf{{(b)SGST reimbursement:}} SGST reimbursement calculation will be strictly available on SGST paid from cash ledger as per GSTR9 filed annually. 
    According to Tamilnadu industrial policy eligible enterprises will get sgst reimbursement for 15 years\\\\
  \\textbf{{(c)Interest Subsidy(applicable only when a term loan is availed for the project):}}  According to Tamilnadu industrial policy 2025, Interest subsidy for MSMEs project is available for 5 yeras and for Large and above projects 6 years\\\\
  \\\\

\\section*{{Costing Table}}
    \\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
    \\hline
    \\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
    \\hline
    Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & Disbursed over 7 years & One-time post production \\\\
    \\hline
    SGST reimbursement & Rs. {result['sgst_reimbursement']} & {{{sgst_eligibility_years}}} & Paid from cash ledger \\\\
    \\hline
    Stamp Duty & Rs. {result['stamp_duty_subsidy']} & One Time & Sub-Large projects are generally not eligible for this incentive\\\\
    \\hline
    Interest Subsidy & Rs. {result['interest_subsidy']} & {{{interest_eligibility_years}}} & Quarterly reimbursements to financial institutions \\\\
    \\hline
    \\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {result['total_subsidy']}.}}  

\\section*{{Other Incentives}}

\\begin{{enumerate}}
  \\item \\textbf{{Training Subsidy}} \\\\
    \\begin{{itemize}}
      \\item \\textbf{{Objective:}} Support skilling and employment of local workforce.\\\\
      \\item \\textbf{{Amount:}} \\\\
        \\begin{{itemize}}
          \\item Rs. 4,000 per worker per month for 6 months (general category). \\\\
          \\item Rs. 6,000 per worker per month for 6 months (for women, transgender, SC/ST, and persons with benchmark disabilities).\\\\
        \\end{{itemize}}
      \\item \\textbf{{Eligibility:}} New or expansion manufacturing projects employing residents of Tamil Nadu. \\\\
      \\item \\textbf{{Purpose:}} Offsets initial training costs and encourages inclusive hiring.\\\\
    \\end{{itemize}}

   \\item \\textbf{{Electricity Tax Incentive}} \\\\
    \\begin{{itemize}}
      \\item \\textbf{{Benefit:}} 100\\% exemption from electricity tax. \\\\
      \\item \\textbf{{Duration:}} 5 years from commencement of commercial production. \\\\
      \\item \\textbf{{Applicability:}} \\\\
        \\begin{{itemize}}
          \\item Power purchased from TANGEDCO (Tamil Nadu Generation and Distribution Corporation Ltd.). \\\\
          \\item Power generated and consumed from captive sources. \\\\
        \\end{{itemize}}
      \\item \\textbf{{Objective:}} Reduces operational costs for new and expanding manufacturing units. \\\\
    \\end{{itemize}}

  \\item \\textbf{{Green Industry Incentive}}
    \\begin{{itemize}}
      \\item \\textbf{{Benefit:}} 25\\% subsidy on the cost of setting up environmental protection infrastructure. \\\\
      \\item \\textbf{{Cap:}} Up to Rs. 1 crore per project. \\\\
      \\item \\textbf{{Eligible Activities:}} \\\\
        \\begin{{itemize}}
          \\item Safety and energy efficiency solutions.\\\\
          \\item Water conservation. \\\\
          \\item Pollution control. \\\\
          \\item Greening solutions. \\\\
        \\end{{itemize}}
      \\item \\textbf{{Objective:}} Promotes sustainable and eco-friendly industrial practices.\\\\
    \\end{{itemize}}

  \\item \\textbf{{Special Incentives for R\\&D Projects}}
    \\begin{{itemize}}
      \\item \\textbf{{Eligibility:}} Standalone R\\&D projects with a minimum investment of Rs. 50 crore and employment for at least 50 persons, 
      registered with DSIR (Department of Scientific and Industrial Research).  \\\\
      \\item \\textbf{{Benefits:}} \\\\
        \\begin{{itemize}}
          \\item 50\\% land cost reimbursement (as applicable) \\\\
          \\item Training subsidy (as mentioned above) \\\\
          \\item Eligible for standard incentives (excluding IP creation and quality certification) \\\\
        \\end{{itemize}}
    \\end{{itemize}}
\\end{{enumerate}}



\\textbf{{Estimated Date of receipt: }}  \\\\
There will be a sanction provided for each of the subsidy 
application made which is sanctioned in upto 90 days and then disbursed as per funds 
availability with the Govt. Department and ranges from 3 months to 6 months from the 
date of sanction of the subsidy application.  
In the case of SGST reimbursement, the company needs to file for the same every 
year post filing of annual GST return i.e. GSTR9 after which the SGST reimbursement 
is made ranging from 3 months to 6 months from the date of filing SGST 
reimbursement application. 
\\end{{itemize}}


\\section*{{How will SCPL ensure the subsidy gets into your bank account? }}

\\item SCPL will work with the client to ensure that the last rupee of subsidy is received in your 
bank account and the contract is valid till we achieve the same  
\\item If there is a delay in receipt of the subsidy amount due to operational reasons or budget 
allocation delay with the respective Govt. Department, SCPL will keep the client informed at 
every step

\\section*{{Value Added Services }} 
\\item Preparation of Detailed Project Report (DPR)  
\\item Market Research to plan your Go To Market Strategy  
\\item DSIR (R\\&D certification) project for accessing R\\&D funding including grants from Govt. agencies  
\\item Intellectual Property protection by filing patent, design registration, trademark and copyright in India and global jurisdictions 

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

