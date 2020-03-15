function edit(id) {
    let inputId = id.replace("Button", "Input");
    let submitId = id.replace("Button", "Submit");
    let input = document.getElementById(inputId);
    let submit = document.getElementById(submitId);
    input.readOnly = false;
    submit.classList.remove("d-none");
}

function submitEdited(id) {
    let submit = document.getElementById(id);
    let inputId = id.replace("Submit", "Input");
    let input = document.getElementById(inputId);
    submit.classList.add("d-none");
    input.readOnly = true;
}
