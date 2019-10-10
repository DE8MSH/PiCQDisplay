#!/usr/bin/env python2
# # -*- coding: utf-8 -*-

# PiCQ Display-writer
# 26.12.2017 by MiCKi9
#
# Pythonscript zum Darstellen bestimmter Gatewayinformationen auf einem
# 4x20 Zeichen LCD-Display am I2C-Bus (Adresse 0x27).
#
# Sollte die Adresse nicht stimmen muss entsprechende Konfiguration
# in der Datei lcddriver.py geändert werden. Folgender Befehl sollte beim
# Herausfinden der richtigen Adresse hilfreich sein:
#
# sudo i2cdetect -y 1

import sys
import time

import subprocess

subprocess.call (["sudo /opt/PiCQ/work/test.py"], shell=True)

sys.exit(0)
