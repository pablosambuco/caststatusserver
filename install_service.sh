#!/bin/bash

sudo cp service/caststatus.service /lib/systemd/system/
sudo systemctl enable caststatus
sudo systemctl start caststatus

