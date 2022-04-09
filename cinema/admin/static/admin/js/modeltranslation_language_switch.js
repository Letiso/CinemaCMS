
function modeltranslationLanguageSwitch (this_id) {
    const data = this_id.split('-')
    let prefix = data[0]
    let lang_code = data[1]

    $(`span[class^=modeltranslation-${prefix}]`).each(function () {
        $(this).hide()
    })
    $(`.modeltranslation-${this_id}`).show()
}

// on page load
$('ul[id$="-language-tabs"] li a[class*="active"]').each(function () {
    modeltranslationLanguageSwitch(this.id)
})

// on click
$('ul[id$="-language-tabs"] li a').on('click', function () {
    modeltranslationLanguageSwitch(this.id)
})
