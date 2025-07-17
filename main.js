import { renderForm as renderMP } from './madhyapradesh.js';
import { renderForm as renderPunjab } from './punjab.js';
import { renderForm as renderKarnataka } from './karnataka.js';
import { renderForm as renderHaryana } from './haryana.js';
import { renderForm as renderTamilnadu } from './tamilnadu.js';
import { renderForm as renderRajasthan } from './rajasthan.js';
import { renderForm as renderMaharashtra } from './maharashtra.js';
import { renderForm as renderGujarat } from './gujarat.js';
import { renderForm as renderUPMSME } from './uttarpradesh_msme.js';
import { renderForm as renderUP } from './uttarpradesh.js';

const stateSelect = document.querySelector("#state");
const stateFormArea = document.querySelector("#stateFormArea");
const form = document.querySelector("#subsidyForm");
const statusDiv = document.querySelector("#status");

function getSelectedEnterpriseSize() {
  return document.querySelector("#enterpriseSize").value;
}

stateSelect.addEventListener("change", () => {
  const state = stateSelect.value;
  const size = getSelectedEnterpriseSize();
  stateFormArea.innerHTML = "";

  try {
    if (state === "Madhya Pradesh") {
      renderMP(stateFormArea);
    } else if (state === "Uttar Pradesh") {
      const largeSizes = ["Large", "Mega", "Ultra Mega", "Super Mega"];
      if (largeSizes.includes(size)) {
        renderUP(stateFormArea);
      } else {
        renderUPMSME(stateFormArea);
      }
    } else if (state === "Punjab") {
      renderPunjab(stateFormArea);
    } else if (state === "Haryana") {
      renderHaryana(stateFormArea);
    } else if (state === "Tamil Nadu") {
      renderTamilnadu(stateFormArea);
    } else if (state === "Karnataka") {
      renderKarnataka(stateFormArea);
    } else if (state === "Maharashtra") {
      renderMaharashtra(stateFormArea);
    } else if (state === "Rajasthan") {
      renderRajasthan(stateFormArea);
    } else if (state === "Gujarat") {
      renderGujarat(stateFormArea);
    } else if (state === "Maharashtra"){
      renderMaharashtra(stateFormArea);
    } else {
      stateFormArea.innerHTML = `<p style="color:red;">No form available for ${state}</p>`;
    }
  } catch (err) {
    console.error("Render error:", err);
    stateFormArea.innerHTML = `<p style="color:red;">Something went wrong loading the form.</p>`;
  }
});

document.querySelector("#enterpriseSize").addEventListener("change", () => {
  if (stateSelect.value === "Uttar Pradesh") {
    stateSelect.dispatchEvent(new Event("change"));
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  statusDiv.innerHTML = "Processing...";

  const formData = new FormData(form);
  const data = {};
  for (let [key, value] of formData.entries()) {
    if (value !== "") data[key] = value;
  }

  console.log("Collected form data:", data);

  try {
    const response = await fetch("https://subsidy-calculator-1.onrender.com/subsidy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log("Result from API:", result);

    if (result.report_path) {
      const downloadUrl = result.report_path.startsWith("/")
        ? result.report_path
        : `/download_pdf/${result.report_path.split("/").pop()}`;
      statusDiv.innerHTML = `
        ✅ Report generated.<br>
        <a href="${downloadUrl}" target="_blank" download>Click to download PDF</a>`;
    } else {
      statusDiv.innerHTML = `❌ Error: ${result.error || "No report_path returned."}`;
      console.error("No report_path received. Full result:", result);
    }
  } catch (err) {
    console.error("Fetch error:", err);
    statusDiv.innerHTML = "❌ Something went wrong. See console.";
  }
});
