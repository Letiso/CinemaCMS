

function add_empty_form(event) {
    if (event) {
        event.preventDefault()
    }

    let currentFormSet = event.target.getAttribute('name')
    const formset = {
        total: `id_${currentFormSet}-TOTAL_FORMS`,
        list: `${currentFormSet}-list`,
        empty_form: `${currentFormSet}-empty-form`,
        class: `card ${currentFormSet}`,
    }

    let totalForms = document.getElementById(formset.total)
    let formsCount = document.getElementsByClassName(currentFormSet).length

    const formCopyTarget = document.getElementById(formset.list)
    const copyEmptyFormEl = document.getElementById(formset.empty_form).cloneNode(true)

    const regex = new RegExp('__prefix__', 'g')
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, formsCount)

    copyEmptyFormEl.setAttribute('class', formset.class)
    copyEmptyFormEl.setAttribute('id', `id_${currentFormSet}-${formsCount}`)

    totalForms.setAttribute('value', formsCount + 1)

    formCopyTarget.append(copyEmptyFormEl)
}
