#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fritzconnection as fc
from datetime import timedelta
import click


ADDRESS = 'fritz.box'
PASSWORD = ''

# print header
print('''
  ______    _ _
 |  ____|  (_) |
 | |__ _ __ _| |_ ____
 |  __| '__| | __|_  /
 | |  | |  | | |_ / /
 |_|  |_|  |_|\__/___|

''')


@click.group()
# @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
def main(password=PASSWORD):
    """
    Small python script to talk to your fritzbox
    """
    global c
    print('[+] Connecting to "{}" ... '.format(ADDRESS))
    c = fc.FritzConnection(address=ADDRESS, password=password)

    # check connection by getting DeviceInfo
    try:
        print('[+] Connected to ', c.call_action('DeviceInfo:1', 'GetInfo')['NewModelName'])
    except Exception as e:
        print('[-] Could not connect!')
        print(e)
        exit(1)


@main.command()
def info():
    '''
    Get basic info
    '''
    status = c.call_action('WANIPConn:1', 'GetStatusInfo')
    link = c.call_action('WANCommonIFC', 'GetCommonLinkProperties')
    print('Status        ', status['NewConnectionStatus'])
    print('Provider Link ', link['NewPhysicalLinkStatus'])
    print('Dslite        ', c.call_action('WANCommonIFC:1', 'X_AVM_DE_GetDsliteStatus')['NewX_AVM_DE_DsliteStatus'])
    print('Access Type   ', link['NewWANAccessType'])
    print('Uptime        ', str(timedelta(seconds=status['NewUptime'])))
    print('IPv6          ', c.call_action('WANIPConn:1', 'X_AVM_DE_GetExternalIPv6Address')['NewExternalIPv6Address'])
    print('IPv4          ', c.call_action('WANIPConn:1', 'GetExternalIPAddress')['NewExternalIPAddress'])
    print('Down Rate     ', link['NewLayer1DownstreamMaxBitRate'] / 1000000)
    print('Up Rate       ', link['NewLayer1UpstreamMaxBitRate'] / 1000000)


@main.command()
def reconnect():
    '''
    Reconnect your fritzbox, get new ip
    '''
    print('[+] Reconnecting ...')
    c.reconnect()


@main.command()
def reboot():
    '''
    Reboot your fritzbox
    '''
    print('[+] Rebooting ...')
    c.call_action('DeviceConfig:1', 'Reboot')
    print('[+] done!')


@main.command()
def hosts():
    '''
    List all active network clients
    '''
    print('[+] Getting Hosts:')
    numHosts = c.call_action('Hosts:1', 'GetHostNumberOfEntries')['NewHostNumberOfEntries']

    for i in range(numHosts):
        host = c.call_action('Hosts:1', 'GetGenericHostEntry', NewIndex=i)

        if host['NewActive'] and host['NewHostName'] != 'fritz.box':
            print(host['NewHostName'], '==', host['NewIPAddress'], '==', host['NewInterfaceType'])


@main.command()
def logs():
    '''
    Print logs
    '''
    print('[+] Getting Logs:')
    logs = c.call_action('DeviceInfo:1', 'GetDeviceLog')['NewDeviceLog']
    # reverse order
    for line in reversed(logs.split('\n')):
        print(line)


if __name__ == '__main__':
    main()
