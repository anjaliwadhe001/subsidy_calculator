#Subsidies apply only to investments made during the policy period (2022–2027). 
#Applicable to Micro, Small, Medium Industrial units
#User Interest rate is a new input 
import pandas as pd
from report_up_msme import generate_report_up_msme

# Load Zone Mapping Data
df = pd.read_csv("Uttar_Pradesh_zone.csv")
df.columns = df.columns.str.strip()
df['District'] = df['District'].str.strip().str.lower()

# Zone configuration
zone_data = {
    "A":{
    "Enterprise Size": ["Micro", "Small", "Medium"],
    "Stamp Duty": [0.50]*3,
    "Capital Investment Subsidy (%)": [20, 15, 10],
    "Eligibility Period for CIS": [2, 3, 4]
    },
    "B":{
    "Enterprise Size": ["Micro", "Small", "Medium"],
    "Stamp Duty": [0.75]*3,
    "Capital Investment Subsidy (%)": [20, 15, 10],
    "Eligibility Period for CIS": [2, 3, 4]
    }, 
    "C":{
    "Enterprise Size": ["Micro", "Small", "Medium"],
    "Stamp Duty": [1.00]*3,
    "Capital Investment Subsidy (%)": [25, 20, 15],
    "Eligibility Period for CIS": [2, 3, 4]
    }

}

# Subsidy calculation logic
def calculate_subsidy(zone, enterprise_size, plant_machinery, building_civil_work,
                      term_loan_amount, land_cost, interest_rate, ):
    
    zone_info = zone_data.get(zone)
    index = zone_info["Enterprise Size"].index(enterprise_size)
    enterprise_size = enterprise_size.strip().capitalize()

    capital_investment = plant_machinery + building_civil_work

    capital_subsidy = 0 
    stamp_duty_subsidy = 0 
    interest_subsidy = 0

    # Capital Subsidy (only for Micro and Small)
    capital_subsidy_rate = zone_info["Capital Investment Subsidy (%)"][index]
    capital_subsidy = min( (capital_subsidy_rate/100) * capital_investment, 40000000)

    # Stamp Duty Subsidy 
    stamp_duty_rate = 0.07
    stamp_duty_subsidy = (zone_info["Stamp Duty"][index]) * stamp_duty_rate * land_cost

    # Interest Subsidy
    if enterprise_size in ["Micro"]:
        annual_interest = ( interest_rate * term_loan_amount) #to be paid by customer
        interest_subsidy = min((annual_interest*0.50), 2500000) * 5 #applicable for 5 years 
    else:
        interest_subsidy=0

    #SGST reimbursement(Not applicable for MSME)

    # Total subsidy 
    total_subsidy = capital_subsidy + stamp_duty_subsidy + interest_subsidy


    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "stamp_duty_exemption": round(stamp_duty_subsidy, 2),
        "interest_subsidy": round(interest_subsidy, 2),
        "capital_subsidy_rate": capital_subsidy_rate,
        "total_subsidy": round(total_subsidy, 2)
    }

def process_up_msme(data):
    try:
        # Extract values
        district = data["District"].strip().lower()
        enterprise_size = data["Enterprise Size"]
        plant_machinery = float(data["Plant and Machinery Investment"])
        building_civil_work = float(data["Building and Civil Work Investment"])
        land_cost = float(data["Land Cost"])
        interest_rate = float(data["Interest rate(%)"])
        term_loan_amount = float(data["Term Loan Amount"])

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
            term_loan_amount,
            land_cost,
            interest_rate 
        )

        # Generate report
        pdf_path = generate_report_up_msme(data, result, zone)
        return {
            "zone": zone,
            "subsidy_result": result,
            "report_path": pdf_path
        }

    except Exception as e:
        return {
            "error": f"Error processing Uttarpradesh MSME Subsidy: {str(e)}"
        }