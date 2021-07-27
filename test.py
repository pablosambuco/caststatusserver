# coding: utf-8
"""prueba"""
# pylint: disable=redefined-builtin
import time
from pprint import pprint as print
from caststatusserver import CastStatusServer
cast = CastStatusServer()
time.sleep(1)
cast.init()
time.sleep(1)
print(cast.update())
