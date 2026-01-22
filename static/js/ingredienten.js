document.addEventListener("DOMContentLoaded", function () {
              
  const selector = document.getElementById("personen-selector");
  if (!selector) return;

  const basePersons = parseInt(selector.dataset.basePersons, 10);
  const ingredienten = document.querySelectorAll("#ingredienten-lijst li");
  const pdfLink = document.getElementById("pdf-download");
              
  function formatHoeveelheid(amount, unit) {

    amount = Number(amount);

    if (Number.isNaN(amount)) return "";
              
    // stuks afronden     
    if (unit === "st") {  
      return Math.round(amount);
    }         
              
    if (Number.isInteger(amount)) {
            return amount.toString();
    }

    const whole = Math.floor(amount);
    const fraction = amount - whole;
              
    const fractions = [   
      { value: 0.75, symbol: "¾" },
      { value: 0.66, symbol: "⅔" },
      { value: 0.5,  symbol: "½" },
      { value: 0.33, symbol: "⅓" },
      { value: 0.25, symbol: "¼" },
    ];        
              
    let fracSymbol = "";  
    for (const f of fractions) {
      if (Math.abs(fraction - f.value) < 0.08) {
        fracSymbol = f.symbol;
        break;            
      }       
    }         
              
    if (whole === 0 && fracSymbol) return fracSymbol;
    if (whole > 0 && fracSymbol) return `${whole}${fracSymbol}`;
              
    // fallback: 1 decimaal, NL-notatie
    return amount.toFixed(1).replace(".", ",");
  }           
  
  // 👉 1. alle ingrediënten initialiseren
  document.querySelectorAll("li[data-base-hoeveelheid]").forEach(li => {
    renderIngredient(li);
  });

  // 👉 2. als je personen-selector hebt
  const personenSelect = document.getElementById("personen");
  if (personenSelect) {
    personenSelect.addEventListener("change", function () {
      document.querySelectorAll("li[data-base-hoeveelheid]").forEach(li => {
        renderIngredient(li);
      });
    });
  }

function renderIngredient(li) {
  console.log({
  naam: li.dataset.naam,
  baseAmount,
  amount,
  unit
  });

  const baseAmount = parseFloat(li.dataset.baseHoeveelheid);
  const unit = (li.dataset.eenheid || "").trim();
  const scaling = li.dataset.schaling;

  let amount = baseAmount;

  if (scaling === "portion") {
    const personen = parseInt(selector.value, 10);
    amount = baseAmount * (personen / basePersons);
  }

  const amountSpan = li.querySelector(".ingredient-hoeveelheid");
  const unitSpan = li.querySelector(".ingredient-eenheid");

  // 👉 GEEN hoeveelheid + eenheid bij 0 / NaN én geen zinvolle unit
  const noAmount = Number.isNaN(amount) || amount === 0;
  const noUnit = unit === "" || unit === "-";

  if (noAmount && noUnit) {
    if (amountSpan) amountSpan.textContent = "";
    if (unitSpan) unitSpan.textContent = "";
    return;
  }

  // 👉 hoeveelheid formatteren
  const formatted = formatHoeveelheid(amount, unit);

  if (amountSpan) {
    amountSpan.textContent = formatted;
  }

  // 👉 unit tonen alleen als zinvol
  if (unitSpan) {
    unitSpan.textContent = noUnit ? "" : unit;
  }
}

            
              
  // ✅ BIJ WIJZIGEN PERSONEN
  selector.addEventListener("change", function () {
       document.querySelectorAll("li[data-base-hoeveelheid]").forEach(li => {
          renderIngredient(li);
       });

       if (pdfLink) {
          const url = new URL(pdfLink.href);
          url.searchParams.set("personen", this.value);
          pdfLink.href = url.toString();
       }
  });
 
function renderIngredient(li) {
  const baseAmount = parseFloat(li.dataset.baseHoeveelheid);
  const unit = li.dataset.eenheid;
  const scaling = li.dataset.schaling;
  
  //if (Number.isNaN(baseAmount)) return;
  
  let amount = baseAmount;
  
  if (scaling === "portion") {
    const personen = parseInt(selector.value, 10);
    amount = baseAmount * (personen / basePersons);
  }
  
  const amountSpan = li.querySelector(".ingredient-hoeveelheid");
  const unitSpan = li.querySelector(".ingredient-eenheid");
  
// 👉 niets tonen bij 0 of ongeldig
  if (!amount || amount === 0 || Number.isNaN(amount)) {
    if (amountSpan) amountSpan.textContent = "";
    if (unitSpan) unitSpan.textContent = "";
    return;
  }
  
// 👉 formatteren
  const formatted = formatHoeveelheid(amount, unit);
  
// 👉 hoeveelheid
  if (amountSpan) {
    amountSpan.textContent = formatted;
  }
  
// 👉 eenheid alleen tonen als die zinvol is
  if (unitSpan) {
    if (unit && unit !== "-") {
      unitSpan.textContent = unit;
    } else {
      unitSpan.textContent = "";
    }
  }
  
} 
  
            
              
  // ✅ BIJ WIJZIGEN PERSONEN
  selector.addEventListener("change", function () {
       document.querySelectorAll("li[data-base-hoeveelheid]").forEach(li => {
          renderIngredient(li);
       });
  
       if (pdfLink) {
          const url = new URL(pdfLink.href);
          url.searchParams.set("personen", this.value);
          pdfLink.href = url.toString();
       }
  });
  
});                                                                                                                                                                                 
;           
