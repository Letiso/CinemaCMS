
const addFormBtn = document.getElementById('top-banners-add-empty-form')
const totalForms = document.getElementById('id_top_banners-TOTAL_FORMS')

addFormBtn.addEventListener('click', add_empty_form)
function add_empty_form(event) {
    if (event) {
        event.preventDefault()
    }
    const currentForms = document.getElementsByClassName('top-banner')
    let currentFormCount = currentForms.length
    const formCopyTarget = document.getElementById('top-banners-list')
    const copyEmptyFormEl = document.getElementById('top-banners-empty-form').cloneNode(true)
    copyEmptyFormEl.setAttribute('class', 'card top-banner')
    copyEmptyFormEl.setAttribute('id', `id_top_banners-${currentFormCount}-`)
    const regex = new RegExp('__prefix__', 'g')

    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
    totalForms.setAttribute('value', currentFormCount + 1)

    formCopyTarget.append(copyEmptyFormEl)
}
