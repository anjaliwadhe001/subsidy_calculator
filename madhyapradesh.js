export function renderForm(container) {
  container.innerHTML = `
    <h3>Fill your Details here</h3>
    <div class="form-group">
      <label for="mpDistrict">District</label>
      <select name="District" id="District">
            <option value="Indore">Indore</option>
            <option value="Bhopal">Bhopal</option>
            <option value="Jabalpur">Jabalpur</option>
            <option value="Gwalior">Gwalior</option>
            <option value="Ujjain">Ujjain</option>
            <option value="Rewa">Rewa</option>
            <option value="Satna">Satna</option>
            <option value="Sagar">Sagar</option>
            <option value="Dewas">Dewas</option>
            <option value="Ratlam">Ratlam</option>
            <option value="Mandsaur">Mandsaur</option>
            <option value="Khargone">Khargone</option>
            <option value="Khandwa">Khandwa</option>
            <option value="Chhindwara">Chhindwara</option>
            <option value="Betul">Betul</option>
            <option value="Sehore">Sehore</option>
            <option value="Vidisha">Vidisha</option>
            <option value="Morena">Morena</option>
            <option value="Bhind">Bhind</option>
            <option value="Shivpuri">Shivpuri</option>
            <option value="Guna">Guna</option>
            <option value="Katni">Katni</option>
            <option value="Damoh">Damoh</option>
            <option value="Chhatarpur">Chhatarpur</option>
            <option value="Shahdol">Shahdol</option>
            <option value="Singrauli">Singrauli</option>
            <option value="Seoni">Seoni</option>
            <option value="Balaghat">Balaghat</option>
            <option value="Barwani">Barwani</option>
            <option value="Jhabua">Jhabua</option>
      </select>
    </div>
    
    <label>Plant and Machinery Investment(Rs.)
      <input type="number" name="Plant and Machinery Investment" required>
    </label><br>

    <label>Building and Civil Work Investment(Rs.)
      <input type="number" name="Building and Civil Work Investment" required>
    </label><br>

    <label>Is Term Loan Availed
      <select name="Is Term Loan Availed?" id="termLoanSelectMP" required>
        <option value="">Select</option>
        <option value="Yes">Yes</option>
        <option value="No">No</option>
      </select>
    </label><br>

    <div id="loanFieldsMP" style="display:none;">
      <label>Term Loan Amount(Rs.)
        <input type="number" name="Term Loan Amount" step="0.01">
      </label><br>

      <label>Interest Rate (%)
        <input type="number" name="Interest Rate" step="0.01">
      </label><br>
    </div>
  `;

  const termLoanSelect = container.querySelector("#termLoanSelectMP");
  const loanFields = container.querySelector("#loanFieldsMP");

  termLoanSelect.addEventListener("change", () => {
    if (termLoanSelect.value === "Yes") {
      loanFields.style.display = "block";
    } else {
      loanFields.style.display = "none";
    }
  });
}
