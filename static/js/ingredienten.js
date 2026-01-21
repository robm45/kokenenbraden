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
  const baseAmount = parseFloat(li.dataset.baseHoeveelheid);
  const unit = li.dataset.eenheid || "";
  const scaling = li.dataset.schaling;

  if (Number.isNaN(baseAmount)) return;

  let amount = baseAmount;

  if (scaling === "portion") {
    const personen = parseInt(selector.value, 10);
    amount = baseAmount * (personen / basePersons);
  }

  const formatted = formatHoeveelheid(amount, unit);

  const amountSpan = li.querySelector(".ingredient-hoeveelheid");
  if (amountSpan) {
    amountSpan.textContent = formatted;
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
