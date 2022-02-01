// init localStorage collapses record
let COLLAPSES = localStorage.getItem('collapses')

if (COLLAPSES) {
    COLLAPSES = JSON.parse(COLLAPSES)
}

// recreate COLLAPSES object if we got an invalid data from LocalStorage
// or just page url is changed
if (!COLLAPSES || (COLLAPSES.name !== location.pathname)) {

    COLLAPSES = {
      name: location.pathname,
      toShow: {}
    }

    localStorage.setItem('collapses', JSON.stringify(COLLAPSES))
}

// restoring saved collapses state
let key, target;
for (key in COLLAPSES.toShow) {
    target = document.getElementById(COLLAPSES.toShow[key]);
    target.setAttribute('class', `${target.getAttribute('class')} show`)
}


// update localStorage record about collapses
function toggle_show(event, collapse_name) {
    if (collapse_name in COLLAPSES.toShow) {
      delete COLLAPSES.toShow[collapse_name]
    }
    else {
      COLLAPSES.toShow[collapse_name] = event.currentTarget.getAttribute('aria-controls')
    }
    localStorage.setItem('collapses', JSON.stringify(COLLAPSES))
}

// init EventListener on every card collapse div
function initCollapsesEventListener() {
    console.log('first')
    $("a[data-toggle*='collapse']").on('click', function (event) {
        // toggle_show(event, $(this).prop("href"))
        console.log(this)
        console.log($(this).prop('href'))
        console.log('second')
    })
}

console.log('third')
initCollapsesEventListener()