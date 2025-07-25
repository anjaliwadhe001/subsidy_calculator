# report_generator file
import pandas as pd
import subprocess
import os
import traceback

def generate_report_rajasthan(user_data, result, zone):
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
  \\item \\textbf{{Name of Scheme:}} Rajasthan Investment Promotion Scheme 2024
  \\item \\textbf{{Base of subsidy:}} Subsidy schemes applicable to your company as a MSME / Large / Mega entity
  \\item \\textbf{{Estimated subsidy value:}} Each subsidy has been mentioned in detail in the proposal.
  \\item \\textbf{{Date of start of commercial production:}} Within the policy period.
\\end{{itemize}}

\\section*{{Subsidy Breakdown}} 

\\textbf{{1.Asset Creation Incentives (You can choose only one of the following)}} \\\\
\\begin{{itemize}}[leftmargin=1.5em]
    \\item \\textbf{{(a)Capital investment subsidy (One-time):}} According to MSME Policy 2024, Plastic alternative, Agricultural and Food processing industries will get subsidy 50\\% of their capital investment with the cap of Rs. 40 lakhs and Rs. 1.5 Crore respectively. 
    \\item \\textbf{{(b)Turnover-linked Incentives: }}Large, Mega and Ultra-mega industries are eligible to get Turnover-linked Incentives based on net sales turnover for 10 years.
    \\item \\textbf{{(c)SGST reimbursement: }}Kindly note that you can avail SGST reimbursement 75\\% of the SGST paid for 7 years and 10 years for MSME and Large, Mega, Ultra mega enterprises respectively.
    \\item \\textbf{{Stamp Duty Subsidy is not available for Rajasthan}}
\\end{{itemize}}

\\section*{{Subsidy Snapshot}}

\\begin{{longtable}}{{|p{{3cm}}|p{{4cm}}|p{{4cm}}|p{{4cm}}|}}
\\hline
\\textbf{{Subsidy head}} & \\textbf{{Total subsidy}} & \\textbf{{No. of years}} & \\textbf{{Assumption}} \\\\
\\hline
Capital Investment Subsidy & Rs. {result['capital_investment_subsidy']} & Disbursed over 10 years  & One-time post production \\\\
\\hline
Turnover-linked Incentives & Rs. {result['turnover_linked_incentive']} & Disbursed annually for 10 years & Available only fot Large, Mega and Ultra Mega Enterprises \\\\
\\hline
SGST reimbursement & Rs. {result['sgst_reimbursement']} & Disbursed equally over 7 years(10 years for MSMEs) & \\\\
\\hline
\\end{{longtable}}

\\begin{{itemize}}
    \\item \\textbf{{2.Interest Subvention(applicable only when a term loan is availed for the project):}} In rajasthan interest subsidy depends on term loan amount. \\\\
\\end{{itemize}}
\\\\
\\begin{{longtable}}{{|p{{4cm}}|p{{3cm}}|}}
\\hline
\\textbf{{Loan amount(in Cr)}} & \\textbf{{Interest rate}} \\\\
\\hline
Upto 5 Cr & 6\\% \\\\
\\hline
Rs.5 - 10 Cr & 4\\% \\\\
\\hline 
Rs.10 - 15 Cr & 3\\% \\\\
\\hline
\\end{{longtable}}

Additional (0.5–2\\%) for ODOP/SC/ST/women/backward areas \\\\

\\begin{{longtable}}{{|p{{3cm}}|p{{4cm}}|p{{3cm}}|p{{4cm}}|}}
\\hline
Interest subsidy & Rs. {result['interest_subsidy']} & Disbursed over 7 years & Post production \\\\
\\hline
\\end{{longtable}}

\\textbf{{Total estimated subsidy available is Rs. {result['total_subsidy']}.}}

\\section*{{Key Subsidy Types \& Eligibility Periods}}
\\begin{{itemize}}
    \\item \\textbf{{Employment Booster: }}10–15\\% additional incentive for exceeding employment thresholds
    \\item \\textbf{{Thrust Booster: }}10\\% additional benefits for thrust sectors
    \\item \\textbf{{Anchor Booster: }}20\\% additional benefits for first 3 mega/ultra-mega projects in a sector/region
    \\item \\textbf{{Green Growth Incentives: }}50\\% reimbursement for environmental infrastructure (maximum Rs. 1 Cr for MSMEs)
    \\item \\textbf{{Special Sectors: }}Sunrise sectors (e.g., green hydrogen, semiconductors) get additional “Sunrise Booster” (25\\% extra for first 3 mega/ultra-mega projects)
    \\item \\textbf{{Exemptions: }}100\\% exemption on electricity duty, mandi fee, and land tax for 7 years; 75\\% exemption + 25\\% reimbursement on stamp duty and conversion charges
    \\item \\textbf{{Employment Generation Subsidy: }}50\\% of employer’s EPF/ESI contribution for 7 years for MSMEs
    \\item \\textbf{{Cluster incentives: }}
\\end{{itemize}}
\\begin{{itemize}}[leftmargin=1.5em]
\\item \\textbf{{Grant- }}80\\% of project cost(Max 10 Cr) for CFCs in MSME Clusters \\\\
        90\\% for SC/ST/Women owned ODOP Clusters
\\item \\textbf{{Eligible Infrastructure: }}Testing labs, packaging units, training centers, recycling plants
\\end{{itemize}} 

\\section*{{Estimated Date of receipt: }} \\\\
There will be a sanction provided for each of the subsidy 
application made which is sanctioned in upto 90 days and then disbursed as per funds 
availability with the Govt. Department and ranges from 3 months to 6 months from the 
date of sanction of the subsidy application.  \\\\
\\\\
In the case of SGST reimbursement, the company needs to file for the same every 
year post filing of annual GST return i.e. GSTR9 after which the SGST reimbursement 
is made ranging from 3 months to 6 months from the date of filing SGST 
reimbursement application. 

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
