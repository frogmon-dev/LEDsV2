# -*- coding: utf-8 -*-
# uCommon.py

import os

from datetime    import datetime, timedelta
from collections import OrderedDict

class COM:
	gSetupFile = 'setup.ini'
	gControlFile = 'control.ini'
	
	gHomeDir   = '/home/pi/LEDsV2/bin/'
	gLogDir    = '/home/pi/LEDsV2/bin/logs/'
	gJsonDir   = '/home/pi/LEDsV2/bin/json/'	
	
	gProcessNM = os.path.abspath( __file__ )

	gYYYY = '0000'
	gMM   = '00'
	gDD   = '00'
	gHH   = '00'
	gNN   = '00'
	gSS   = '00'
	
	gstrYMD    = datetime.now().strftime('%Y%m%d')
	gstrYMDHMS = datetime.now().strftime('%Y%m%d%H%M%S')
	gstrDATE   = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	gStrTime   = datetime.now().strftime('%H:%M:%S')
	
	gNOW  = datetime.now()
	
	gPORT = '/dev/ttyUSB0'
	#gPORT = '/dev/ttyAMA0'
