#!/usr/bin/python3
# -*- coding: utf-8 -*-
import modules.custom_functions as s
import time

s.create_listeners()

while True:
   try:
      time.sleep(1)
   except KeyboardInterrupt:
      break
