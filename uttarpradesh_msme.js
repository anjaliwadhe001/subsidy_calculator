export function renderForm(container) {
  container.innerHTML = `
    <h3>Uttar Pradesh Details</h3>
    <div class="form-group">
      <label for="upDistrict">District</label>
      <select name="District" id="District">
        <option value="Gautam Buddh Nagar">Gautam Buddh Nagar</option>
        <option value="Ghaziabad">Ghaziabad</option>
        <option value="Madhyanchal">Madhyanchal</option>
        <option value="Paschimanchal">Paschimanchal</option>
        <option value="Bundelkhand">Bundelkhand</option>
        <option value="Poorvanchal">Poorvanchal</option>
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

    <div class="form-group">
      <label for="landOwned">Is land owned by legal entity</label>
      <select id="landOwned" name="Land Owned By Legal Entity?" required>
        <option value="">Select</option>
        <option value="Yes">Yes</option>
        <option value="No">No</option>
      </select>
    </div>

    <div class="form-group hidden" id="landCostGroup">
      <label for="landCost">Land Cost(Rs.)</label>
      <input type="number" id="landCost" name="Land Cost">
    </div>

    <div class="form-group">
      <label for="termLoan">Term Loan Availed</label>
      <select id="termLoan" name="Term Loan Availed">
        <option value="">Select</option>
        <option value="Yes">Yes</option>
        <option value="No">No</option>
      </select>
    </div>

    <div class="form-group hidden" id="interestRateGroup">
      <label for="interestRate">Interest Rate (%)</label>
      <input type="number" id="interestRate" name="Interest Rate">
    </div>

    <div class="form-group hidden" id="termloanAmount">
      <label for="termloanAmount">Term Loan Amount(Rs.)</label>
      <input type="number" id="termloanAmountInput" name="Term Loan Amount">
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

  const landOwned = container.querySelector("#landOwned");
  const landCostGroup = container.querySelector("#landCostGroup");
  const landCostInput = landCostGroup.querySelector("input");

  landOwned.addEventListener("change", () => {
    const showLandCost = landOwned.value === "Yes";
    landCostGroup.classList.toggle("hidden", !showLandCost);
    landCostInput.required = showLandCost;
  });

}
