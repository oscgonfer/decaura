#!/usr/bin/python

import time
import asyncio
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from threading import current_thread
from queue import Queue
from typing import List, Any
import RPi.GPIO as GPIO
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
GPIO.setup(LED_PIN, GPIO.OUT)

SERVER_IP = "decaura.local"
SERVER_PORT = 6005
UDP_FILTER = "/hello/*"

def std_out(msg, who):
    print (f'[{who}]: {msg}')

# Run this to make a forever loop with no sleep
async def loop():
    while True:
        # This can't be 0, as it will load the cpu like crazy...
        await asyncio.sleep(0.001)

class UDPBridge(object):
    def __init__(self):
        super(UDPBridge, self).__init__()

    async def main(self, dispatcher):

        server = AsyncIOOSCUDPServer((SERVER_IP, SERVER_PORT), dispatcher,
                                     asyncio.get_event_loop())
        # Create datagram endpoint and start serving
        transport, protocol = await server.create_serve_endpoint()

        await loop()
        transport.close()  # Clean up serve endpoint

    def send(self, *args: List[Any]) -> None:
        std_out (f'{time.strftime("%H:%M:%S %d-%m-%Y")}: {args[0]}\n', 'SACN')
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(LED_PIN, GPIO.LOW)
        

udpbridge = UDPBridge()
dispatcher = Dispatcher()
# Filter OSC messages by "/leds"
dispatcher.map(UDP_FILTER, udpbridge.send)
# Run main loop
asyncio.run(udpbridge.main(dispatcher))
