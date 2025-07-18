#Subsidies apply only to investments made during the policy period (2022–2027). 
#Industrial Investment & Employment Promotion Policy 2022 (Applicable to  large, mega, super-mega, and ultra-mega industrial units)

import pandas as pd
from report_uttarpradesh import generate_report_up

# Load Zone Mapping Data
df = pd.read_csv("Uttar_Pradesh_zone.csv")
df.columns = df.columns.str.strip()
df['District'] = df['District'].str.strip().str.lower()

# Zone configuration
zone_data = { "Zone":["A","B","C"],
    "A": {
        "Enterprise Size": ["Large", "Mega", "Super Mega", "Ultra-Mega"],
        "Capital Investment Subsidy(%)": [10, 15, 20, 25],
        "Stamp Duty (%)": [0.50]*4,
        "SGST Reimbursement (%)": [100, 100, 100, 100],
        "SGST Eligible Years": [5, 10, 12, 15],
        "SGST Reimbursement Max (%)": [60, 70, 80, 90],
    },
    "B": {
        "Enterprise Size": ["Large", "Mega", "Super Mega", "Ultra-Mega"],
        "Capital Investment Subsidy(%)": [15, 20, 25, 30],
        "Stamp Duty (%)": [0.75]*4,
        "SGST Reimbursement (%)": [100, 100, 100, 100],
        "SGST Eligible Years": [5, 10, 12, 15],
        "SGST Reimbursement Max (%)": [60, 70, 80, 90],
    },
    "C": {
        "Enterprise Size": ["Large", "Mega", "Super Mega", "Ultra-Mega"],
        "Capital Investment Subsidy(%)": [20, 25, 30, 35],
        "Stamp Duty (%)": [1.00]*4,
        "SGST Reimbursement (%)": [100, 100, 100, 100],
        "SGST Eligible Years": [5, 10, 12, 15],
        "SGST Reimbursement Max (%)": [60, 70, 80, 90],
    }
   }

# Subsidy calculation logic
def calculate_subsidy(zone, enterprise_size, plant_machinery, building_civil_work,
                       land_cost,net_sgst_paid_cash_ledger):
    
    zone_info = zone_data.get(zone)
    index = zone_info["Enterprise Size"].index(enterprise_size)
    enterprise_size = enterprise_size.strip().capitalize()
    
    capital_investment = plant_machinery + building_civil_work

    capital_subsidy = 0 
    stamp_duty_subsidy = 0 
    sgst_reimbursement = 0

    # Capital Subsidy 
    capital_subsidy = (zone_info["Capital Investment Subsidy(%)"][index]/100) * capital_investment

    # Stamp Duty Subsidy 
    stamp_duty_subsidy = zone_info["Stamp Duty (%)"][index] * (0.07 * land_cost)

    # Interest Subsidy not applicable

    # SGST Reimbursement
    max_sgst = capital_investment * (zone_info["SGST Reimbursement Max (%)"][index] / 100)
    sgst_eligible_years = zone_info["SGST Eligible Years"][index]
    sgst_reimbursement = min(net_sgst_paid_cash_ledger, max_sgst) * (zone_info["SGST Eligible Years"][index])

    # Total subsidy 
    total_subsidy = capital_subsidy + sgst_reimbursement + stamp_duty_subsidy 


    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "stamp_duty_exemption": round(stamp_duty_subsidy, 2),
        "sgst_reimbursement": round(sgst_reimbursement,2),
        "sgst_eligible_years":sgst_eligible_years,
        "total_subsidy": round(total_subsidy, 2)
    }

def process_up(data):
    try:
        
        # Extract values
        district = data["District"].strip().lower()
        enterprise_size = data["Enterprise Size"]
        plant_machinery = float(data["Plant and Machinery Investment"])
        building_civil_work = float(data["Building and Civil Work Investment"])
        land_cost = float(data.get("Land Cost",0))
        net_sgst_paid_cash_ledger = float(data["Net SGST Paid Cash Ledger"])

        #Zone 
        zone_row = df[df['District'].str.lower() == district]
        if zone_row.empty:
            zone = "Unknown"
        else:
            zone = zone_row.iloc[0]["Zone"]
        
        result = calculate_subsidy(
            zone,
            enterprise_size,
            plant_machinery,
            building_civil_work,
            land_cost,
            net_sgst_paid_cash_ledger
        )

        # Generate report
        pdf_path = generate_report_up(data, result, zone)

        return {
            "zone": zone,
            "subsidy_result": result,
            "report_path": pdf_path
        }
    except Exception as e:
        return {
            "error": f"Error processing Uttarpradesh subsidy: {str(e)}"
        }