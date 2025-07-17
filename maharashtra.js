import { maharashtraData } from './maharashtra_data.js';

export function renderForm(container) {
  container.innerHTML = `
    <h3>maharashtra Details</h3>

    <div class="form-group">
      <label for="maharashtraDistrict">District:</label>
      <select id="maharashtraDistrict" name="District" required>
        <option value="">Select District</option>
        ${Object.keys(maharashtraData).map(d => `<option value="${d}">${d}</option>`).join("")}
      </select>
    </div>

    <div class="form-group">
      <label for="maharashtraSubdistrict">Subdistrict:</label>
      <select id="maharashtraSubdistrict" name="Subdistrict" required>
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

    <div class="form-group hidden" id="termloanAmount">
      <label for="termloanAmount">Term Loan Amount:</label>
      <input type="number" id="termloanAmountInput" name="Term Loan Amount">
    </div>

    <div class="form-group">
      <label for="netsgstpaidcashLedger">Net SGST Paid Cash Ledger:</label>
      <input type="number" id="netsgstpaidcashLedger" name="Net SGST Paid Cash Ledger" required>
    </div>
  `;

  const termLoan = container.querySelector("#termLoan");
  const termloanAmount = container.querySelector("#termloanAmount");

  termLoan.addEventListener("change", () => {
    const isYes = termLoan.value === "Yes";
  
    termloanAmount.classList.toggle("hidden", !isYes);
    termloanAmount.querySelector("input").required = isYes;
  });

  const districtSelect = container.querySelector("#maharashtraDistrict");
  const subdistrictSelect = container.querySelector("#maharashtraSubdistrict");

  districtSelect.addEventListener("change", () => {
    const selectedDistrict = districtSelect.value;
    const subdistricts = maharashtraData[selectedDistrict] || [];

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
