#! /usr/bin/python3

import os
import getpass
import csv
import time
import netmiko
import paramiko
import sys
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from getpass import getpass
from pprint import pprint
from netmiko import ConnectHandler


snmpv3_update = ['snmp-server group <snmp_username> v3 auth', 'snmp-server group <snmp_groupname> v3 auth notify <notify-view-name>', 'snmp-server view <notify-view-name> internet included', 'snmp-server view <notify-view-name> mib-2 included', 'snmp-server view <notify-view-name> system included', 'snmp-server view <notify-view-name> interfaces included', 'snmp-server view <notify-view-name> chassis included', 'snmp-server host <snmp_host> version 3 auth <snmp_username>', 'snmp-server host <snmp_host> version 3 auth <snmp_user>', 'snmp-server host <snmp_host> version 3 auth <snmp_username>', 'snmp-server user <snmp_username> <snmp_groupname> v3 auth sha <auth_pw> priv aes 128 <enc_pw> access <SNMP_ACL>']





numerical_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']     # Look for lines that start with integer only (IP Addresses)

with open("SNMPv3_Hosts.txt", "r") as r:              # Hostfile with Cisco devices to be updated
    for line in r:
        if line[0] in numerical_list:
            line = line.split()     # create an indexed list separated by spaces, so that first term in list is the IP address of device
            Host = {
                'device_type': 'cisco_ios',
                'ip': line[0],
                'username': '<username>',
                'password': '<password>',
                'port': 22
            }
            try:
                ssh_connect = ConnectHandler(**Host)
                ssh_connect.enable()
                result = ssh_connect.send_config_set(snmpv3_update)            # send snmpv3 commands to device
                print(result)
            except(AuthenticationException):
                print('Authentication Failure: ' + line[1])
            except(NetMikoTimeoutException):
                print('Timeout to device: ' + line[1]) 
            except(SSHException):
                print('SSH may not be enabled, check config on: ' + line[1])
