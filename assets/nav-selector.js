$(document).ready(function () {
    var menu = {};
    $('.nav-item').each(function () {
        menu[$(this).attr('href')] = $(this)
    })
    var selected = menu[window.location.pathname]
    selected.addClass('active');
});