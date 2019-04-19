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
    print('{} {} minutes have passed'.format(datetime.datetime.now(), interval))
    ts = today_string()
    prev = data.get(ts, 0)
    data[ts] = prev + interval

def read_log(fname):
    try:
        with open(fname, 'r') as l:
            return json.load(l)
    except:
        return {'program_name': 'vigilant', 'data': {}}

def write_log(log, fname):
    try:
        with open(fname, 'w') as l:
            l.write(json.dumps(log, indent=2, sort_keys=True))
    except:
        print('Could not write to log: ' + LOG_FILE)
        sys.exit(1)

def today_string():
    return datetime.datetime.now().strftime(DATE_FORMAT)

def sort_keys(data):
    return sorted(data.keys(), key=lambda s: datetime.datetime.strptime(s, DATE_FORMAT))

def print_table(data):
    if not data:
        print('no data to display')
        return

    horz = '+' + '-'*(len(today_string()) + 2) + '+' + \
             '-'*(len('00h00m')+2) + '+'
    def table_time(mins):
        return '{:02d}h{:02d}m'.format(mins // 60, mins % 60)
    def row(l, r, mins):
        print('| {} | {} | {} '.format(l, r, '*' * (mins // 30)))
    
    total = 0
    for key in sort_keys(data):
        print(horz)
        mins = data[key]
        total = total + mins
        row(key, table_time(mins), mins)
    print(horz)
    print('avg: ' + table_time(total // len(data)))



def main(args):
    log = read_log(LOG_FILE)

    if args.interval is not None:
        add_checkpoint(log['data'], args.interval)
        write_log(log, LOG_FILE)
    elif args.disp_log:
        print(LOG_FILE)
    else:
        print_table(log['data'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action='store_true', dest='disp_log', help='display the path to the log file')
    parser.add_argument('--checkpoint', type=int, dest='interval', help='number of minutes between checkpoints')
    args = parser.parse_args()
    main(args)
