export function renderForm(container) {
  container.innerHTML = `
    <h3>Fill your Details here</h3>
    
    <div class="form-group">
      <label for="punjabDistrict">District:</label>
      <select name="District" id="punjabDistrict" required>
        <option value="">Select District</option>
        <option value="Amritsar">Amritsar</option>
        <option value="Barnala">Barnala</option>
        <option value="Bathinda">Bathinda</option>
        <option value="Faridkot">Faridkot</option>
        <option value="Fatehgarh Sahib">Fatehgarh Sahib</option>
        <option value="Firozpur">Firozpur</option>
        <option value="Fazilka">Fazilka</option>
        <option value="Gurdaspur">Gurdaspur</option>
        <option value="Hoshiarpur">Hoshiarpur</option>
        <option value="Jalandhar">Jalandhar</option>
        <option value="Kapurthala">Kapurthala</option>
        <option value="Ludhiana">Ludhiana</option>
        <option value="Mansa">Mansa</option>
        <option value="Moga">Moga</option>
        <option value="Sri Muktsar Sahib">Sri Muktsar Sahib</option>
        <option value="Pathankot">Pathankot</option>
        <option value="Patiala">Patiala</option>
        <option value="Rupnagar">Rupnagar</option>
        <option value="Sahibzada Ajit Singh Nagar">Sahibzada Ajit Singh Nagar</option>
        <option value="Sangrur">Sangrur</option>
        <option value="Shahid Bhagat Singh Nagar">Shahid Bhagat Singh Nagar</option>
        <option value="Tarn Taran">Tarn Taran</option>
        <option value="Malerkotla">Malerkotla</option>
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
      <select id="termLoan" name="Term Loan Availed" required>
        <option value="">Select</option>
        <option value="Yes">Yes</option>
        <option value="No">No</option>
      </select>
    </div>

    <div class="form-group hidden" id="termLoanAmountGroup">
      <label for="termLoanAmount">Term Loan Amount:</label>
      <input type="number" id="termLoanAmount" name="Term Loan Amount">
    </div>

    <div class="form-group">
      <label for="netsgstpaidcashLedger">Net SGST Paid Cash Ledger:</label>
      <input type="number" id="netsgstpaidcashLedger" name="Net SGST Paid Cash Ledger" required>
    </div>
  `;

  // Handle Term Loan logic
  const termLoan = container.querySelector("#termLoan");
  const termLoanAmountGroup = container.querySelector("#termLoanAmountGroup");
  const termLoanAmountInput = container.querySelector("#termLoanAmount");

  termLoan.addEventListener("change", () => {
    const showLoanAmount = termLoan.value === "Yes";
    termLoanAmountGroup.classList.toggle("hidden", !showLoanAmount);
    termLoanAmountInput.required = showLoanAmount;
  });

  // Handle Land Cost logic
  const landOwned = container.querySelector("#landOwned");
  const landCostGroup = container.querySelector("#landCostGroup");
  const landCostInput = container.querySelector("#landCost");

  landOwned.addEventListener("change", () => {
    const showLandCost = landOwned.value === "Yes";
    landCostGroup.classList.toggle("hidden", !showLandCost);
    landCostInput.required = showLandCost;
  });
}
