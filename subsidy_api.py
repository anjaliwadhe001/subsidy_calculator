from flask import Flask, request, jsonify
import pandas as pd
from report import generate_pdf
from subsidy import process_subsidy_application

app = Flask(__name__)

# Zone Data
df = pd.read_csv("Zone_database.csv")
df.columns = df.columns.str.strip()
df['Subdistrict'] = df['Subdistrict'].str.strip().str.lower()

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

# Subsidy Calculation 
def calculate_subsidy(zone, enterprise_size, plant_machinery, building_civil_work,
                      term_loan_amount, land_cost, net_sgst_paid_cash_ledger):
    zone_info = zone_df[zone_df["Zone"] == zone].iloc[0]
    capital_investment = plant_machinery + building_civil_work

    capital_subsidy = 0
    if enterprise_size in ["Micro", "Small"]:
        capital_subsidy = min(0.15 * capital_investment, 2000000)

    stamp_duty_subsidy = zone_info["Stamp Duty (%)"] * (0.07 * land_cost)
    annual_interest = term_loan_amount * (zone_info["Interest Rate (%)"] / 100)
    interest_subsidy = min(annual_interest, 2000000) * zone_info["Interest Years"]

    sgst_reimbursement = (
        net_sgst_paid_cash_ledger * (zone_info["SGST Initial (%)"] / 100) +
        net_sgst_paid_cash_ledger * (zone_info["SGST Extended (%)"] / 100)
    )

    total_subsidy = capital_subsidy + stamp_duty_subsidy + interest_subsidy + sgst_reimbursement

    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "stamp_duty_exemption": round(stamp_duty_subsidy, 2),
        "interest_subsidy": round(interest_subsidy, 2),
        "sgst_reimbursement": round(sgst_reimbursement, 2),
        "total_subsidy": round(total_subsidy, 2)
    }

#API Endpoint 
@app.route("/calculate-subsidy", methods=["POST","HEAD","GET"])
def calculate():
    try:
        data = request.get_json(force=True)

        result = process_subsidy_application(data, df, zone_df, generate_pdf, calculate_subsidy)

        if "error" in result:
            return jsonify({"error": result["error"]}), 400

        return jsonify({
            "zone": result["zone"],
            "subsidy_breakup": result["subsidy_breakup"],
            "pdf_path": result["pdf_path"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
