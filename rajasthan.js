import { rajasthanData } from './rajasthan_data.js';

export function renderForm(container) {
  container.innerHTML = `
    <h3>Fill your Details here</h3>

    <div class="form-group">
      <label for="rajasthanDistrict">District</label>
      <select id="rajasthanDistrict" name="District" required>
        <option value="">Select District</option>
        ${Object.keys(rajasthanData).map(d => `<option value="${d}">${d}</option>`).join("")}
      </select>
    </div>

    <div class="form-group">
      <label for="rajasthanSubdistrict">Subdistrict</label>
      <select id="rajasthanSubdistrict" name="Subdistrict" required>
        <option value="">Select Subdistrict</option>
      </select>
    </div>

    <div class="form-group">
      <label for="plantMachinery">Plant & Machinery Investment(Rs.)</label>
      <input type="number" id="plantMachinery" name="Plant and Machinery Investment" required>
    </div>

    <div class="form-group">
      <label for="buildingCivil">Building & Civil Work Investment(Rs.)</label>
      <input type="number" id="buildingCivil" name="Building and Civil Work Investment" required>
    </div>

    <div class="form-group" id="turnoverField">
      <label for="netTurnover">Net Turnover(Rs.)</label>
      <input type="number" id="netTurnover" name="Net Turnover">
    </div>

    <div class="form-group">
      <label for="termLoan">Term Loan Availed</label>
      <select id="termLoan" name="Term Loan Availed">
        <option value="">Select</option>
        <option value="Yes">Yes</option>
        <option value="No">No</option>
      </select>
    </div>

    <div class="form-group hidden" id="termloanAmount">
      <label for="termloanAmountInput">Term Loan Amount(Rs.)</label>
      <input type="number" id="termloanAmountInput" name="Term Loan Amount">
    </div>

  `;

  const districtSelect = container.querySelector("#rajasthanDistrict");
  const subdistrictSelect = container.querySelector("#rajasthanSubdistrict");
  const termLoan = container.querySelector("#termLoan");
  const termloanAmount = container.querySelector("#termloanAmount");

  districtSelect.addEventListener("change", () => {
    const selectedDistrict = districtSelect.value;
    const subdistricts = rajasthanData[selectedDistrict] || [];

    subdistrictSelect.innerHTML = `<option value="">Select Subdistrict</option>` +
      subdistricts.map(sd => `<option value="${sd.trim()}">${sd.trim()}</option>`).join("");
  });

  termLoan.addEventListener("change", () => {
    const isYes = termLoan.value === "Yes";
    termloanAmount.classList.toggle("hidden", !isYes);
    termloanAmount.querySelector("input").required = isYes;
  });

}
