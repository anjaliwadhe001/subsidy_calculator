# Need to Add dropdown for  Industry type
import pandas as pd
from report_rajasthan import generate_report_rajasthan

# Load Zone Mapping Data
df = pd.read_csv("Rajasthan_subdistrict_zone.csv") 
df.columns = df.columns.str.strip()
df['Subdistrict'] = df['Subdistrict'].str.strip().str.lower()

# Zone data
zone_data = {
     #Zone A- Developed 
     #Zone B- Developing 
     #Zone C- Backward
    "A":{
        "Enterprise Size":["Micro", "Small", "Medium","Large", "Mega", "Ultra Mega"],
        "Capital Investment Subsidy(%)": [50, 50, 50, 13, 17, 23],
        "TIL Rate(%)":[0, 0, 0, 1.2, 1.4, 1.65]
    },
    "B":{
        "Enterprise Size":["Micro", "Small", "Medium","Large", "Mega", "Ultra Mega"],
        "Capital Investment Subsidy(%)": [50, 50, 50, 17, 20, 25],
        "TIL Rate(%)":[0, 0, 0, 1.4, 1.65, 1.85]
    },
    "C":{
        "Enterprise Size":["Micro", "Small", "Medium","Large", "Mega", "Ultra Mega"],
        "Capital Investment Subsidy(%)": [50, 50, 50, 20, 23, 28],
        "TIL Rate(%)":[0, 0, 0, 1.65, 1.85, 2.0]
    }
}

# Calculation logic
def calculate_subsidy(zone, enterprise_size, plant_machinery, building_civil_work, industry_type,
                      term_loan_amount, net_sgst_paid_cash_ledger,turn_over):
    
    zone_info = zone_data.get(zone)
    index = zone_info["Enterprise Size"].index(enterprise_size.strip().capitalize())
    enterprise_size = enterprise_size.strip().capitalize()

    capital_investment = plant_machinery + building_civil_work

    capital_subsidy = 0
    interest_subsidy = 0
    sgst_reimbursement = 0
    turnover_linked_incentive = 0

    # Capital Subsidy (Micro & Small only) 
    # Add in the report that Disbursed over 10 years for large projects
    if enterprise_size in ["Small", "Medium", "Micro"] and industry_type == "Plastic Alternatives":
        capital_subsidy = min(0.50 * capital_investment, 4000000)
    elif enterprise_size in ["Small", "Medium", "Micro"] and industry_type in["Agriculture processing", "Food processing"]: 
        capital_subsidy = min(0.50 * capital_investment, 15000000)
    elif enterprise_size in ["Large", "Mega", "Ultra Mega"]:
        capital_subsidy = capital_investment * (zone_info["Capital Investment Subsidy(%)"][index]/100)
    else:
        capital_subsidy = 0

    # No Stamp Duty Subsidy in rajasthan

    # Interest Subsidy

    if enterprise_size in ["Small", "Medium", "Micro"]:
        interest_rate = 0
        if term_loan_amount<=50000000:
            interest_rate = 0.06
        elif 50000000<term_loan_amount<=100000000:
            interest_rate = 0.04
        elif 100000000<term_loan_amount<=500000000:
            interest_rate = 0.03

        annual_interest = term_loan_amount * interest_rate
        interest_subsidy = min(annual_interest, 2000000) * 7 

    elif enterprise_size in ["Large", "Mega", "Ultra Mega"]:
        interest_rate = 0.05
        annual_interest = interest_rate * term_loan_amount 
        interest_subsidy = min(annual_interest, 0.025 * capital_investment) * 5


    # SGST Reimbursement
    if enterprise_size in ["Large", "Mega", "Ultra Mega"]:
        sgst_reimbursement = net_sgst_paid_cash_ledger * 0.75 * 7
    else:
        sgst_reimbursement = net_sgst_paid_cash_ledger * 0.75 * 10

    #TLI 
    if enterprise_size in ["Large", "Mega", "Ultra Mega"]:
        turnover_linked_incentive =  (zone_info["TIL Rate(%)"][index]/100) * turn_over
    else: 
        turnover_linked_incentive = 0

    # Total subsidy 
    total_subsidy = max(capital_subsidy, sgst_reimbursement, turnover_linked_incentive) + interest_subsidy

    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "interest_subsidy": round(interest_subsidy, 2),
        "sgst_reimbursement": round(sgst_reimbursement, 2),
        "turnover_linked_incentive":round(turnover_linked_incentive,2),
        "total_subsidy": round(total_subsidy, 2)
    }    

def process_rajasthan(data):
    try:
        # Extract values
        subdistrict = data["Subdistrict"].strip().lower()
        enterprise_size = data["Enterprise Size"]
        industry_type = data["Industry Type"]
        plant_machinery = float(data["Plant and Machinery Investment"])
        building_civil_work = float(data["Building and Civil Work Investment"])
        term_loan_amount = float(data["Term Loan Amount"])
        net_sgst_paid_cash_ledger = float(data["Net SGST Paid Cash Ledger"])
        turn_over = float(data["Net Turnover"])

        # Zone lookup
        zone_row = df[df['Subdistrict'].str.lower() == subdistrict]
        if zone_row.empty:
            zone = "Unknown"
        else:
            zone = zone_row.iloc[0]["Zone"]

        # Perform calculations
        result = calculate_subsidy(
            zone,
            enterprise_size,
            plant_machinery,
            building_civil_work,
            industry_type,
            term_loan_amount,
            net_sgst_paid_cash_ledger,
            turn_over
        )

        # Generate report
        pdf_path = generate_report_rajasthan(data, result, zone)

        return {
            "zone": zone,
            "subsidy_result": result,
            "report_path": pdf_path
        }

    except Exception as e:
        return {
            "error": f"Error processing Rajasthan subsidy: {str(e)}"
        }