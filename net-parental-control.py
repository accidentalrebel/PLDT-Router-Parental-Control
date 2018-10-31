#!/usr/bin/env python3

# A simple python script to manage the Parental Control system of a PLDT Home DSL router.
# Juan Karlo Licudine. 2018. accidentalrebel@gmail.com
#
# First argument: The command to invoke
# Check out ACCEPTED_COMMANDS constant variablefor full list of commands
#
# Second argument: Device name/s to exclude.
# Separated by a comma. For example, "device1,device2".
#
# Sample usages:
# ./net-parental-control.py enable
# ./net-parental-control.py lockdown device3,device4
#
# The devices.json file should look like the one below:
# {
#    "device1" : {
#	"mac" : "00:01:02:03:04:05",  # The mac address of the device
#	"enableTimeFrom" : "09:30",   # The starting time to enable this device
#	"enableTimeTo" : "23:00"      # The time to disable this device
#    },
#    "device2" : {
#	"mac" : "00:01:02:03:04:05",
#	"enableTimeFrom" : "14:00",
#	"enableTimeTo" : "20:00"
#    }
#}

import time
import json
import sys
import requests

USERNAME = 'admin'
PASSWORD = 'pass'
ACCEPTED_COMMANDS = [ 'lockdown', 'unlockdown', 'enable', 'disable' ]

if len(sys.argv) <= 1:
    print('No command specified. Exiting')
    exit()
    
command_type = sys.argv[1]
if not command_type in ACCEPTED_COMMANDS:
    print('Unknown command. Exiting.')
    exit()

command_target = 'all' # This is always "all", for now.
if len(sys.argv) > 2:
    excluded_devices = sys.argv[2]
else:
    excluded_devices = None

usersFile = open('devices.json', 'r')
users = json.load(usersFile)
usersFile.close();

disableTimeFrom = '09:00'
disableTimeTo = '09:01'

url = 'http://192.168.1.1/'
session = requests.session()

def sendRequest(page, payload):
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
    return session.post(url + page, data=payload, headers=headers)

def login():
    page = 'login.cgi'
    payload = { 'username':USERNAME, 'password':PASSWORD, 'submit.htm%3Flogin.htm':'Send' }
    sendRequest(page, payload)
    print('Logged in')

def deleteAllEntries():
    page = 'form2timelimitdel.cgi'
    payload = { 'deleteAll':'Delete+All', 'delindex':'', 'submit.htm%3Ffamily.htm':'Send' }
    sendRequest(page, payload)
    print('Deleted all entries')

def lock(user_id, user):
    page = 'form2timelimit.cgi'
    payload = { 'select':'0', 'selectday':'0', 'timefrom':disableTimeFrom, 'timeto':disableTimeTo, 'filtertype':'on', 'src':'', 'end':'', 'mac':user['mac'], 'addFilterTime':'Add', 'submit.htm%3Ffamily.htm':'Send' }
    sendRequest(page, payload)
    print('Locked user: ' + user_id)

def unlock(user_id, user):
    page = 'form2timelimit.cgi'
    payload = { 'select':'0', 'selectday':'1234560', 'timefrom':user['enableTimeFrom'], 'timeto':user['enableTimeTo'], 'filtertype':'on', 'src':'', 'end':'', 'mac':user['mac'], 'addFilterTime':'Add', 'submit.htm%3Ffamily.htm':'Send' }
    sendRequest(page, payload)
    print('Unlocked user: ' + user_id)

def handleControlStatus(command):
    page = 'form2timelimitenable.cgi'

    on_off = '1'
    if command == 'disable':
        on_off = '0'
        
    payload = { 'openoroff': on_off, 'submit.htm%3Ffamily.htm':'Send' }
    r = sendRequest(page, payload)
    print('Parental control ' + command + 'd')

def getTargets(command_target, excluded_devices):
    targets = []
    if command_target == 'all':
        for user in users:
            if excluded_devices and isExcludedDevice(user, excluded_devices):
                continue

            targets.append(user)
    else:
        targets.append(command_target)

    return targets

def handleCommand(command_type, command_target, excluded_devices):
    if command_type == 'lockdown' or command_type == 'unlockdown':
        targets = getTargets(command_target, excluded_devices)
        for target in targets:
            user = users[target]

            if command_type == 'lockdown':
                lock(target, user)
            else:
                unlock(target, user)

        print("Executed " + command_type + " for " + str(targets))
    else:
        handleControlStatus(command_type)

def isExcludedDevice(device_name, excluded_devices):
    excluded_devices = excluded_devices.split(',')
    for excluded in excluded_devices:
        if excluded == device_name:
            return True

    return False

login()
time.sleep(1)

if command_type == 'lockdown' or command_type == 'unlockdown':
    deleteAllEntries()
    time.sleep(1)

handleCommand(command_type, command_target, excluded_devices)
