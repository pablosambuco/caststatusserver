#!/usr/bin/python3
# -*- coding: utf-8 -*-
import custom_functions as s
import time

s.buscar()

while True:
   try:
      time.sleep(1)
   except KeyboardInterrupt:
      break   
