function edit(id) {
    let inputId = id.replace("Button", "Input");
    let submitId = id.replace("Button", "Submit");
    let input = document.getElementById(inputId);
    let submit = document.getElementById(submitId);
    input.readOnly = false;
    submit.classList.remove("d-none");
    input.classList.remove("noBorder")
}

function submitEdited(id) {
    let submit = document.getElementById(id);
    let inputId = id.replace("Submit", "Input");
    let input = document.getElementById(inputId);
    submit.classList.add("d-none");
    input.classList.add("noBorder")
    input.readOnly = true;
}

function item_alert() {
    let message = document.getElementById("item_alert").innerHTML
    if(message) {
        alert(message)
    }
}

function countCharacters(charsId, inputId) {
    let inputtedChars = document.getElementById(inputId).value;
    let maxInputLength = document.getElementById(inputId).maxLength
    let remainingChars = parseInt(maxInputLength) - parseInt(inputtedChars.length);
    document.getElementById(charsId).innerHTML = remainingChars.toString();
}