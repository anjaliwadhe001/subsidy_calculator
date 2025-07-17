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
      <label for="enterpriseSize">Enterprise Size:</label>
      <select id="enterpriseSize" name="Enterprise Size" required>
        <option value="">Select</option>
        <option value="Micro">Micro</option>
        <option value="Small">Small</option>
        <option value="Medium">Medium</option>
        <option value="Large">Large</option>
        <option value="Mega">Mega</option>
        <option value="Ultra Mega">Ultra Mega</option>
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
      <select id="industryType" name="Industry Type" required>
        <option value="">Select</option>
        <option value="Plastic Alternatives">Plastic Alternatives</option>
        <option value="Agriculture processing">Agriculture processing</option>
        <option value="Food processing">Food processing</option>
        <option value="Other">Other</option>
      </select>
    </div>

    <div class="form-group hidden" id="turnoverField">
      <label for="netTurnover">Net Turnover:</label>
      <input type="number" id="netTurnover" name="Net Turnover">
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
      <label for="termloanAmountInput">Term Loan Amount:</label>
      <input type="number" id="termloanAmountInput" name="Term Loan Amount">
    </div>

    <div class="form-group">
      <label for="netsgstpaidcashLedger">Net SGST Cash Ledger:</label>
      <input type="number" id="netsgstpaidcashLedger" name="Net SGST Cash Ledger" required>
    </div>
  `;

  const districtSelect = container.querySelector("#rajasthanDistrict");
  const subdistrictSelect = container.querySelector("#rajasthanSubdistrict");
  const termLoan = container.querySelector("#termLoan");
  const termloanAmount = container.querySelector("#termloanAmount");
  const industryType = container.querySelector("#industryType");
  const enterpriseSize = container.querySelector("#enterpriseSize");
  const turnoverField = container.querySelector("#turnoverField");

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

  function updateTurnoverVisibility() {
    const type = industryType.value;
    const size = enterpriseSize.value;
    const needsTurnover = type === "Other" && ["Large", "Mega", "Ultra Mega"].includes(size);

    turnoverField.classList.toggle("hidden", !needsTurnover);
    turnoverField.querySelector("input").required = needsTurnover;
  }

  industryType.addEventListener("change", updateTurnoverVisibility);
  enterpriseSize.addEventListener("change", updateTurnoverVisibility);
}
