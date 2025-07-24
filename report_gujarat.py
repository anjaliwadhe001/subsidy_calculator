#Ask for stamp duty eligibility 

# report_generator file
import pandas as pd
import os
import traceback
import subprocess

def generate_report_gujarat(user_data, result, zone):

    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    safe_name = user_data.get("Organisation Name", "user").replace(" ", "_")
    safe_name1 = user_data.get("State", "user").replace(" ", "_")
    filename = f"{safe_name}_{safe_name1}_Subsidy_Report.pdf"
    tex_filename = f"{safe_name}_{safe_name1}_Subsidy_Report.tex"

    tex_path = os.path.join(output_dir, tex_filename)
    pdf_path = os.path.join(output_dir, filename)

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

\\textbf{{Date: {pd.Timestamp.now().strftime('%d-%m-%Y')}}}

\\vspace{{1em}}
\\begin{{itemize}}
    \item {user_data['Organization Name']} \\
    \item {user_data['Subdistrict']}, {user_data['District']}, {user_data['State']} \\
\\end{{itemize}}
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

\\item \\textbf{{Asset Creation Incentives}} \\\\
\\begin{{itemize}}[leftmargin=1.5em]
    \\textbf{{(a)Capital Investment Subsidy (One-time): }}According to MSME Policy 2024, Plastic alternative, Agricultural and Food processing industries will get subsidy 50\\% of their capital investment with the cap of Rs. 40 lakhs and Rs. 1.5 Crore respectively. \\\\
    \\textbf{{(b)SGST reimbursement: }}Kindly note that you can avail SGST reimbursement of {{{sgst_rate}}} on the SGST paid for {{{sgst_eligibility_years}}} with the annual cap of {{{sgst_max_rate}}} of Fixed Capital Investment. \\\\
    \\textbf{{(c)Stamp Duty Subsidy (One-time): }}Under the Aatma nirbhar Gujarat Scheme, the government provides a \\textbf{{100\\% reimbursement of stamp duty and registration charges}} paid to the Government of Gujarat for the purchase and/or lease of land meant for eligible industrial projects.\\\\
    \\textbf{{(d)Interest Subsidy(applicable only when a term loan is availed for the project): }}Interest Subsidy is available at {{{interest_rate}}} of term loan amount for {{{interest_eligibility_years}}}. \\\\
\\end{{itemize}}
    
\\section*{{Subsidy Snapshot}}
    \\begin{{longtable}}{{|p{{4cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
    \\hline
    \\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
    \\hline
    Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & One Time years & Available only for Micro and Large Enterprises \\\\
    \\hline
    SGST reimbursement & Rs. {result['sgst_reimbursement']} & Disbursed over {{{sgst_eligibility_years}}} & Paid from cash ledger \\\\
    \\hline
    Stamp Duty Subsidy & Rs. {result['stamp_duty_subsidy']} & One Time & Available only for MSME and Mega Enterprises \\\\
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
\\begin{{itemize}}
    \\item SCPL will work with the client to ensure that the last rupee of subsidy is received in your 
    bank account and the contract is valid till we achieve the same  
    \\item If there is a delay in receipt of the subsidy amount due to operational reasons or budget 
    allocation delay with the respective Govt. Department, SCPL will keep the client informed at 
    every step
\\end{{itemize}}

\\section*{{Value Added Services }} 
\\begin{{itemize}}
    \\item Preparation of Detailed Project Report (DPR)  
    \\item Market Research to plan your Go To Market Strategy  
    \\item DSIR (R\\&D certification) project for accessing R\\&D funding including grants from Govt. agencies  
    \\item Intellectual Property protection by filing patent, design registration, trademark and copyright in India and global jurisdictions 
\\end{{itemize}}

\\section*{{Not sure}} 
\\begin{{itemize}}
    \\item Conduct a referral check by asking to get in touch with our happy customers
\\end{{itemize}}

\\section*{{Disclosure}}
\\begin{{itemize}}
    \\item SCPL (parent company of Subsidy4India) Team has calculated the subsidy based on 
    details provided by the client and the same can vary depending on the capital investment 
    made by the client. exact location of the land where the manufacturing unit is being 
    setup, documents provided for registering the subsidy application and any follow up 
    documents required by the Central or State Government authorities and will not be liable 
    for any reduction in subsidy amount applicable to the client including the client being 
    determined as non-eligible to avail the subsidy due to lack of documentation, change of 
    policy and non-cooperation by client
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