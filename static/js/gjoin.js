function submitCode() {
    var code = $("#code-input").val();

    $.ajax(`/join-group?${code}`)
        .done(function (data) {
            // success!
        })
        .fail(function () {
            $('#error-msg').show();
        });
}

$(document).ready(function () {
    $('#sub').click(submitCode);
});