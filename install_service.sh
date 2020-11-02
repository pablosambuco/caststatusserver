#!/bin/bash

sudo cp caststatus.service /lib/systemd/system/
sudo systemctl enable caststatus
sudo systemctl start caststatus

