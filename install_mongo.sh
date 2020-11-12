#!/bin/bash

sudo apt-get update
sudo apt-get install mongodb #instala server, clientes y dev
sudo service mongodb start
mongorestore db/
