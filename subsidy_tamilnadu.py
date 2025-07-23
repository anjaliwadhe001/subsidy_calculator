import pandas as pd
from report_tamilnadu import generate_report_tamilnadu

# Load Zone Mapping Data
df = pd.read_csv("Tamilnadu_district_zone.csv")
df.columns = df.columns.str.strip()
df['District'] = df['District'].str.strip().str.lower()

# Calculation
def calculate_subsidy(zone, enterprise_size, plant_machinery, building_civil_work, land_cost,
                      term_loan_amount):

    enterprise_size = enterprise_size.strip().capitalize()
    capital_investment = plant_machinery + building_civil_work

    # Capital Subsidy 
    if enterprise_size in ["Small", "Medium"]:
        capital_subsidy = min(0.25 * capital_investment, 15000000)
    elif enterprise_size == "Micro":
        capital_subsidy = min(0.25 * capital_investment, 2500000)
    elif enterprise_size == "Large": # for zone A not applicable 
        if zone == "B":
            capital_subsidy = 0.10 * capital_investment
        elif zone == "C":
            capital_subsidy = 0.12 * capital_investment
    elif enterprise_size == "Mega":
        if zone == "A":
            capital_subsidy = 0.10 * capital_investment
        elif zone == "B":
            capital_subsidy = 0.12 * capital_investment
        elif zone == "C":
            capital_subsidy = 0.15 * capital_investment
    elif enterprise_size == "Ultra Mega":
        if zone == "A":
            capital_subsidy = 0.20 * capital_investment
        elif zone == "B":
            capital_subsidy = 0.22 * capital_investment
        elif zone == "C":
            capital_subsidy = 0.25 * capital_investment
    else:
        capital_subsidy = 0

    # Stamp Duty Subsidy
    if enterprise_size in ["Small", "Medium"]:
        stamp_duty_subsidy = land_cost * 0.07 * 0.50 #50% reimbursment
    elif enterprise_size == "Micro":
        stamp_duty_subsidy = 0.07 * land_cost #100% reimbursment
    elif enterprise_size in ["Mega", "Ultra-Mega"] and zone == "A":
        stamp_duty_subsidy = 0.50 * 0.07 * land_cost #50% reimbursment
    elif enterprise_size in ["Large", "Mega", "Ultra-Mega"] and zone == "B":
        stamp_duty_subsidy = 0.50 * 0.07 * land_cost #50% reimbursment
    elif enterprise_size in ["Large", "Mega", "Ultra-Mega"] and zone == "C":
        stamp_duty_subsidy = 0.07 * land_cost #100% reimbursment
    else:
        stamp_duty_subsidy = 0

    # Interest Subsidy
    if enterprise_size in ["Micro", "Small", "Medium"]:
        interest_eligibility_years = 5
    else:
        interest_eligibility_years = 6
        
    if enterprise_size in ["Micro", "Small", "Medium"]:
        interest_subsidy = min(term_loan_amount * 0.05, 2000000) * interest_eligibility_years 
    elif enterprise_size == "Large":
        interest_subsidy = min(term_loan_amount * 0.05, 2000000) * interest_eligibility_years
    elif enterprise_size == "Mega":
        interest_subsidy = min(term_loan_amount * 0.05, 10000000) * interest_eligibility_years
    elif enterprise_size == "Ultra Mega":
        interest_subsidy = min(term_loan_amount * 0.05, 40000000) * interest_eligibility_years
    else: 
        interest_subsidy = 0

    # SGST Reimbursement (not applicable for MSMEs)
    if enterprise_size == "Large" and zone == "A":
        sgst_eligibility_years = 0
        sgst_reimbursement = 0
    elif enterprise_size in ["Large", "Mega", "Ultra-Mega"]:
        sgst_eligibility_years = 0
        sgst_reimbursement = 1.00 * capital_investment * sgst_eligibility_years #100% reimbursement for 15 years 
    else:
        sgst_eligibility_years = 0 
        sgst_reimbursement = 0

    # Total subsidy 
    total_subsidy = capital_subsidy + sgst_reimbursement + stamp_duty_subsidy + interest_subsidy

    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "stamp_duty_subsidy": round(stamp_duty_subsidy, 2),
        "interest_subsidy": round(interest_subsidy, 2),
        "interest_eligibility_years": interest_eligibility_years,
        "sgst_reimbursement": round(sgst_reimbursement, 2),
        "sgst_eligibility_years": sgst_eligibility_years,
        "total_subsidy": round(total_subsidy, 2)
    }

def process_tamilnadu(data):
    try:
        # Extract values
        district = data["District"].strip().lower()
        enterprise_size = data["Enterprise Size"]
        plant_machinery = float(data["Plant and Machinery Investment"])
        building_civil_work = float(data["Building and Civil Work Investment"])
        land_cost = float(data.get("Land Cost",0))
        term_loan_amount = float(data.get("Term Loan Amount",0))

        #Zone 
        zone_row = df[df['District'].str.lower() == district]
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
            land_cost,
            term_loan_amount
        )

        # Generate report
        pdf_path = generate_report_tamilnadu(data, result, zone)

        return {
            "zone": zone,
            "subsidy_result": result,
            "report_path": pdf_path
        }

    except Exception as e:
        return {
            "error": f"Error processing Tamilnadu subsidy: {str(e)}"
        }