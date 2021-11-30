

function add_empty_form(event, currentFormset) {
    if (event) {
        event.preventDefault()
    }

    const formset = {
        total: `id_${currentFormset}-TOTAL_FORMS`,
        list: `${currentFormset}-list`,
        empty_form: `${currentFormset}-empty-form`,
    }

    const totalForms = document.getElementById(formset.total)
    const formIndex = document.getElementsByClassName(currentFormset).length

    const formCopyTarget = document.getElementById(formset.list)
    let copyEmptyFormEl = document.getElementById(formset.empty_form).cloneNode(true)

    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(
        RegExp('__prefix__', 'g'), formIndex
    )

    copyEmptyFormEl.setAttribute('class',
        copyEmptyFormEl.getAttribute('class').replace(
            RegExp('hidden'), currentFormset
        )
    )
    // copyEmptyFormEl.setAttribute('class', formset.class)

    copyEmptyFormEl.setAttribute('id', `id_${currentFormset}-${formIndex}`)

    totalForms.setAttribute('value', formIndex + 1)

    formCopyTarget.append(copyEmptyFormEl)
}
