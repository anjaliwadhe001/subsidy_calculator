from flask import Flask, request, jsonify, send_file
import pandas as pd
from report import generate_pdf
from subsidy import process_subsidy_application
app = Flask(__name__)

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

# Clean calculation function (uses only passed parameters!)
def calculate_subsidy(zone, enterprise_size, plant_machinery, building_civil_work,
                      term_loan_amount, land_cost, net_sgst_paid_cash_ledger):

    zone_info = zone_df[zone_df["Zone"] == zone].iloc[0]
    enterprise_size = enterprise_size.strip().capitalize()
    capital_investment = plant_machinery + building_civil_work

    # Capital Subsidy (Micro & Small only)
    if enterprise_size in ["Micro", "Small"]:
        capital_subsidy = min(0.15 * capital_investment, 2000000)
    else:
        capital_subsidy = 0

    # Stamp Duty Subsidy
    stamp_duty_subsidy = zone_info["Stamp Duty (%)"] * (0.07 * land_cost)

    # Interest Subsidy
    annual_interest = term_loan_amount * (zone_info["Interest Rate (%)"] / 100)
    interest_subsidy = min(annual_interest, 2000000) * zone_info["Interest Years"]

    # SGST Reimbursement
    sgst_reimbursement = (
        net_sgst_paid_cash_ledger * (zone_info["SGST Initial (%)"] / 100) +
        net_sgst_paid_cash_ledger * (zone_info["SGST Extended (%)"] / 100)
    )

    return {
        "capital_investment_subsidy": round(capital_subsidy, 2),
        "stamp_duty_exemption": round(stamp_duty_subsidy, 2),
        "interest_subsidy": round(interest_subsidy, 2),
        "sgst_reimbursement": round(sgst_reimbursement, 2),
        "total_subsidy": round(capital_subsidy + stamp_duty_subsidy + interest_subsidy + sgst_reimbursement, 2)
    }

# API endpoint
@app.route("/calculate-subsidy", methods=["POST"])
def calculate():
    try:
        data = request.get_json(force=True)

        subdistrict = data.get("subdistrict", "").strip().lower()
        row = df[df["Subdistrict"] == subdistrict]
        if row.empty:
            return jsonify({"error": "Subdistrict not found."}), 400

        # Let process_subsidy_application handle calculation and PDF
        result = process_subsidy_application(data, df, zone_df, generate_pdf, calculate_subsidy)

        if "error" in result:
            return jsonify({"error": result["error"]}), 400

        # Return final generated PDF
        return send_file(
            result["pdf_path"],
            as_attachment=True,
            download_name="Final_Subsidy_Report.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
