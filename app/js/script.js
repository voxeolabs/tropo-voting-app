function updater() {
    $.ajax({
        url: '/results',
        success: function(data) {
            $('#results').html(data);
        },
        complete: function() {
            setTimeout(updater, 5000);
        }
    })
};

$(document).ready(function() {
    updater();
});
