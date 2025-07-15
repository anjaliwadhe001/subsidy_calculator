import pandas as pd
from report_karnataka import generate_report_karnataka

# Load Zone Mapping Data
df = pd.read_csv("Karnataka_subdistrict_zone.csv") 
df.columns = df.columns.str.strip()
df['Subdistrict'] = df['Subdistrict'].str.strip().str.lower()

# Zone data
zone_data = {
    "A":{
        "Enterprise Size":["Micro","Small","Medium","Large", "Mega","Ultra-Mega"],
        "Capital Subsidy(%)":[30, 25, 20, 25, 25, 25],
        "PLI(%)":[2.5]*6, #cap 60%
        "Stamp Duty(%)": [100]*6,
    },
    "B":{
        "Enterprise Size":["Micro","Small","Medium","Large", "Mega","Ultra-Mega"],
        "Capital Subsidy(%)":[25, 20, 15, 20, 20, 20],
        "PLI(%)":[2.0]*6, #cap 60%
        "Stamp Duty(%)": [100]*6,
    },
    "C":{
        "Enterprise Size":["Micro","Small","Medium","Large", "Mega","Ultra-Mega"],
        "Capital Subsidy(%)":[10, 10, 5, 10, 10, 10],
        "PLI(%)":[1.0]*6, #cap 60%
        "Stamp Duty(%)": [75]*6,
    }
}

# Calculation logic
def calculate_subsidy(zone, enterprise_size, plant_machinery, building_civil_work, turn_over, land_cost, 
                      term_loan_amount):

    zone_info = zone_data.get(zone)
    index = zone_info["Enterprise Size"].index(enterprise_size.strip().capitalize())
    enterprise_size = enterprise_size.strip().capitalize()
    capital_investment = plant_machinery + building_civil_work

    capital_subsidy = 0
    interest_subsidy = 0 
    stamp_duty_subsidy = 0 
    sgst_reimbursement = 0

    # Capital Subsidy 
    capital_subsidy =(zone_info[ "Capital Subsidy(%)"][index] /100)* capital_investment

    # Production linked incentives PLI

    sgst_rate = (zone_info["PLI(%)"][index])
    sgst_amount = (sgst_rate/100) * turn_over  

    if zone in ["A","B"]:
        #eligible for 7 years 
        sgst_reimbursement = min(sgst_amount, 0.60 * capital_investment) * 7
    else:
        sgst_reimbursement = min(sgst_amount, 0.30 * capital_investment) * 7 #cap for zone C is 30%

    # Stamp Duty Subsidy
    stamp_duty_subsidy = (zone_info["Stamp Duty(%)"][index]/100) * land_cost * 0.07 

    # Interest Subsidy 
    # Interest subsidy is applicable only in Zona A and Zona B for Small, Medium and Micro Enterprises
    if enterprise_size in ["Small", "Medium", "Micro"] and zone in["A","B"]:
        interest_subsidy =  0.05 * term_loan_amount * 5 #Eligible for 5 years
    else: 
        interest_subsidy = 0 

    #Total Subsidy
    total_subsidy = capital_subsidy + sgst_reimbursement + stamp_duty_subsidy + interest_subsidy

    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "interest_subsidy": round(interest_subsidy, 2),
        "sgst_reimbursement": round(sgst_reimbursement, 2),
        "stamp_duty_subsidy":round(stamp_duty_subsidy,2),
        "total_subsidy": round(total_subsidy, 2)
    }    

def process_karnataka(data):
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
        turn_over = float(data["Net Turnover"])
        land_cost = float(data.get("Land Cost", 0))
        term_loan_amount = float(data.get("Term Loan Amount", 0))
        

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
            turn_over,
            land_cost,
            term_loan_amount
        )

        # Generate report
        pdf_path = generate_report_karnataka(data, result, zone)

        return {
            "zone": zone,
            "subsidy_result": result,
            "report_path": pdf_path
        }

    except Exception as e:
        return {
            "error": f"Error processing Karnataka subsidy: {str(e)}"
        }