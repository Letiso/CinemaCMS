// init localStorage collapses record
let collapses = localStorage.getItem('collapses')

if (collapses) {
    collapses = JSON.parse(collapses)
}

if (!collapses || (collapses.name !== location.pathname)) {
    collapses = {
      name: location.pathname,
      toShow: {}
    }
    localStorage.setItem('collapses', JSON.stringify(collapses))
}

// restoring saved collapses state
let key, target;
for (key in collapses.toShow) {
    target = document.getElementById(collapses.toShow[key]);
    target.setAttribute('class', `${target.getAttribute('class')} show`)
}

// log
// console.log(localStorage.getItem('collapses'))
// console.log(collapses)


// update localStorage record about collapses
function toggle_show(event, collapse) {
    if (collapse in collapses.toShow) {
      delete collapses.toShow[collapse]
    }
    else {
      collapses.toShow[collapse] = event.currentTarget.getAttribute('aria-controls')
    }
    localStorage.setItem('collapses', JSON.stringify(collapses))

    // log
    // console.log(collapse)
    // console.log(JSON.parse(localStorage.getItem('collapses')).toShow)
}
