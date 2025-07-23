import pandas as pd
from report_maharashtra import generate_report_maharashtra

# Load Zone Mapping Data
df = pd.read_csv("Maharashtra_zone.csv") 
df.columns = df.columns.str.strip()
df['Subdistrict'] = df['Subdistrict'].str.strip().str.lower()

# Zone data
zone_data = {

    "Zone": ["A", "B","C","D","D+"], 
     #Zone A- Industrially developed areas (including Greater Mumbai) 
     #Zone B- Developed
     #Zone C- Moderately Developed
     #Zone D- Less Developed
     #Zone D+- Least Developed

    "Capital Subsidy Rate": [0, 30, 40, 50, 60],
    "SGST Eligible years": [0, 7, 7, 10, 10],
    "Interest rate":[0, 5, 5, 5, 5],
    "Interest eligibility years":[0, 7, 7, 10, 10]
}
zone_df = pd.DataFrame(zone_data)

# Calculation logic
def calculate_subsidy(zone, plant_machinery, building_civil_work, land_cost,
                      term_loan_amount):

    zone_info = zone_df[zone_df["Zone"] == zone].iloc[0]
    
    capital_investment = plant_machinery + building_civil_work

    capital_subsidy = 0 
    stamp_duty_waive_off = 0 
    interest_subsidy = 0 
    sgst_reimbursement = 0 

    # Capital Subsidy and SGST Reimbursement for Zone A
    capital_subsidy = (zone_info["Capital Subsidy Rate"]/100) * capital_investment 
    
    # Stamp Duty Subsidy 
    if zone in ["A", "B"]:
        stamp_duty_waive_off = 0
    else:
        stamp_duty_waive_off = 0.07 * land_cost

    # Interest Subsidy
    interest_subsidy = term_loan_amount * (zone_info["Interest rate"]/100) * (zone_info["Interest eligibility years"])

    # SGST Reimbursement
    capital_subsidy_per_year = capital_subsidy / (zone_info["SGST Eligible years"])
    capital_investment_per_year = capital_investment / (zone_info["SGST Eligible years"])
    sgst_reimbursement = min(capital_subsidy_per_year, capital_investment_per_year) * (zone_info["SGST Eligible years"])

    # Total subsidy 
    total_subsidy = capital_subsidy + sgst_reimbursement + stamp_duty_waive_off + interest_subsidy

    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "stamp_duty_waive_off":round(stamp_duty_waive_off,2),
        "interest_subsidy": round(interest_subsidy, 2),
        "sgst_reimbursement": round(sgst_reimbursement, 2),
        "total_subsidy": round(total_subsidy, 2)
    }    

def process_maharashtra(data):
    try:        
        # Extract values
        subdistrict = data["Subdistrict"].strip().lower()
        plant_machinery = float(data["Plant and Machinery Investment"])
        building_civil_work = float(data["Building and Civil Work Investment"])
        land_cost = float(data.get("Land Cost",0))
        term_loan_amount = float(data.get("Term Loan Amount",0))
        

        # Zone lookup
        zone_row = df[df['Subdistrict'].str.lower() == subdistrict]
        if zone_row.empty:
            zone = "Unknown"
        else:
            zone = zone_row.iloc[0]["Zone"]

        # Perform calculations
        result = calculate_subsidy(
            zone,
            plant_machinery,
            building_civil_work,
            land_cost,
            term_loan_amount,
        )
        
        # Generate report
        pdf_path = generate_report_maharashtra(data, result, zone)

        return {
            "zone": zone,
            "subsidy_result": result,
            "report_path": pdf_path
        }

    except Exception as e:
        return {
            "error": f"Error processing Maharashtra subsidy: {str(e)}"
        }