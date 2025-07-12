export function renderForm(container) {
  container.innerHTML = `
    <h3>Uttar Pradesh Details</h3>
    <div class="form-group">
      <label for="upDistrict">District:</label>
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
      <label for="netsgstpaidcashLedger">Net SGST Cash Ledger:</label>
      <input type="number" id="netsgstpaidcashLedger" name="Net SGST Paid Cash Ledger" required>
    </div>
  `;
}
