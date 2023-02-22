#!/bin/bash

sudo cp service/caststatusserver.service /lib/systemd/system/
sudo systemctl enable caststatusserver
sudo systemctl start caststatusserver

