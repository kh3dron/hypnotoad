import sys
import threading
import paramiko
import subprocess
import getopt


def usage():
    print("""
    [*] Welcome to Hypnotoad.
    [*] The power of about 30 shitty workstations at your fingertips.
    [*] run with: python3.6 hypnotoad.py 'command1' 'command2' onwards.
    """)

def main():
    if ((len(sys.argv))< 2):
        usage()
        exit(0)

    #"Guest" accounts, always logged in
    username = "student"
    password = "student"

    for g in (range(1, len(sys.argv))):
        linuxlab(username, password, sys.argv[g])


def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(ip, username=user, password=passwd)
      
    except (BadHostKeyException, AuthenticationException,
        SSHException, socket.error) as e:
        print(e)
        return
    
    ssh_session = client.get_transport().open_session()
    
    if ssh_session.active:
        ssh_session.exec_command(command)
        return ((ssh_session.recv(1024)).decode("utf-8"))
    else:
        return "[*] SSH session failed."

def linuxlab(username, password, command):
    print("Running ", command, " on [30] machines")

    for r in range(1, 31):
        hostname = "simpson" + str(r)

        try:
            res = (ssh_command(hostname, username, password, command))[:-1]
            if r < 10:
                hostname += " "
            print(hostname + ":   " + res)
            
        except Exception as e:
            print("[***] ERROR: Can't reach "+ hostname)

if __name__ == '__main--':
    main()
