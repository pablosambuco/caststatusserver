# -*- coding: utf-8 -*-
import motor
client = motor.motor_tornado.MotorClient(
   "mongodb+srv://<username>:<password>@<cluster-url>/test?retryWrites=true&w=majority")
db = client.test