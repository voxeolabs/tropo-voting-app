var casper = require('casper').create({
    viewportSize : {width : 1000, height : 800}
});

casper.start("http://localhost", function() {
    this.capture("dexy--home.png");
});

casper.run();
