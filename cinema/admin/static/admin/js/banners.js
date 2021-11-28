

const addFormBtnTopBanners = document.getElementById('top_banners-add')
const addFormBtnNewsBanners = document.getElementById('news_banners-add')

addFormBtnTopBanners.addEventListener('click', add_empty_form)
addFormBtnNewsBanners.addEventListener('click', add_empty_form)


function add_empty_form(event) {
    if (event) {
        event.preventDefault()
    }
    let currentFormSet = event.target.getAttribute('name')

    let totalForms = document.getElementById(`id_${currentFormSet}-TOTAL_FORMS`)
    let formsCount = document.getElementsByClassName(currentFormSet).length

    const formCopyTarget = document.getElementById(`${currentFormSet}-list`)
    const copyEmptyFormEl = document.getElementById(`${currentFormSet}-empty-form`).cloneNode(true)

    const regex = new RegExp('__prefix__', 'g')
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, formsCount)

    copyEmptyFormEl.setAttribute('class', `card ${currentFormSet}`)
    copyEmptyFormEl.setAttribute('id', `id_${currentFormSet}-${formsCount}-`)

    totalForms.setAttribute('value', formsCount + 1)

    formCopyTarget.append(copyEmptyFormEl)
}


// const addFormBtn = document.getElementById('news-banners-add-empty-form')
// const totalForms = document.getElementById('id_news_banners-TOTAL_FORMS')
//
// addFormBtn.addEventListener('click', add_empty_form)
// function add_empty_form(event) {
//     if (event) {
//         event.preventDefault()
//     }
//     const currentForms = document.getElementsByClassName('news-banner')
//     let currentFormCount = currentForms.length
//     const formCopyTarget = document.getElementById('news-banners-list')
//     const copyEmptyFormEl = document.getElementById('news-banners-empty-form').cloneNode(true)
//     copyEmptyFormEl.setAttribute('class', 'card news-banner')
//     copyEmptyFormEl.setAttribute('id', `id_news_banners-${currentFormCount}-`)
//     const regex = new RegExp('__prefix__', 'g')
//
//     copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
//     totalForms.setAttribute('value', currentFormCount + 1)
//
//     formCopyTarget.append(copyEmptyFormEl)
// }