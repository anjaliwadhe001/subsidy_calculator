import { rajasthanData } from './rajasthan_data.js';

export function renderForm(container) {
  container.innerHTML = `
    <h3>Rajasthan Details</h3>

    <div class="form-group">
      <label for="rajasthanDistrict">District:</label>
      <select id="rajasthanDistrict" name="District" required>
        <option value="">Select District</option>
        ${Object.keys(rajasthanData).map(d => `<option value="${d}">${d}</option>`).join("")}
      </select>
    </div>

    <div class="form-group">
      <label for="rajasthanSubdistrict">Subdistrict:</label>
      <select id="rajasthanSubdistrict" name="Subdistrict" required>
        <option value="">Select Subdistrict</option>
      </select>
    </div>

    <div class="form-group">
      <label for="plantMachinery">Plant & Machinery Investment:</label>
      <input type="number" id="plantMachinery" name="Plant and Machinery Investment" required>
    </div>

    <div class="form-group">
      <label for="buildingCivil">Building & Civil Work Investment:</label>
      <input type="number" id="buildingCivil" name="Building and Civil Work Investment" required>
    </div>

    <div class="form-group">
      <label for="industryType">Industry Type:</label>
      <select id="industryType" id="industryType" name="Industry Type" required>
      <option value="">Select</option>
      <option value="Plastic Alternatives">Plastic Alternatives</option>
      <option value="Agriculture processing">Agriculture processing</option>
      <option value="Food processing">Food processing</option>
      <option value="Other">Other</option>
    </div>


    <div class="form-group">
      <label for="landOwned">Is land owned by legal entity?</label>
      <select id="landOwned" name="Land Owned By Legal Entity?" required>
        <option value="">Select</option>
        <option value="Yes">Yes</option>
        <option value="No">No</option>
      </select>
    </div>

    <div class="form-group hidden" id="landCostGroup">
      <label for="landCost">Land Cost:</label>
      <input type="number" id="landCost" name="Land Cost">
    </div>

    <div class="form-group">
      <label for="termLoan">Term Loan Availed?</label>
      <select id="termLoan" name="Term Loan Availed">
        <option value="">Select</option>
        <option value="Yes">Yes</option>
        <option value="No">No</option>
      </select>
    </div>

    <div class="form-group hidden" id="interestRateGroup">
      <label for="interestRate">Interest Rate (%):</label>
      <input type="number" id="interestRate" name="Interest Rate">
    </div>

    <div class="form-group hidden" id="termloanAmount">
      <label for="termloanAmount">Term Loan Amount:</label>
      <input type="number" id="termloanAmountInput" name="Term Loan Amount">
    </div>

    <div class="form-group">
      <label for="netsgstpaidcashLedger">Net SGST Cash Ledger:</label>
      <input type="number" id="netsgstpaidcashLedger" name="Net SGST Cash Ledger" required>
    </div>
  `;

  const termLoan = container.querySelector("#termLoan");
  const interestRateGroup = container.querySelector("#interestRateGroup");
  const termloanAmount = container.querySelector("#termloanAmount");

  termLoan.addEventListener("change", () => {
    const isYes = termLoan.value === "Yes";
    interestRateGroup.classList.toggle("hidden", !isYes);
    interestRateGroup.querySelector("input").required = isYes;

    termloanAmount.classList.toggle("hidden", !isYes);
    termloanAmount.querySelector("input").required = isYes;
  });

  const districtSelect = container.querySelector("#rajasthanDistrict");
  const subdistrictSelect = container.querySelector("#rajasthanSubdistrict");

  districtSelect.addEventListener("change", () => {
    const selectedDistrict = districtSelect.value;
    const subdistricts = rajasthanData[selectedDistrict] || [];

    subdistrictSelect.innerHTML = `<option value="">Select Subdistrict</option>` +
      subdistricts.map(sd => `<option value="${sd.trim()}">${sd.trim()}</option>`).join("");
  });

  const landOwned = container.querySelector("#landOwned");
  const landCostGroup = container.querySelector("#landCostGroup");
  const landCostInput = landCostGroup.querySelector("input");

  landOwned.addEventListener("change", () => {
    const showLandCost = landOwned.value === "Yes";
    landCostGroup.classList.toggle("hidden", !showLandCost);
    landCostInput.required = showLandCost;
  });
}
