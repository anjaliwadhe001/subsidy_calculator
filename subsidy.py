import pandas as pd
from report import generate_pdf

def process_subsidy_application(data, df, zone_df, generate_pdf, subsidy_haryana):
    """
    Processes the subsidy application data and returns subsidy results and PDF report path.

    Args:
        data (dict): Input data simulating the JSON payload.
        df (pd.DataFrame): Subdistrict zone lookup DataFrame.
        zone_df (pd.DataFrame): Zone subsidy parameters DataFrame.
        generate_pdf (function): Function to generate PDF report.
        calculate_subsidy (function): Function to compute subsidy.

    Returns:
        dict: {
            "zone": str,
            "subsidy_breakup": dict,
            "pdf_path": str,
            "error": str (optional)
        }
    """
    try:
        subdistrict = data.get("subdistrict", "").strip().lower()
        row = df[df["Subdistrict"] == subdistrict]
        if row.empty:
            return {"error": "Subdistrict not found."}

        zone = row.iloc[0]["Zone"]

        # Default values
        land_cost = 0.0
        term_loan_amount = 0.0

        if data.get("land_owned_by_legal_entity", "no").strip().lower() == "yes":
            land_cost = float(data.get("land_cost", 0.0))

        if data.get("loan_avail", "no").strip().lower() == "yes":
            term_loan_amount = float(data.get("term_loan_amount", 0.0))
            loan_tenure = data.get("loan_tenure", "N/A")
        else:
            loan_tenure = "N/A"

        # Create user_data dictionary for PDF
        user_data = {
            "Name": data.get("name"),
            "Organization Name": data.get("organization_name"),
            "State": data.get("state"),
            "District": data.get("district"),
            "Subdistrict": subdistrict.title(),
            "Enterprise Size": data.get("enterprise_size"),
            "Business Nature": data.get("business_nature"),
            "Capital investment": float(data.get("plant_machinery", 0)) + float(data.get("building_civil_work", 0)),
            "Industry Type": data.get("industry_type"),
            "Plant & Machinery": data.get("plant_machinery"),
            "Building & Civil Work": data.get("building_civil_work"),
            "Land Owned by Legal Entity": data.get("land_owned_by_legal_entity"),
            "Loan Avail": data.get("loan_avail"),
            "Loan Tenure": loan_tenure,
            "SGST Paid": data.get("net_sgst_paid_cash_ledger")
        }

        # Calculate subsidy
        result = subsidy_haryana(
            zone,
            data["enterprise_size"].capitalize(),
            float(data["plant_machinery"]),
            float(data["building_civil_work"]),
            term_loan_amount,
            land_cost,
            float(data["net_sgst_paid_cash_ledger"])
        )

        zone_data = zone_df[zone_df["Zone"] == zone].iloc[0].to_dict()

        # Generate PDF report
        pdf_path = generate_pdf(user_data, result, zone, zone_data)

        return {
            "zone": zone,
            "subsidy_breakup": result,
            "pdf_path": pdf_path,
        }

    except Exception as e:
        return {"error": str(e)}
