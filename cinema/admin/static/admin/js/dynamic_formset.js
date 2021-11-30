

function add_empty_form(event, currentFormset) {
    // page reloading stop
    if (event) {
        event.preventDefault()
    }

    const totalForms = document.getElementById(`id_${currentFormset}-TOTAL_FORMS`)
    const formIndex = document.getElementsByClassName(currentFormset).length

    const formCopyTarget = document.getElementById(`${currentFormset}-list`)
    let copyEmptyFormEl = document.getElementById(`${currentFormset}-empty-form`).cloneNode(true)

    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(
        RegExp('__prefix__', 'g'), formIndex
    )

    copyEmptyFormEl.setAttribute('class',
        copyEmptyFormEl.getAttribute('class').replace(
            RegExp('hidden'), currentFormset
        )
    )
    copyEmptyFormEl.setAttribute('id', `id_${currentFormset}-${formIndex}`)

    totalForms.setAttribute('value', formIndex + 1)
    formCopyTarget.append(copyEmptyFormEl)
}
