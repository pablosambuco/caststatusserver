#!/bin/bash

#install dependencies
yes | sudo apt-get install g++ protobuf-compiler libprotobuf-dev libboost-dev curl m4 wget libssl-dev python3-clang-9
wget https://download.rethinkdb.com/repository/raw/dist/rethinkdb-2.4.1.tgz
tar xf rethinkdb-2.4.1.tgz
cd rethinkdb-2.4.1
./configure --allow-fetch python=python3
sudo make install
cd ..
rm -rf rethinkdb-2.4.1
rm rethinkdb-2.4.1.tgz

sudo pip3 install rethinkdb

