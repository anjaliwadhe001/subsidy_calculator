# report_generator file
# Need to add subsidies to this report 
import pandas as pd
import os

def generate_pdf(user_data, result, zone, zone_data):
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


\\item {user_data['Organization Name']} \\\\
\\item {user_data['Subdistrict']}, {user_data['District']}, {user_data['State']} \\\\
\\textbf{{Attn.:}} {user_data['Name']}

\\vspace{{1em}}

\\section*{{Overview}}
Subsidy4India has identified various subsidies available for your organisation for your manufacturing unit in {user_data['District']}, {user_data['Subdistrict']} \\& {user_data['State']} and sharing the evaluation report for your perusal which is located in Zone \\textbf{{{zone}}}.

\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Name of Scheme:}} Haryana Enterprises & Employment Policy 2020
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Within the policy period.
\\end{{itemize}}

\\section*{{Subsidy Breakdown}}
\\begin{{itemize}}[leftmargin=1.5em]
  \\item \\textbf{{Capital investment subsidy (One-time):}} You can avail the capital subsidy only once 
after your unit starts commercial production, by applying online 
within three months
  \\item \\textbf{{Stamp Duty exemption / reimbursement:}} Stamp Duty exemption is 
available during purchase of industrial land for the project / Stamp Duty 
reimbursement would be available to the land owner only and the same entity 
should be billing the client when the manufacturing unit commences production 
  \\item \\textbf{{Interest subsidy(applicable only when a term loan is availed for the project):}} Zone A & B have 5 %interest subsidy benefits for 5 years
  and Zone C & D have 6% benefits for 7 years 
   \\item \\textbf{{SGST reimbursement: }} Kindly note that you can avail SGST reimbursement for capital investment made to the 
tune of {user_data['Capital investment']} and the same will be {(zone_data["SGST Initial (%)"] / 100) + (zone_data["SGST Extended (%)"] / 100)}of the investment made 
which comes to {result['SGST reimbursement']} payable over {zone_data["SGST Initial Years"]+zone_data["SGST Extended Years"]} years 
\\item SGST reimbursement calculation (will be strictly available on SGST paid from cash ledger as 
per GSTR9 filed annually 

 \\item \\textbf{{Estimated Date of receipt: }}  There will be a sanction provided for each of the subsidy 
application made which is sanctioned in upto 90 days and then disbursed as per funds 
availability with the Govt. Department and ranges from 3 months to 6 months from the 
date of sanction of the subsidy application.  
In the case of SGST reimbursement, the company needs to file for the same every 
year post filing of annual GST return i.e. GSTR9 after which the SGST reimbursement 
is made ranging from 3 months to 6 months from the date of filing SGST 
reimbursement application. 
\\end{{itemize}}

\\section*{{Costing Table}}
\\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & 1 & One-time post production \\\\
\\hline
Stamp Duty reimbursement & Rs. {result['stamp_duty_exemption']} & 1 & Available during purchase \\\\
\\hline
Interest subsidy & Rs. {result['interest_subsidy']} & 7 (from system) & Post production \\\\
\\hline
SGST reimbursement & Rs. {result['sgst_reimbursement']} & 7 (from system) & Paid from cash ledger \\\\
\\hline
\\end{{longtable}}

\\section*{{How will SCPL ensure the subsidy gets into your bank account? }}
\\begin{{itemize}}[leftmargin=1.5em]
\\item ● SCPL will work with the client to ensure that the last rupee of subsidy is received in your 
bank account and the contract is valid till we achieve the same  
\\item ● If there is a delay in receipt of the subsidy amount due to operational reasons or budget 
allocation delay with the respective Govt. Department, SCPL will keep the client informed at 
every step

\\section*{{Value Added Services }} 
\\begin{{itemize}}[leftmargin=1.5em]
\\item ● Preparation of Detailed Project Report (DPR)  
\\item ● Market Research to plan your Go To Market Strategy  
\\item ● DSIR (R&D certification) project for accessing R&D funding including grants from Govt. agencies  
\\item ● Intellectual Property protection by filing patent, design registration, trademark and copyright in India and global jurisdictions 

\\section*{{Not sure}} 
\\begin{{itemize}}[leftmargin=1.5em]
\\item Conduct a referral check by asking to get in touch with our happy customers

\\section*{{Disclosure}}
\\begin{{itemize}}[leftmargin=1.5em]
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
    with open("report.tex", "w", encoding="utf-8") as f:
        f.write(tex_content)

    # Compile to PDF
    os.system("pdflatex -interaction=nonstopmode report.tex")
    return "report.pdf"
