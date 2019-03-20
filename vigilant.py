#!/usr/bin/env python3

'''
Objectives
----------
1. Make the checkpoints as light as possible.
2. Provide good graphical output
'''

import argparse
import datetime
import sys
import json


DATE_FORMAT = '%a %b %d %Y'     # 'Sun Mar 17 2019'
LOG_FILE = '/Users/briantracy/Desktop/projects/vigilant/file.json'

def add_checkpoint(data, interval):
    ts = today_string()
    prev = data.get(ts, 0)
    data[ts] = prev + interval

def read_log(fname):
    with open(fname, 'r') as l:
        try:
            return json.load(l)
        except Exception:
            return {'program_name': 'vigilant', 'data': {}}

def write_log(log, fname):
    with open(fname, 'w') as l:
        try:
            l.write(json.dumps(log, indent=2, sort_keys=True))
        except:
            print('Could not write to log: ' + LOG_FILE)
            sys.exit(1)

def today_string():
    return datetime.datetime.now().strftime(DATE_FORMAT)

def error(log, msg):
    log['error'] = msg
    write_log(log, LOG_FILE)
    sys.exit(1)

def print_table(log):
    horz = '+' + '-'*(len(today_string()) + 2) + '+' + \
             '-'*(len('00h00m')+2) + '+'
    def table_time(mins):
        return '{:02d}h{:02d}m'.format(mins // 60, mins % 60)
    def row(l, r):
        print('| {} | {} |'.format(l, r))

    print(horz)
    for key in sorted(log['data'].keys()):
        row(key, table_time(log['data'][key]))
        print(horz)

def main(args):
    log = read_log(LOG_FILE)

    
    if args.interval:
        add_checkpoint(log['data'], args.interval)
        log['error'] = ''
        write_log(log, LOG_FILE)
    elif args.disp_log:
        print(LOG_FILE)
    else:
        print_table(log)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action='store_true', dest='disp_log', help='display the path to the log file')
    parser.add_argument('--checkpoint', type=int, dest='interval', help='number of minutes between checkpoints')
    args = parser.parse_args()
    main(args)
