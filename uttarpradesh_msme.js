export function renderForm(container) {
  container.innerHTML = `
    <h3>Uttar Pradesh Details</h3>
    <div class="form-group">
      <label for="upmsmeDistrict">District:</label>
      <input type="text" id="upmsmeDistrict" name="District" required>
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
      <label for="landCost">Land Cost:</label>
      <input type="number" id="landCost" name="Land Cost" required>
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
      <input type="number" id="termloanAmount" name="termloanAmount">
    </div>
  `;

  const termLoan = container.querySelector("#termLoan");
  const interestRateGroup = container.querySelector("#interestRateGroup");
  const termloanAmount = container.querySelector("#termloanAmount");

  termLoan.addEventListener("change", () => {
    if (termLoan.value === "Yes") {
      interestRateGroup.classList.remove("hidden");
      interestRateGroup.querySelector("input").required = true;
      
      termloanAmount.classList.remove("hidden");
      document.getElementById("TermLoanAmount").setAttribute("required", "true");
    } else {
      interestRateGroup.classList.add("hidden");
      interestRateGroup.querySelector("input").required = false;

      termloanAmount.classList.add("hidden");
      document.getElementById("TermLoanAmount").removeAttribute("required");
    }
  });
}
