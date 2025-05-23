import pandas as pd

# Assume zone_df and df are already loaded or importable if modularizing.

def process_subsidy_application(data, df, zone_df, generate_pdf, calculate_subsidy):
    """
    Processes the subsidy application data and returns subsidy results and PDF report path.

    Args:
        data (dict): Input data simulating the JSON payload.
        df (pd.DataFrame): Subdistrict zone lookup DataFrame.
        zone_df (pd.DataFrame): Zone subsidy parameters DataFrame.
        generate_pdf_func (function): Function to generate PDF report.
        calculate_subsidy_func (function): Function to compute subsidy.

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

        # Collect user data for PDF
        user_data = {
            "Name": data.get("name"),
            "Organization Name": data.get("organization_name"),
            "State": data.get("state"),
            "District": data.get("district"),
            "Subdistrict": subdistrict.title(),
            "Enterprise Size": data.get("enterprise_size"),
            "Business Nature": data.get("buisness_nature"),
            "Industry Type": data.get("industry_type"),
            "Plant & Machinery": data.get("plant_machinery"),
            "Building & Civil Work": data.get("building_civil_work"),
            "Land Owned": data.get("land_owned"),
            "Land Owned by Legal Entity": data.get("land_owned_by_legal_entity"),
            "Loan Avail": data.get("loan_avail"),
            "Loan Tenure": data.get("loan_tenure"),
            "SGST Paid": data.get("net_sgst_paid_cash_ledger")
        }

        # Default zero values
        land_cost = 0.0
        term_loan_amount = 0.0

        if data.get("land_owned_by_legal_entity", "no").strip().lower() == "yes":
            land_cost = float(data.get("land_cost", 0.0))

        if data.get("loan_avail", "no").strip().lower() == "yes":
            term_loan_amount = float(data.get("term_loan_amount", 0.0))

        # Calculate subsidy
        result = calculate_subsidy_func(
            zone,
            data["enterprise_size"].capitalize(),
            float(data["plant_machinery"]),
            float(data["building_civil_work"]),
            term_loan_amount,
            land_cost,
            float(data["net_sgst_paid_cash_ledger"])
        )

        # Generate PDF report and get the path
        pdf_path = generate_pdf_func(user_data, result, zone)

        return {
            "zone": zone,
            "subsidy_breakup": result,
            "pdf_path": pdf_path
        }

    except Exception as e:
        return {"error": str(e)}

