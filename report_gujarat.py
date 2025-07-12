#Ask for stamp duty eligibility 

# report_generator file
import pandas as pd
import os

def generate_report_gujarat(user_data, result, zone):
    interest_eligibility_years = result.get('interest_eligibility_years', '')
    if interest_eligibility_years:
        interest_eligibility_years = f"{interest_eligibility_years} years"

    interest_rate = result.get('interest_rate', '')
    if interest_rate:
        interest_rate = f"{interest_rate}\\%"

    sgst_max_rate = result.get('sgst_max_rate', '')
    if sgst_max_rate:
        sgst_max_rate =f"{sgst_max_rate}\\%"

    sgst_rate = result.get('sgst_rate', '')
    if sgst_rate:
        sgst_rate=f"{sgst_rate}\\%"

    sgst_eligibility_years = result.get('sgst_eligibility_years', '')
    if sgst_eligibility_years:
        sgst_eligibility_years=f"{sgst_eligibility_years} years"

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
\\item {user_data['Subdistrict']}, {user_data['District']}, {user_data['State']} \\\\
\\textbf{{Attn.:}} {user_data['Name']}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {user_data['District']}, {user_data['Subdistrict']} \\& {user_data['State']} and sharing the evaluation report for your perusal which is located in Zone \\textbf{{{zone}}}.
\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Name of Scheme:}} Atmanirbhar Gujarat Scheme
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Within the policy period (5 October 2022 - 4 October 2027).
\\end{{itemize}}

\\section*{{Subsidy Breakdown}} 
\\begin{{itemize}}[leftmargin=1.5em]
\\item \\textbf{{Asset Creation Incentives}} \\\\

    \\textbf{{(a)Capital Investment Subsidy (One-time): }}According to MSME Policy 2024, Plastic alternative, Agricultural and Food processing industries will get subsidy 50\\% of their capital investment with the cap of Rs. 40 lakhs and Rs. 1.5 Crore respectively. \\\\
    \\\\
    \\textbf{{(b)SGST reimbursement: }}Kindly note that you can avail SGST reimbursement of {{{sgst_rate}}} on the SGST paid for {{{sgst_eligibility_years}}} with the annual cap of {{{sgst_max_rate}}} of Fixed Capital Investment.\\\\
    \\\\
    \\textbf{{(c)Stamp Duty Subsidy (One-time): }}Under the Aatma nirbhar Gujarat Scheme, the government provides a \\textbf{{100\\% reimbursement of stamp duty and registration charges}} paid to the Government of Gujarat for the purchase and/or lease of land meant for eligible industrial projects. \\\\
    \\\\
    \\textbf{{(d)Interest Subsidy(applicable only when a term loan is availed for the project): }}Interest Subsidy is available at {{{interest_rate}}} of term loan amount for {{{interest_eligibility_years}}}. \\\\

\\section*{{Costing Table}}
    \\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
    \\hline
    \\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
    \\hline
    Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & One Time years & Post production \\\\
    \\hline
    SGST reimbursement & Rs. {result['sgst_reimbursement']} & Disbursed over {{{sgst_eligibility_years}}} & Paid from cash ledger \\\\
    \\hline
    Stamp Duty Subsidy & Rs. {result['stamp_duty_subsidy']} & One Time & Can be availed during purchase\\\\
    \\hline
    Interest Subsidy & Rs. {result['interest_subsidy']} & {{{interest_eligibility_years}}} & Post production\\\\
    \\hline 
    \\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {result['total_subsidy']}.}}

\\section*{{Other Key Subsidies \\& Incentives}} \\\\

\\section*{{Estimated Date of receipt }}  \\\\
There will be a sanction provided for each of the subsidy 
application made which is sanctioned in upto 90 days and then disbursed as per funds 
availability with the Govt. Department and ranges from 3 months to 6 months from the 
date of sanction of the subsidy application.  \\\\
\\\\
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
\\begin{{itemsize}}
    \\item Preparation of Detailed Project Report (DPR)  
    \\item Market Research to plan your Go To Market Strategy  
    \\item DSIR (R\\&D certification) project for accessing R\\&D funding including grants from Govt. agencies  
    \\item Intellectual Property protection by filing patent, design registration, trademark and copyright in India and global jurisdictions 
\\end{{itemsize}}

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
    with open("Subsidy_report_gujarat.tex", "w", encoding="utf-8") as f:
        f.write(tex_content)

    # Compile to PDF
    os.system("pdflatex -interaction=nonstopmode Subsidy_report_gujarat.tex")
    return "Subsidy_report_gujarat.pdf"
