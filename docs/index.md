[TOC]

## System Setup and Installation

The web application described here is written using [the web.py
framework](http://webpy.org). A config file is included for deployment using
apache and mod_wsgi, more information can be found
[here](http://webpy.org/cookbook/mod_wsgi-apache) and in the section called
'Deployment' [on this page](http://webpy.org/cookbook/).

The ubuntu installation instructions provided below have been verified using an
EC2 instance running the AMI shown in this launch script:

{{ d['/run-ec2.sh|pyg'] }}

Here are the full instructions for installing all necessary software and starting the web application on a generic ubuntu server.

We start by making sure we have the latest system updates and all install packages are upgraded to their most recent versions:

{{ d['/ubuntu-setup.sh|idio']['update-package-manager'] }}

We will need git for installing code from repositories:

{{ d['/ubuntu-setup.sh|idio']['utilities'] }}

We install python and [pip](http://www.pip-installer.org/) for installing python packages:

{{ d['/ubuntu-setup.sh|idio']['install-python'] }}

We use ubuntu's package manager to install the webpy framework and also the sqlite3 database:

{{ d['/ubuntu-setup.sh|idio']['webpy-installs'] }}

We install the tropo-webapi-python package from source:

{{ d['/ubuntu-setup.sh|idio']['tropo-installs'] }}

We install the apache2 server and ensure that mod_rewrite is enabled:

{{ d['/ubuntu-setup.sh|idio']['install-apache'] }}

We install mod_wsgi which will let us easily use apache to run web.py applications:

{{ d['/ubuntu-setup.sh|idio']['install-wsgi'] }}

Next we fetch the source code for our web application and create the sqlite database from the schema:

{{ d['/ubuntu-setup.sh|idio']['install-voting-app'] }}

We specify the canonical server name to be used in an environment variable which will be picked up by apache:

{{ d['/ubuntu-setup.sh|idio']['set-server-name'] }}

This should be set to whatever canonical name you want to use to host this app.
You can leave it as 'example.com' for testing purposes and create a record in
your development machine's host file which links the IP address of your
development server to example.com.

We tell apache to use the configuration file in the tropo-voting-app
repository, and we restart the apache server so all our changes are loaded:

{{ d['/ubuntu-setup.sh|idio']['configure-apache'] }}

As written, this will add another vhost record to the existing apache2 config.
You can also uncomment the line that removes the sites-available/default file
and then the only vhost will be the one specified here.

That's it for our bash script! At this point you should be able to hit the canonical server name and, assuming you have DNS set up, you should see the app running.

Here is the apache configuration file that has been activated:

{{ d['/apache.conf|idio'] }}

## Overview

A web application serves the python script which drives our call interface, and
the web application also exposes voting results, counts votes and stores the
available options. The web application supports both the tropo web api and
scripting interfaces.

Here is the SQL which creates the database tables we will use and populates the
songs table:

{{ d['/data/schema.sql|pyg'] }}

## Getting Started

### Scripting

Our web application exposes a static python file which contains the script that
will be used by the scripting api. We point the tropo application to the url of
this script file.

http://voice.pitchlift.org/script.py

### WebAPI

We define a starting URL which we point our tropo application to. This method
will interact only minimally with the user (maybe saying "hello"), but its
primary object is to direct the call to the appropriate handler. This might
mean differentiating between text and voice, or directing based on the caller
id or network, but even if it's just a simple redirect this is a nice option to
avoid hard-coding the starting point into the tropo application specification.
If you want to change your menu options you can simply change where this start
method points to rather than having to change the url in the tropo console.

{{ d['/app/voting_webapi.py|idio']['start'] }}

## Preparing the Menu: A List of Songs

The point of the application is to allow callers to vote on which of the
available songs they would most like to hear. So, callers will first be
presented with a list of the available songs.

### Scripting

Using the scripting interface, our script is run by the tropo instance so it
doesn't have direct access to the database. We need to allow it to fetch a list
of songs from our web application:

Here we see a method in the songs model which returns an array of song
information:

{{ d['/models/songs.py|idio']['songs-array'] }}

We expose the available songs as a simple CSV listing:

{{ d['/app/voting_scripting.py|idio']['songs'] }}

{{ d['curl.sh|pyg'] }}

<pre>
{{ d['curl.sh|sh'] }}
</pre>

In our voice script, we fetch and parse this CSV data:

{{ d['/app/script.py|idio']['load-songs'] }}

We prepare the menu prompt which will tell the user how to vote for each song
and tells Tropo what the acceptable responses are:

{{ d['/app/script.py|idio']['song-prompt'] }}

### Web API

Using the Tropo Web API, we have direct access to the database, so we prepare
the prompt directly.

{{ d['/app/voting_webapi.py|idio']['do-menu'] }}

## Voting

### Scripting

In the scripting API, we greet the caller and play the menu prompt, capturing the result:

{{ d['/app/script.py|idio']['prompt-user'] }}

Then we post the vote to the server to save it:

{{ d['/app/script.py|idio']['post-vote'] }}

### Web API

## Saving Vote

The server page appends the vote to the database:

{{ d['/app/voting_scripting.py|idio']['vote'] }}

The votes model handles the appending:

{{ d['/models/votes.py|idio']['vote-for-song'] }}

{{ d['/models/songs.py|idio']['cache-vote'] }}

We can view individual votes for debugging (to be removed):

{{ d['curl-votes.sh|pyg'] }}

<pre>
{{ d['curl-votes.sh|sh'] }}
</pre>

The app's home page shows us the songs and current vote tally:

![home page screenshot](home.png)
