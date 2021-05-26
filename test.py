# coding: utf-8
import time
import pprint
from caststatusserver import CastStatusServer
cast = CastStatusServer()
time.sleep(1)
cast.init()
time.sleep(1)
pprint.pprint(cast.update())
