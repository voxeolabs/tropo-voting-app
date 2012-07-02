function updater() {
    $.ajax({
        /// @export "get-updated-results"
        url: '/results.json',

        /// @export "success"
        success: function(data) {
            results_json = JSON.parse(data);

            if (!window.previous_data) {
                window.previous_data = results_json;
            }

            function matchesKeyword(keyword, dict) {
                dict['keyword'] == keyword
            }

            /// @export "iterate-records"
            var position = -1;
            var total_votes = 0;
            results_json.forEach(function(item) {

                /// @export "increment-position"
                position += 1;
                position_id = "#position-" + position

                /// @export "find-previous-position"
                previous_position = -1;
                for (var i = 0; i < 9; i++) {
                    var dict = window.previous_data[i];
                    previous_position += 1;
                    if (dict['keyword'] == item['keyword']) {
                        break;
                    }
                }

                var direction;
                if (position > previous_position) {
                    direction = "&darr;";
                } else if (position < previous_position) {
                    direction = "&uarr;";
                } else if (window.previous_data[i]["votes"] < item["votes"]) {
                    direction = "&rarr;"
                } else if (window.previous_data[i]["votes"] == item["votes"]) {
                    direction = "&nbsp;";
                } else {
                    throw "stop";
                }

                var instructions = "Press " + item["number"];
                $(position_id).html('<span class="direction">' + direction + "</span> " + item['title'] + " (" + item["votes"] + " votes) " + '<span class="instructions">' + instructions +  '</span>');
                $(position_id).attr("keyword", item["keyword"]);

                total_votes = total_votes + item["votes"]
            });
            window.previous_data = results_json;

            if (total_votes > window.previous_total) {
                $("#counter").flipCounter("setNumber", total_votes);
                window.previous_total = total_votes
            }
        },
        complete: function() {
           setTimeout(updater, 750);
        }
    })
};

$(document).ready(function() {
    window.previous_total = 0;
    updater();
    $("#counter").flipCounter({
        imagePath : "/static/js/flipCounter-medium.png",
        easing: jQuery.easing.easeOutCubic,
        duration: 5000
    });
});
