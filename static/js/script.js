/**
 * Makes input editable by removing readonly attribute.
 * Takes 'edit' button id and can recreate other needed id's
 * as they all start with items ID from the database (part of the key).
 * Also, makes the 'save' button  visible so the edited value can be 
 * sent to the database. 
 * 
 * Triggered by 'edit' button.
 * @param {string} id 
 */
function edit(id) {
    let inputId = id.replace("Button", "Input");
    let submitId = id.replace("Button", "Submit");
    let input = document.getElementById(inputId);
    let submit = document.getElementById(submitId);
    input.readOnly = false;
    submit.classList.remove("d-none");
    input.classList.remove("noBorder")
}

/**
 * Reverses the actions of 'edit' function above,
 * so that the list comes back to the look before
 * edit. 
 * Takes 'save' button id. 
 * Triggered by the 'save' button.
 * @param {string} id 
 */
function submitEdited(id) {
    let submit = document.getElementById(id);
    let inputId = id.replace("Submit", "Input");
    let input = document.getElementById(inputId);
    submit.classList.add("d-none");
    input.classList.add("noBorder")
    input.readOnly = true;
}

/**
 * Displays an alert that a user should choose or create a list
 * first, before adding items, if the message exists.
 * The message existence is determined by the code in the python file. 
 * The message has content if there is no list chosen, otherwise
 * it is an empty string. 
 */
function item_alert() {
    let message = document.getElementById("itemAlert").innerHTML
    if(message) {
        alert(message)
    }
}

/**
 * Keeps track of remaining characters in input fields 
 * with limited number of characters and displays it for the user. 
 * @param {string} charsId 
 * @param {string} inputId 
 */
function countCharacters(charsId, inputId) {
    let inputtedChars = document.getElementById(inputId).value;
    let maxInputLength = document.getElementById(inputId).maxLength
    let remainingChars = parseInt(maxInputLength) - parseInt(inputtedChars.length);
    document.getElementById(charsId).innerHTML = remainingChars.toString();
}