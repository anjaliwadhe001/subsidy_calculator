#Add startup as a option in enterprise size
from report_punjab import generate_report_punjab
 
# No zonification

# Calculation logic
def calculate_subsidy(enterprise_size, plant_machinery, building_civil_work, land_cost,
                      term_loan_amount, net_sgst_paid_cash_ledger):

    enterprise_size = enterprise_size.strip().capitalize()
    capital_investment = plant_machinery + building_civil_work

    capital_subsidy = 0
    stamp_duty_subsidy = 0
    interest_subsidy = 0
    sgst_reimbursement = 0

    # Capital Subsidy 
    if enterprise_size in ["Micro", "Small"]:
        capital_subsidy = min(0.25 * capital_investment, 2500000) 
    else: 
        capital_subsidy = 0
  
    # Stamp Duty Subsidy 
    # 100% exemption for MSMEs 
    if enterprise_size in ["Micro", "Small", "Medium", "Large"]:
        stamp_duty_subsidy = 0.07 * land_cost
    
    # Interest Subsidy
    
    if enterprise_size in ["Micro", "Small", "Medium"]:
        interest_subsidy = min(term_loan_amount * 0.05  , 1000000) * 3
    elif enterprise_size == "Startup":  
        interest_subsidy = min(term_loan_amount * 0.08  , 500000) * 3
    else: 
        interest_subsidy = 0

    # SGST Reimbursement (Eligibility 5 years )
    if enterprise_size == "Startup":  
        sgst_reimbursement = net_sgst_paid_cash_ledger * 5
    elif enterprise_size == "Small":
        sgst_reimbursement = min(0.60 * net_sgst_paid_cash_ledger, 0.60 * capital_investment) * 5
    elif enterprise_size == "Micro":
        sgst_reimbursement = min(0.70 * net_sgst_paid_cash_ledger, 0.70 * capital_investment) * 5 
    elif enterprise_size == "Medium":
        sgst_reimbursement = min(0.50 * net_sgst_paid_cash_ledger, 0.50 * capital_investment) * 5
    elif enterprise_size == "Large":
        sgst_reimbursement = min(0.30 * net_sgst_paid_cash_ledger, 0.30 * capital_investment) * 5
    else:
        sgst_reimbursement = 0 

    #Total Subsidy
    total_subsidy = capital_subsidy + sgst_reimbursement + stamp_duty_subsidy + interest_subsidy

    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "interest_subsidy": round(interest_subsidy, 2),
        "sgst_reimbursement": round(sgst_reimbursement, 2),
        "stamp_duty_subsidy":round(stamp_duty_subsidy,2),
        "total_subsidy": round(total_subsidy, 2)
    }    

def process_punjab(data):
    try:
        # Extract values
        enterprise_size = data["Enterprise Size"]
        plant_machinery = float(data["Plant and Machinery Investment"])
        building_civil_work = float(data["Building and Civil Work Investment"])
        land_cost = float(data.get("Land Cost",0))
        term_loan_amount = float(data.get("Term Loan Amount",0))
        net_sgst_paid_cash_ledger = float(data["Net SGST Paid Cash Ledger"])

        # Perform calculations
        result = calculate_subsidy(
            enterprise_size,
            plant_machinery,
            building_civil_work,
            land_cost,
            term_loan_amount,
            net_sgst_paid_cash_ledger,
        )
        
        # Generate report
        pdf_path = generate_report_punjab(data, result)
        
        return {
            "subsidy_result": result,
            "report_path": pdf_path
        }

    except Exception as e:
        return {
            "error": f"Error processing Punjab subsidy: {str(e)}"
        }