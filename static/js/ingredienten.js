document.addEventListener("DOMContentLoaded", function () {
              
  const selector = document.getElementById("personen-selector");
  if (!selector) return;

  const basePersons = parseInt(selector.dataset.basePersons, 10);
  const ingredienten = document.querySelectorAll("#ingredienten-lijst li");
  const pdfLink = document.getElementById("pdf-download");
              
  function formatHoeveelheid(amount, unit) {
    if (!amount || amount === 0) return "";
              
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
              
              
              
  function updateIngredienten(geselecteerdePersonen) {
    const personen = parseInt(geselecteerdePersonen, 10);
    const factor = personen / basePersons;
              
    //console.log("updateIngredienten aangeroepen met:", geselecteerdePersonen);
              
    ingredienten.forEach(li => {
      const base = parseFloat(li.dataset.baseHoeveelheid);
      const unit = li.dataset.eenheid || "";
      const schaling = li.dataset.schaling;
              
      const hoeveelheidSpan = li.querySelector(".ingredient-hoeveelheid");
              
      //console.log({       
      //     naam: li.dataset.naam,
      //     base,          
      //     unit,          
      //     schaling       
      //});                 
              
      // Geen hoeveelheid → niets tonen
      if (!base || schaling === "none") {
        hoeveelheidSpan.textContent = "";
        return;           
      }       
              
      let nieuweHoeveelheid = base;
              
      if (schaling === "portion") {
        nieuweHoeveelheid = base * factor;
      }       
              
      if (unit === "st") {
        nieuweHoeveelheid = Math.ceil(nieuweHoeveelheid);
      }       
              
      hoeveelheidSpan.textContent =
        formatHoeveelheid(nieuweHoeveelheid, unit);
              
      //console.log({       
      //  nieuweHoeveelheid 
      //});                 
    });       
  }           
              
  // ✅ INITIËLE AANROEP BIJ PAGINALAAD
  updateIngredienten(basePersons);
              
  // ✅ BIJ WIJZIGEN PERSONEN
  selector.addEventListener("change", function () {
    updateIngredienten(this.value);
              
    if (pdfLink) {        
      const url = new URL(pdfLink.href);
      url.searchParams.set("personen", this.value);
      pdfLink.href = url.toString();
    }         
  });         
              
});           
