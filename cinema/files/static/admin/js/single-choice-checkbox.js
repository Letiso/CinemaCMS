// Event listener binding for single-choice-checkbox file inputs
const checkboxLists = document.getElementsByClassName('single_choice_checkbox-list')

for (let i = 0; i < checkboxLists.length; i++) {
    let checkboxList = checkboxLists[i].getElementsByTagName('INPUT');
    for (let i = 0; i < checkboxList.length; i++) {
        checkboxList[i].setAttribute('onclick', 'single_choice_checkbox(event)');
    }
}
// end of Event listener binding

function single_choice_checkbox(event) {
    const lastChecked = event.currentTarget
    const options = document.getElementsByName(lastChecked.name)
    for (let i = 0; i < options.length; i++) {
        if (options[i] !== lastChecked) {
            options[i].checked = false
        }
    }
}