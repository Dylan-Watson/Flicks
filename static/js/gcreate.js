function checkPeople() {
    $.get('/check-people')
        .done(function (data) {
            // TODO: Start here. pass code in url. write the backend, loop through current members. continue in loop on current user. return all other members of group. loop through and append in js
        })
        .fail(function () {

        });
}

$(document).ready(function () {
    // setInterval(checkPeople, 1000);
});