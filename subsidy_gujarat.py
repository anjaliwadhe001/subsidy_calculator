import pandas as pd
from report_gujarat import generate_report_gujarat

# Load Zone Mapping Data
df = pd.read_csv("Gujarat_subdistrict_zone.csv") 
df.columns = df.columns.str.strip()
df['Subdistrict'] = df['Subdistrict'].str.strip().str.lower()

# Zone data
## Not adding thrust sectors in calculations
zone_data = {
#Zone A: Category I Taluka
#Zone B: Category II Taluka
#Zone C: Category III Taluka & Municipal Corp

    "A":{
        "Enterprise Size":["Micro","Small","Medium","Large", "Mega"],
        "Capital Subsidy(%)":[25, 0, 0, 10, 0],
        "Interest rate(%)":[7]*5, #cap 60%
        "Interest eligible years":[7, 7, 7, 10, 10],
        "Max interest": [3500000, 3500000, 3500000, 0, 0], #cap amount for interest subsidy
        "SGST reimbursement(%)": [100, 100, 100, 75, 100],
        "SGST eligibility years":[10, 10, 10, 10, 20],
        "SGST max(%)": [7.5, 7.5, 7.5, 7.5, 0.9]
    },
    "B":{
        "Enterprise Size":["Micro","Small","Medium","Large", "Mega"],
        "Capital Subsidy(%)":[20, 0, 0, 8, 0],
        "Interest rate(%)":[6]*5, #cap 60%
        "Interest eligible years":[6, 6, 6, 8, 10], 
        "Max interest": [3000000, 3000000, 3000000, 0, 0],
        "SGST reimbursement(%)":[90, 90, 90, 60, 100],
        "SGST eligibility years":[10, 10, 10, 10, 20],
        "SGST max(%)":[6.5, 6.5, 6.5, 6, 0.9]
    },
    "C":{
        "Enterprise Size":["Micro","Small","Medium","Large", "Mega"],
        "Capital Subsidy(%)":[10, 0, 0, 4, 0],
        "Interest rate(%)":[5]*5, #cap 60%
        "Interest eligible years":[5, 5, 5, 6, 10],
        "Max interest": [2500000, 2500000, 2500000, 0, 0],
        "SGST reimbursement(%)":[80, 80, 80, 40, 100],
        "SGST eligibility years":[10, 10, 10, 10, 20],
        "SGST max(%)":[5, 5, 5, 4, 0.9]
    }
}

# Calculation logic
def calculate_subsidy(zone, enterprise_size, plant_machinery, building_civil_work, land_cost, term_loan_amount):

    zone_info = zone_data.get(zone)
    index = zone_info["Enterprise Size"].index(enterprise_size.strip().capitalize())
    enterprise_size = enterprise_size.strip().capitalize()
    
    capital_investment = plant_machinery + building_civil_work

    capital_subsidy = 0 
    stamp_duty_subsidy = 0 
    sgst_reimbursement = 0 
    interest_subsidy = 0 

    # Capital Subsidy (available for Micro & Mega)
    # Available only for enterprises 
    capital_subsidy_rate = zone_info["Capital Subsidy(%)"][index] 
    capital_subsidy = capital_subsidy_rate/100 * capital_investment

    #Sgst_reimbursement
    sgst_max_rate = (zone_info["SGST max(%)"][index])
    sgst_eligibility_years = (zone_info["SGST eligibility years"][index])
    sgst_reimbursement_max= capital_investment * (sgst_max_rate/100) * sgst_eligibility_years 
    sgst_rate = (zone_info["SGST reimbursement(%)"][index])

    sgst_amount = (sgst_rate/100) * capital_investment * sgst_eligibility_years 

    sgst_reimbursement = min(sgst_amount, sgst_reimbursement_max)

    # Stamp Duty Subsidy
    # Confirm this for Large
    if enterprise_size in ["Micro", "Small", "Medium", "Mega"]: #100% stamp duty
        stamp_duty_subsidy = land_cost * 0.07 
    else: 
        stamp_duty_subsidy = 0

    # Interest Subsidy 
    interest_eligibility_years = (zone_info["Interest eligible years"][index])
    interest_rate = (zone_info["Interest rate(%)"][index])

    total_interest =  (interest_rate/100) * term_loan_amount 

    if enterprise_size in ["Micro", "Small", "Medium"]:
        interest_subsidy = min(total_interest, (zone_info["Max interest"][index])) * interest_eligibility_years
    elif enterprise_size == "Mega":
        interest_subsidy = min (total_interest, 0.012 * capital_investment) * interest_eligibility_years #for Mega industries 1.2% of FCI 
    elif enterprise_size == "Large":
        interest_subsidy = min (total_interest, 0.01 * capital_investment) * interest_eligibility_years #for Large industries 1% of FCI 
    else:
        interest_subsidy = 0

    # Total subsidy 
    total_subsidy = capital_subsidy + sgst_reimbursement + stamp_duty_subsidy + interest_subsidy
        
    return {
        "capital_subsidy_rate": capital_subsidy_rate ,
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "sgst_reimbursement": round(sgst_reimbursement, 2),
        "sgst_rate": sgst_rate,
        "sgst_eligibility_years": sgst_eligibility_years,
        "sgst_max_rate": sgst_max_rate,
        "stamp_duty_subsidy":round(stamp_duty_subsidy,2),
        "interest_subsidy": round(interest_subsidy, 2),
        "interest_eligibility_years":interest_eligibility_years,
        "total_subsidy": round(total_subsidy, 2)
    }    

def process_gujarat(data):
    try:

        if "Enterprise Size" in data:
            enterprise_size = data["Enterprise Size"]
        else:
            raise ValueError("Missing 'Enterprise Size' in input data.")

        # Extract values
        subdistrict = data["Subdistrict"].strip().lower()
        enterprise_size = data["Enterprise Size"]
        plant_machinery = float(data["Plant and Machinery Investment"])
        building_civil_work = float(data["Building and Civil Work Investment"])
        land_cost = float(data.get("Land Cost",0))
        term_loan_amount = float(data.get(("Term Loan Amount"), 0))

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
            land_cost,
            term_loan_amount
        )

        # Generate report
        pdf_path = generate_report_gujarat(data, result, zone)

        return {
            "zone": zone,
            "subsidy_result": result,
            "report_path": pdf_path
        }

    except Exception as e:
        return {
            "error": f"Error processing Gujarat subsidy: {str(e)}"
        }