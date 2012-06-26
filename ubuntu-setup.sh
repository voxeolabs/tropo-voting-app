#!/bin/bash -v

### @export "capture-logs"
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

### @export "update-package-manager"
apt-get update
apt-get upgrade -y --force-yes

### @export "utilities"
apt-get install -y git-core

### @export "install-python"
apt-get install -y python-dev
apt-get install -y python-pip

### @export "webpy-installs"
apt-get install -y python-webpy
apt-get install -y sqlite3

### @export "tropo-installs"
git clone https://github.com/tropo/tropo-webapi-python.git
cd tropo-webapi-python
pip install .
cd ..

### @export "install-apache"
apt-get install -y apache2
a2enmod rewrite

### @export "install-wsgi"
apt-get install -y libapache2-mod-wsgi

### @export "install-voting-app"
cd /var/www
git clone https://github.com/voxeolabs/tropo-voting-app
cd tropo-voting-app
sqlite3 data/data.sqlite3 < data/schema.sql
chown -R www-data data

### @export "set-server-name"
export TROPO_VOTING_APP_SERVER_NAME="example.com" # change to canonical server name or point IP address to example.com in your /etc/hosts for testing

### @export "configure-apache"
#rm /etc/apache2/sites-available/default # uncomment to remove other vhosts
echo "Include /var/www/tropo-voting-app/apache.conf" >> /etc/apache2/sites-available/default
apachectl restart
