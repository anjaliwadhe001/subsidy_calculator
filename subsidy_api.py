from flask import Flask, request, jsonify, send_file 
from subsidy_rajasthan import process_rajasthan
from subsidy_haryana import process_haryana
from subsidy_up_msme import process_up_msme
from subsidy_uttarpradesh import process_up
from subsidy_madhyapradesh import process_madhyapradesh
from subsidy_karnataka import process_karnataka
from subsidy_tamilnadu import process_tamilnadu 
from subsidy_maharashtra import process_maharashtra
from subsidy_gujarat import process_gujarat
from subsidy_punjab import process_punjab
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#API Route for subsidy calculation
@app.route("/subsidy", methods=["POST"])
def calculate_subsidy():
    data = request.get_json(force=True)
    print('Received request', data)

    State = data.get("State")
    enterprise_size = data.get("Enterprise Size")

    if not State or not enterprise_size:
        return jsonify({"error": "Missing required fields in input"}), 400

    if State == "Rajasthan":
        result = process_rajasthan(data)
    elif State == "Haryana":
        result = process_haryana(data)
    elif State == "Uttar Pradesh": 
        if enterprise_size in ["Large", "Mega", "Ultra Mega", "Super Mega", "Ultra-Mega"]:
            result = process_up(data)
        elif enterprise_size in ["Micro", "Small", "Medium"]:
            result = process_up_msme(data)
    elif State == "Madhya Pradesh":
        result = process_madhyapradesh(data)
    elif State == "Karnataka":
        result = process_karnataka(data)
    elif State == "Tamil Nadu":
        result = process_tamilnadu(data)
    elif State == "Maharashtra":
        result = process_maharashtra(data)
    elif State == "Gujarat":
        result = process_gujarat(data)
    elif State == "Punjab":
        result = process_punjab(data)
    else:
        return jsonify({"error": f"Unsupported state selected: {State}"}), 400

    return jsonify(result)

#API Route for pdf download
@app.route("/download_pdf/<filename>", methods=["GET"])
def download_pdf(filename):
    pdf_dir = os.path.join(os.getcwd(), "reports")
    file_path = os.path.join(pdf_dir, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
  
