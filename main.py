#!/usr/env python3

#
#
# Check Modify date for version displayed on menu at runtime, generated from "get_build_date" 
# $ TZ=UTC stat *

#
# duplicate key check in fixes.ini
# $ grep "\[" fixes.ini  | sort | uniq -c | sort -n
#

import os
import argparse
import configparser
import hashlib

FIRMWARE = "firmware.ini"
FIXES = "fixes.ini"

def hashfile(f):
    BUF_SIZE = 65536 
    sha256 = hashlib.sha256()

    with open(f, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def dumpini(d, filename="sfixes.ini"):
    config = False
    config = configparser.ConfigParser()
    for section in d.keys():
        config[section] = {}
        for option in d[section]:
            config[section][option] = str(d[section][option])    
    with open(filename, 'w') as f:
        config.write(f)
    return

def readini(filename="fixes.ini"):
    d = {}
    if os.path.exists(filename):
        config = {}
        config = configparser.ConfigParser()
        config.read(filename)
        # convert to dict, thought there was a proper way to do this
        for section in config.sections():
            d[section] = {}
            for option in config[section]:
                d[section][option] = str(config[section][option])
        return d
    else:
        print(f"File not found: {filename}")
        exit(1)

def main(args):
    if (args.identify_fw):
        if args.fw_path is None or not os.path.exists(args.fw_path):
            print("Couldn't find a valid path with --fw-path")
            exit(1)

        fw = readini(FIRMWARE)
        for root, dirs, files in os.walk(args.fw_path):
            for filename in files:
                abs_path = os.path.join(root, filename)
                filehash = hashfile(abs_path)
                for fwhash in fw.keys():
                    if filehash == fwhash:
                        fwfilename = fw[fwhash]["filename"]
                        fwversion = fw[fwhash]["version"]
                        print(f"Filename: {filename} is {fwfilename} from SAROO firmware version: {fwversion}")
    elif (args.apply_fixes):
        fx = readini(FIXES)
        print(fx)
    elif (args.diff_fixes):
        if args.ini_path is None or not os.path.exists(args.ini_path):
                    print("Couldn't find a valid path with --ini-path")
                    exit(1)
        fx = readini(FIXES)
        fd = readini(args.ini_path)
        diff = list(set(fd.keys()) - set(fx.keys()))
        if len(diff) > 0:
            for item in sorted(diff):
                item_length = len(item)
                if item_length != 16:
                    #print(f" {item} Incorrect Length: {item_length}, padding and checking again")
                    pieces = item.split()
                    padding = ' ' * ( 16 - ( item_length - 1 ) )
                    test_string = padding.join(pieces)
                    if not test_string in fx.keys():
                        print(f" [{test_string}] needs GAME_ID length correction (for firmware v0.05 or less)")
                else:
                    print(f" [{item}]")
        else:
            print("No new entries found")
    elif (args.check_keys):
        fx = readini(FIXES)
        for item in fx.keys():
            if len(item) != 16:
                print(f"Incorrect Length: {item} {len(item)} (for firmware v0.05 or less)")
    else:
        print("Nothing to do!")
        return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='sarooing',
        description='SAROO SEGA Saturn cart basic utils, id fw etc'
    )

    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('-id', '--identify-fw', help="identify firmware", action='store_true')
    modes.add_argument('-df', '--diff-fixes', help="diff ini file to library", action='store_true')
    modes.add_argument('-af', '--apply-fixes', help="generate an ini structure with fixes appropriate to version", action='store_true')
    modes.add_argument('-ck', '--check-keys', help="check keys in library are expected length (16c)", action='store_true')

    parser.add_argument('--fw-path', type=str)
    parser.add_argument('--ini-path', type=str)
    args = parser.parse_args()

    main(args)