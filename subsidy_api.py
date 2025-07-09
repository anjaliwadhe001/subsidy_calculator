from flask import Flask, request, jsonify, send_file
#from subsidy_rajasthan import process_rajasthan
#from subsidy_haryana import process_haryana
#from subsidy_up_msme import process_up_msme
#from subsidy_uttarpradesh import process_up
from subsidy_madhyapradesh import process_madhyapradesh
#from subsidy_karnataka import process_karnataka
#from subsidy_tamilnadu import process_tamilnadu 
#from subsidy_maharashtra import process_maharashtra
#from subsidy_gujarat import process_gujarat
#from subsidy_punjab import process_punjab
import os

app = Flask(__name__)

@app.route("/subsidy", methods=["POST"])
def calculate_subsidy():
    data = request.get_json(force=True)
    State = data.get("State")
    enterprise_size = data.get("Enterprise size")

    if not State or not enterprise_size:
        return jsonify({"error": "Missing required fields in input"}), 400

    if State == "Rajasthan":
        result = process_rajasthan(data)
    elif State == "Haryana":
        result = process_haryana(data)
    elif State == "Uttarpradesh": 
        if enterprise_size in ["Large", "Mega", "Ultra Mega", "Super Mega", "Ultra-Mega"]:
            result = process_up(data)
        elif enterprise_size in ["Micro", "Small", "Medium"]:
            result = process_up_msme(data)
    elif State == "Madhyapradesh":
        result = process_madhyapradesh(data)
    elif State == "Karnataka":
        result = process_karnataka(data)
    elif State == "Tamilnadu":
        result = process_tamilnadu(data)
    elif State == "Maharashtra":
        result = process_maharashtra(data)
    elif State == "Gujarat":
        result = process_gujarat(data)
    elif State == "Punjab":
        result = process_punjab(data)
    else:
        return jsonify({"error": "Unsupported state selected"}), 400

    return jsonify(result)

@app.route("/download_pdf/<filename>", methods=["GET"])
def download_pdf(filename):
    path = os.path.join(os.getcwd(), filename)
    return send_file(
        path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )
if __name__ == "__main__":
    app.run(debug=True)
