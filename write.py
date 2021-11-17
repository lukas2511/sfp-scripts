#!/usr/bin/python3

import sys
import os
import smbus
import struct
import collections
import time
import tqdm

def parse_info(flash):
    sfp = collections.namedtuple('SFP', 'type connector encoding bitrate vendor partnumber revision wavelength options upper_bitrate_margin lower_bitrate_margin serial datecode diagnostics checksum2')
    foo = dict(sfp._asdict(sfp._make(struct.unpack(">BxB8xBB7x16s4x16s4sH2xHBB16s8sB2xB32x", bytearray(flash)))))
    for key in foo:
        if isinstance(foo[key], bytes):
            foo[key] = foo[key].decode()
    return foo

BUS = int(sys.argv[1])
bus = smbus.SMBus(BUS)

ROM = open(sys.argv[2], "rb").read()

PIN = bytes.fromhex(sys.argv[3])

info = parse_info(ROM)
print(info)

def unlock(pin):
    if len(pin) != 4:
        print("Invalid pin!")
        sys.exit(1)

    bus.write_byte_data(0x51, 0x7b, pin[0])
    time.sleep(0.1)
    bus.write_byte_data(0x51, 0x7c, pin[1])
    time.sleep(0.1)
    bus.write_byte_data(0x51, 0x7d, pin[2])
    time.sleep(0.1)
    bus.write_byte_data(0x51, 0x7e, pin[3])
    time.sleep(0.1)

unlock(PIN)

flash = []
for i in tqdm.tqdm(range(128)):
    bus.write_byte_data(0x50, i, ROM[i])
    time.sleep(0.1)

verify = []
for i in range(128):
    bus.read_byte_data(0x50, i)

if flash == verify:
    print("Flashing successful")

