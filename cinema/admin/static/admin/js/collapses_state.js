// init localStorage collapses record
let COLLAPSES = localStorage.getItem('collapses')

if (COLLAPSES) {
    COLLAPSES = JSON.parse(COLLAPSES)
}

// recreate COLLAPSES object if we got an invalid data from LocalStorage
// or just page url is changed
if (!COLLAPSES) {
// if (!COLLAPSES || (COLLAPSES.name !== location.pathname)) {
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
    $("a[data-toggle*='collapse']").on('click', function (event) {
        const collapse_name = $(this).prop('href').split('#')[1]

        toggle_show(event, collapse_name)
    })
}

initCollapsesEventListener()