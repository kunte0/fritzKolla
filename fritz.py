#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fritzconnection as fc
import sys
import time
from datetime import datetime, timedelta


ADDRESS = 'fritz.box'
PASSWORD = 'yourpassword'

HELP = '[?] arguments: info/status, reconnect, hosts, api, logs, reboot'


if(len(sys.argv) != 2):
    print(HELP)
    exit(1)


print('''
  ______    _ _
 |  ____|  (_) |
 | |__ _ __ _| |_ ____
 |  __| '__| | __|_  /
 | |  | |  | | |_ / /
 |_|  |_|  |_|\__/___|

''')
print('[+] Connecting to "{}" ... '.format(ADDRESS))
c = fc.FritzConnection(address=ADDRESS, password=PASSWORD)

# check connection by getting DeviceInfo
try:
    print('[+] Connected to ', c.call_action('DeviceInfo:1', 'GetInfo')['NewModelName'])
except Exception as e:
    print('[-] Could not connect!')
    exit(1)


if sys.argv[1] == 'info' or sys.argv[1] == 'status':
    status = c.call_action('WANIPConn:1', 'GetStatusInfo')
    print('Status  ', status['NewConnectionStatus'])
    print('Uptime  ', str(timedelta(seconds=status['NewUptime'])))
    print('IP      ', c.call_action('WANIPConn:1','X_AVM_DE_GetExternalIPv6Address')['NewExternalIPv6Address'])
    print('Dslite  ', c.call_action('WANCommonIFC:1', 'X_AVM_DE_GetDsliteStatus')['NewX_AVM_DE_DsliteStatus'])


elif sys.argv[1] == 'reconnect':
    print('[+] Reconnecting ...')
    c.reconnect()


elif sys.argv[1] == 'reboot':
    print('[+] Rebooting ...')
    c.call_action('DeviceConfig:1', 'Reboot')
    print('[+] done!')


elif sys.argv[1] == 'hosts':
    print('[+] Getting Hosts:')
    numHosts = c.call_action('Hosts:1', 'GetHostNumberOfEntries')['NewHostNumberOfEntries']

    for i in range(numHosts):
        host = c.call_action('Hosts:1', 'GetGenericHostEntry', NewIndex=i)
        hostname = host['NewHostName']
        hostip = host['NewIPAddress']
        if host['NewActive'] == '1' and hostip and hostname != 'fritz.box':
            print(hostname, ' === ', hostip)


elif sys.argv[1] == 'logs' or sys.argv[1] == 'log':
    print('[+] Getting Logs:')
    logs = c.call_action('DeviceInfo:1', 'GetDeviceLog')['NewDeviceLog']
    # reverse order
    for line in reversed(logs.split('\n')):
        print(line)


elif sys.argv[1] == 'api':
    fc.print_api(address=ADDRESS, password=PASSWORD)


else:
    print(HELP)
