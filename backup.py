#!/usr/bin/python3

import sys
import os
import smbus
import struct
import collections

def parse_info(flash):
    sfp = collections.namedtuple('SFP', 'type connector encoding bitrate vendor partnumber revision wavelength options upper_bitrate_margin lower_bitrate_margin serial datecode diagnostics checksum2')
    foo = dict(sfp._asdict(sfp._make(struct.unpack(">BxB8xBB7x16s4x16s4sH2xHBB16s8sB2xB32x", bytearray(flash)))))
    for key in foo:
        if isinstance(foo[key], bytes):
            foo[key] = foo[key].decode()
    return foo

BUS = int(sys.argv[1])
bus = smbus.SMBus(BUS)

flash = []
for i in range(128):
    flash.append(bus.read_byte_data(0x50, i))

info = parse_info(flash)
vendor = info['vendor'].strip()

if not os.path.exists("backups/%s" % vendor):
    os.mkdir("backups/%s" % vendor)

print(info)
open("backups/%s/%s.bin" % (vendor, info['partnumber']), "wb").write(bytes(flash))




