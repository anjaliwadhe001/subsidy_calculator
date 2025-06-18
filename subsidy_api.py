from flask import Flask, request, jsonify, send_file, send_from_directory
import pandas as pd
from report import generate_pdf
from subsidy import process_subsidy_application
from flask_cors import CORS
import os
from pathlib import Path

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Load Zone Mapping Data
df = pd.read_csv("Haryana_subdistrict_zone.csv")
df.columns = df.columns.str.strip()
df['Subdistrict'] = df['Subdistrict'].str.strip().str.lower()

# Static zone configuration
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

# Subsidy calculation function
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

# API route to process data and return JSON with public PDF link
@app.route("/calculate-subsidy", methods=["POST"])
def calculate():
    try:
        data = request.get_json(force=True)

        # Process and generate PDF report
        result = process_subsidy_application(
            data, df, zone_df, generate_pdf, calculate_subsidy
        )

        if "error" in result:
            return jsonify({"error": result["error"]}), 400

        # Ensure static directory exists
        static_dir = Path("static")
        static_dir.mkdir(exist_ok=True)

        # Save PDF into static folder
        pdf_filename = "Subsidy_Calculation_Report.pdf"
        new_pdf_path = static_dir / pdf_filename
        os.replace(result["pdf_path"], new_pdf_path)

        return jsonify({
            "zone": result["zone"],
            "subsidy_breakup": result["subsidy_breakup"],
            "pdf_path": f"https://thescpl.in/static/{pdf_filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve static files manually (in case Flask is not auto-configured to serve them)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route("/", methods=["GET"])
def home():
    return "Subsidy Calculator backend is running"

if __name__ == "__main__":
    app.run(debug=True)
