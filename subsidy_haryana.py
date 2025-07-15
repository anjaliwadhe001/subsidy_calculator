import pandas as pd
from report_haryana import generate_report_haryana

# Load Zone Mapping Data
df = pd.read_csv("Haryana_subdistrict_zone.csv")
df.columns = df.columns.str.strip()
df['Subdistrict'] = df['Subdistrict'].str.strip().str.lower()

# Zone data
zone_data = {
    "Zone": ["A", "B", "C", "D"],
    "SGST Initial (%)": [50, 60, 70, 75],
    "SGST Initial Years": [5, 7, 8, 10],
    "SGST Extended (%)": [25, 30, 30, 35],
    "SGST Extended Years": [3, 3, 3, 3],
    "Stamp Duty (%)": [0, 0.60, 0.75, 1.00],
    "Interest Rate (%)": [5, 5, 6, 6],
    "Interest Years": [5, 5, 7, 7],
    "Capital Investment Subsidy": [15] * 4,
    "Max Investment Subsidy (Rs.)": [2000000] * 4,
    "Max Interest/Year (Rs.)": [2000000] * 4
}
zone_df = pd.DataFrame(zone_data)

# Calculation
def calculate_subsidy(zone, enterprise_size, plant_machinery, building_civil_work,land_cost,
                      term_loan_amount, net_sgst_paid_cash_ledger):

    zone_info = zone_df[zone_df["Zone"] == zone].iloc[0]
    enterprise_size = enterprise_size.strip().capitalize()
    capital_investment = plant_machinery + building_civil_work
    print("Capital investment", capital_investment)

    # Capital Subsidy (Micro & Small only)
    if enterprise_size in ["Micro", "Small"]:
        capital_subsidy = min(0.15 * capital_investment, 2000000)
    else:
        capital_subsidy = 0

    print("Capital subsidy", capital_subsidy)

    # Stamp Duty Subsidy 
    stamp_duty_rate = zone_info["Stamp Duty (%)"].item()
    stamp_duty_subsidy = stamp_duty_rate * (0.07 * land_cost)
    print("Stamp Duty: ", stamp_duty_subsidy)

    # Interest Subsidy 
    interest_rate_percent = zone_info["Interest Rate (%)"].item()
    interest_years = zone_info["Interest Years"].item()

    if enterprise_size in ["Micro", "Small"]:
        annual_interest = term_loan_amount * (interest_rate_percent / 100)
        interest_subsidy = min(annual_interest, 2000000) * interest_years
    else:
        interest_subsidy = 0 
    print("Interest Subsidy", interest_subsidy)
    
    # SGST Reimbursement
    sgst_initial_percent = zone_info["SGST Initial (%)"].item()
    sgst_extended_percent = zone_info["SGST Extended (%)"].item()

    sgst_reimbursement = (
        net_sgst_paid_cash_ledger * (sgst_initial_percent / 100) +
        net_sgst_paid_cash_ledger * (sgst_extended_percent / 100)
    )
    # Total subsidy
    total_subsidy = capital_subsidy + sgst_reimbursement + stamp_duty_subsidy + interest_subsidy

    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "stamp_duty_exemption": round(stamp_duty_subsidy, 2),
        "interest_subsidy": round(interest_subsidy, 2),
        "sgst_reimbursement": round(sgst_reimbursement, 2),
        "total_subsidy": round(total_subsidy, 2)
    }
def safe_float(value):
    try:
        return float(str(value).replace(",", "").replace("Rs.", "").strip())
    except:
        return 0.0

def process_haryana(data):
    try:
        if "Enterprise Size" in data:
            enterprise_size = data["Enterprise Size"]
        else:
            raise ValueError("Missing 'Enterprise Size' in input data.")

        subdistrict = data["Subdistrict"].strip().lower()
        plant_machinery = safe_float(data["Plant and Machinery Investment"])
        building_civil_work = safe_float(data["Building and Civil Work Investment"])
        land_cost = safe_float(data.get("Land Cost",0))
        term_loan_amount = safe_float(data.get(["Term Loan Amount"],0))
        net_sgst_paid_cash_ledger = safe_float(data["Net SGST Paid Cash Ledger"])

        # Zone lookup
        zone_row = df[df['Subdistrict'].str.lower() == subdistrict]
        if zone_row.empty:
            zone = "Unknown" 
            return {"error": f"Subdistrict '{subdistrict}' not found in zone mapping."}
        else:
            zone = zone_row.iloc[0]["Zone"]

        # Perform calculations
        result = calculate_subsidy(
            zone,
            enterprise_size,
            plant_machinery,
            building_civil_work,
            land_cost,
            term_loan_amount,
            net_sgst_paid_cash_ledger
        )
        # Generate report
        pdf_path = generate_report_haryana(data, result, zone, zone_df[zone_df["Zone"] == zone].iloc[0])

        return {
            "zone": zone,
            "subsidy_result": result,
            "report_path": pdf_path
        }

    except Exception as e:
        return {
            "error": f"Error processing Haryana subsidy: {str(e)}"
        }