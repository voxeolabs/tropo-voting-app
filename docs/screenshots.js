var casper = require('casper').create({
    viewportSize : {width : 1024, height : 576}
});

casper.start("http://localhost", function() {
    this.wait(500, function() {
        this.capture("dexy--home.png");
    });
});

casper.run();
