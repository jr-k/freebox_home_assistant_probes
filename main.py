from fbxtools.fbx import Fbx
import time
import sys
from flask import Flask
from flask import request
import subprocess
import json
import os

# Globals
FREEBOX_API_VERSION = 4
SERVER_PORT = 9876

server = Flask(__name__)
app = Fbx('https://mafreebox.freebox.fr/api/v' + str(FREEBOX_API_VERSION))
doAuth = not os.path.exists(os.path.realpath('./') + '/app_auth.json')

# Init (Optionnal)
if doAuth:
	appToken, trackId = app.get_app_token()
	print(appToken)
	currentStatus = ''
	attempt = 5
	while attempt > 0:
		time.sleep(3)
		response = app.track_auth_progress(trackId)
		if response['data']['success']:
			currentStatus = response['data']['result']['status']
		if currentStatus == 'granted':
			print('[fbx] Your application got authorization !')
			break
		print('[fbx] attempts remaining: ' + str(attempt) + ', status: ' + currentStatus)
		attempt -= 1

@server.route('/')
def index():
	return "hi"

@server.route('/probes')
def doProbes():
	system = get_system()
	connection = get_connection()
	storageDisk = get_storage_disk()

	del system['cookies']
	systemClear = {f'system_{k}': v for k, v in system['data']['result'].items()}
	connectionClear = {f'connection_{k}': v for k, v in connection['data']['result'].items()}
	allClear = {**systemClear, **connectionClear}

	d = 0
	for disk in storageDisk['data']['result']:
		p = 0
		partitions = disk['partitions']
		del disk['partitions']
		diskClear = {f'disk{d}_{k}': v for k, v in disk.items()}
		allClear = {**allClear, **diskClear}
		for partition in partitions:
			partitionClear = {f'disk{d}_partition{p}_{k}': v for k, v in partition.items()}
			allClear = {**allClear, **partitionClear}
			p += 1
		d += 1
	allClearJson = json.dumps(allClear)

	return allClearJson

@app.api.call('/system')
def get_system():
	return {}

@app.api.call('/connection')
def get_connection():
	return {}

@app.api.call('/storage/disk')
def get_storage_disk():
	return {}

app.get_session_token()
server.run(host="0.0.0.0", port=SERVER_PORT)
app.disconnect_app()
