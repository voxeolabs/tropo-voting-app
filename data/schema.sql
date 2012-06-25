CREATE TABLE songs (
    number INTEGER PRIMARY KEY,
    title TEXT,
    keyword TEXT,
    votes_cache INTEGER
);

INSERT INTO songs (title, keyword, number) VALUES ("Piano Man by Billy Joel", "piano", 1);
INSERT INTO songs (title, keyword, number) VALUES ("Imagine by John Lennon", "imagine", 2);
INSERT INTO songs (title, keyword, number) VALUES ("Rocket Man by Elton John", "rocket", 3);
INSERT INTO songs (title, keyword, number) VALUES ("Crazy Little Thing Called Love by Queen", "crazy", 4);
INSERT INTO songs (title, keyword, number) VALUES ("Daydream Believer by The Monkees", "daydream", 5);
INSERT INTO songs (title, keyword, number) VALUES ("Sweet Caroline by Neil Diamond", "caroline", 6);
INSERT INTO songs (title, keyword, number) VALUES ("Hey Jude by The Beatles", "jude", 7);
INSERT INTO songs (title, keyword, number) VALUES ("Don't Stop Believin by Journey", "believing", 8);
INSERT INTO songs (title, keyword, number) VALUES ("Tainted Love by Soft Cell", "tainted", 9);

CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_number INTEGER,
    phone_number TEXT
);
