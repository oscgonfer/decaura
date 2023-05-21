#!/usr/bin/python

import subprocess
from pythonosc import osc_message_builder
from pythonosc import udp_client
from os import walk, getcwd
import time
import random
import sys, traceback
from sonic_pi_tool import Server

min_time = 40 # in seconds
max_time = 90 # in seconds
fade_out_time = 15

# OSC Sender to Sonic Pi
host = '127.0.0.1'
cmd_port=-4557
osc_port=4560
sender = udp_client.SimpleUDPClient(host, osc_port)
# Songs list
songs = []

for root, dirs, files in walk(getcwd()):
    for file in files:
        if file.startswith('decaura_vol'):
            songs.append(file)

print ("Songs list:")
print (songs)

def song_player():
    print ("Sending global OSC: 1")
    sender.send_message('/global', 1)
    
    print ("Picking new song:")
    current_song = random.choice(songs)
    print (current_song)
    print ("Starting it...")
    subprocess.call(["./sonic_pi_tool.py", "run-file", f"compositions/{current_song}"])
    
    duration = random.randint(min_time, max_time)
    elapsed_time = 0
    
    while elapsed_time < duration:
        time.sleep(1)
        elapsed_time += 1
        print (f"Elapsed time: {elapsed_time}/{round(duration)}(s)")
    sender.send_message('/global', 0)
    time.sleep(fade_out_time)
    subprocess.call(["./sonic_pi_tool.py", "stop"])

def main():
    s = Server(host=host, cmd_port=cmd_port, osc_port=osc_port, send_preamble=False, verbose=False)
    started = 0
    try:
        while True:
            if s.check_if_running():
                time.sleep(5)
                print ("Server is not running. Waiting")
            else:
                if started:
                    song_player()
                else:
                    print ("Sleeping 20s for sonic pi to be stable")
                    time.sleep(20)
                    started = 1
    except KeyboardInterrupt:
        print ("Shutdown requested...exiting")
        subprocess.call(["./sonic-pi-tool.py", "stop"])
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    main()
