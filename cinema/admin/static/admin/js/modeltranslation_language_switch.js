
function modeltranslationLanguageSwitch (this_id) {
    const data = this_id.split('--')
    const prefix = data[0]
    const lang_code = data[1]

    $(`span[class*=modeltranslation-${prefix}]`).hide()
    $(`span[class*=modeltranslation-${prefix}][class*=${lang_code}]`).show()
}

// on page load
$('ul[id$="-language-tabs"] li a[class*="active"]').each(function () {
    modeltranslationLanguageSwitch(this.id)
})

// on click
$('ul[id$="-language-tabs"] li a').on('click', function () {
    modeltranslationLanguageSwitch(this.id)
})
