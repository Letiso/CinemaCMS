
function add_empty_form(event, form_prefix) {
    // page reloading stop
    if (event) {
        event.preventDefault()
    }
    
    const totalForms = document.getElementById(`id_${form_prefix}-TOTAL_FORMS`)
    const formIndex = document.getElementsByClassName(form_prefix).length

    const formCopyTarget = document.getElementById(`${form_prefix}-list`)
    let copyEmptyFormEl = document.getElementById(`${form_prefix}-empty-form`).cloneNode(true)

    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(
        RegExp('__prefix__', 'g'), formIndex
    )

    copyEmptyFormEl.className = copyEmptyFormEl.className.replace(
            RegExp('hidden'), form_prefix
    )
    copyEmptyFormEl.id =  `id_${form_prefix}-${formIndex}`

    totalForms.value = formIndex + 1
    formCopyTarget.append(copyEmptyFormEl)
}
