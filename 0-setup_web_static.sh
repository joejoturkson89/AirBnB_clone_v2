#!/usr/bin/env bash
# This script sets up web servers for the development of web static
sudo apt-get -y update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/releases/test/index.html
sudo echo -e "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
file=/etc/nginx/sites-available/default
phrase="location /hbnb_static/{\n\talias /data/web_static/current/;\n}\n"
sudo sed -i "27i $phrase" $file
sudo service nginx restart
