document.addEventListener("DOMContentLoaded", function () {
  const addBtn = document.getElementById("add-ingredient");
  const formsetBody = document.getElementById("ingredienten-formset");
  const totalForms = document.getElementById("id_ingredient_items-TOTAL_FORMS");
  const emptyForm = document.getElementById("empty-form");

  if (!addBtn || !formsetBody || !totalForms || !emptyForm) {
    console.error("Formset onderdelen ontbreken");
    return;
  }

  addBtn.addEventListener("click", function () {
    const count = parseInt(totalForms.value, 10);

    let newRow = emptyForm.innerHTML.replace(/__prefix__/g, count);

    formsetBody.insertAdjacentHTML("beforeend", newRow);
    totalForms.value = count + 1;
  });

  formsetBody.addEventListener("change", function(e) {
    const forms = formsetBody.querySelectorAll(".ingredient-form");
    const lastForm = forms[forms.length - 1];

    if (lastForm.contains(e.target)) {
      document.getElementById("add-ingredient").click();
    }
  });

});

document.addEventListener("DOMContentLoaded", function () {
  const formsetBody = document.getElementById("ingredienten-formset");

  formsetBody.addEventListener("click", function(e) {
    if (e.target && e.target.classList.contains("remove-ingredient")) {
      const row = e.target.closest("tr");
      if (!row) return;

      // Checkbox DELETE aanvinken zodat Django het verwijdert
      const deleteInput = row.querySelector('input[type="checkbox"][name$="DELETE"]');
      if (deleteInput) deleteInput.checked = true;

      // Rij verbergen
      row.style.display = "none";
    }
  });
});

