

function add_empty_form(event, currentFormset) {
    if (event) {
        event.preventDefault()
    }

    const formset = {
        total: `id_${currentFormset}-TOTAL_FORMS`,
        list: `${currentFormset}-list`,
        empty_form: `${currentFormset}-empty-form`,
        class: `card ${currentFormset}`,
    }

    const totalForms = document.getElementById(formset.total)
    const formsCount = document.getElementsByClassName(currentFormset).length

    const formCopyTarget = document.getElementById(formset.list)
    let copyEmptyFormEl = document.getElementById(formset.empty_form).cloneNode(true)

    const regex = new RegExp('__prefix__', 'g')
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, formsCount)

    copyEmptyFormEl.setAttribute('class', formset.class)
    copyEmptyFormEl.setAttribute('id', `id_${currentFormset}-${formsCount}`)

    totalForms.setAttribute('value', formsCount + 1)

    formCopyTarget.append(copyEmptyFormEl)
}
