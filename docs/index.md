## Overview

A web application serves the python script which drives our call interface, and the web application also exposes voting results, counts votes and stores the available options.

Here is the SQL which creates the database tables we will use and populates the songs table:

{{ d['/data/schema.sql|pyg'] }}

## Songs

We create a songs model which abstracts database interactions. Here we see a method which returns an array of song information:

{{ d['/models/songs.py|idio']['songs-array'] }}

We expose the available songs as a simple CSV listing:

{{ d['/app/voice.py|idio']['songs'] }}

{{ d['curl.sh|pyg'] }}

<pre>
{{ d['curl.sh|sh'] }}
</pre>

## Calling

In our voice script, we parse this CSV data to obtain a list of songs which we use to prompt the caller with:

{{ d['/app/script.py|idio']['load-songs'] }}

We prepare the prompt which will tell the user how to vote for each song:

{{ d['/app/script.py|idio']['song-prompt'] }}

Now we greet the caller and play our prompt, capturing the result:

{{ d['/app/script.py|idio']['prompt-user'] }}

## Voting

Then we post the vote to the server to save it:

{{ d['/app/script.py|idio']['post-vote'] }}

The server page appends the vote to the database:

{{ d['/app/voice.py|idio']['vote'] }}

The votes model handles the appending:

{{ d['/models/votes.py|idio']['vote-for-song'] }}

{{ d['/models/songs.py|idio']['cache-vote'] }}

We can view individual votes for debugging (to be removed):

{{ d['curl-votes.sh|pyg'] }}

<pre>
{{ d['curl-votes.sh|sh'] }}
</pre>

The app's home page shows us the songs and current vote tally:

{{ d['curl-home.sh|pyg'] }}

<pre>
{{ d['curl-home.sh|sh'] }}
</pre>
