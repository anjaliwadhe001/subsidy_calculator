
export function renderForm(container) {
  container.innerHTML = `
    <h3>Fill your Details here</h3>

    <div class="form-group">
      <label for="tamilnaduDistrict">District</label>
      <select id="tamilnaduDistrict" name="District" required>
        <option value="">Select District</option>
        <option value="Chengalpattu">Chengalpattu</option>
        <option value="Chennai">Chennai</option>
        <option value="Kancheepuram">Kancheepuram</option>
        <option value="Tiruvallur">Tiruvallur</option>
        <option value="Coimbatore">Coimbatore</option>
        <option value="Erode">Erode</option>
        <option value="Karur">Karur</option>
        <option value="Krishnagiri">Krishnagiri</option>
        <option value="Namakkal">Namakkal</option>
        <option value="The Nilgiris">The Nilgiris</option>
        <option value="Ranipet">Ranipet</option>
        <option value="Salem">Salem</option>
        <option value="Tiruchirappalli">Tiruchirappalli</option>
        <option value="Tirupattur">Tirupattur</option>
        <option value="Tiruppur">Tiruppur</option>
        <option value="Vellore">Vellore</option>
        <option value="Ariyalur">Ariyalur</option>
        <option value="Cuddalore">Cuddalore</option>
        <option value="Dharmapuri">Dharmapuri</option>
        <option value="Dindigul">Dindigul</option>
        <option value="Kallakurichi">Kallakurichi</option>
        <option value="Kanniyakumari">Kanniyakumari</option>
        <option value="Madurai">Madurai</option>
        <option value="Mayiladuthurai">Mayiladuthurai</option>
        <option value="Nagapattinam">Nagapattinam</option>
        <option value="Perambalur">Perambalur</option>
        <option value="Pudukkottai">Pudukkottai</option>
        <option value="Ramanathapuram">Ramanathapuram</option>
        <option value="Sivagangai">Sivagangai</option>
        <option value="Tenkasi">Tenkasi</option>
        <option value="Thanjavur">Thanjavur</option>
        <option value="Theni">Theni</option>
        <option value="Thiruvarur">Thiruvarur</option>
        <option value="Thoothukudi">Thoothukudi</option>
        <option value="Tirunelveli">Tirunelveli</option>
        <option value="Tiruvannamalai">Tiruvannamalai</option>
        <option value="Villupuram">Villupuram</option>
        <option value="Virudhunagar">Virudhunagar</option>
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
