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

                var instructions = "";
                if (position == 0) {
                    instructions = "to vote ";
                }
                instructions = instructions += "say '" + item["keyword"] + "' or press " + item["number"];
                $(position_id).html(item['title'] + " (" + item["votes"] + " votes) " + '<span class="instructions">' + instructions +  '</span>');
                $(position_id).attr("keyword", item["keyword"]);

                var direction;
                if (position > previous_position) {
                    direction = "down";
                } else if (position < previous_position) {
                    direction = "up";
                } else {
                    direction = "unchanged";
                }

                $(position_id).attr("class", direction);
                total_votes = total_votes + item["votes"]
            });
            window.previous_data = results_json;

            $("#counter").flipCounter("setNumber", total_votes);
        },
        complete: function() {
            setTimeout(updater, 1250);
        }
    })
};

$(document).ready(function() {
    updater();
    $("#counter").flipCounter({
        imagePath : "/static/js/flipCounter-medium.png"
    });
});
