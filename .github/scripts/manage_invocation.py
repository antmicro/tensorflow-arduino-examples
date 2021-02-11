#!/usr/bin/env python3

import argparse, sys, logging
from distantrs import Invocation

INVOCATION_DETAILS = '/tmp/distant-rs-invocation.txt'

logging.basicConfig(format="[%(asctime)s] %(levelname)-8s| %(message)s")

l = logging.getLogger(__name__)

def get_invocation_details():
    with open(INVOCATION_DETAILS, 'r') as f:
        return f.read().split("--")

def open_i_func(arg):
    i = Invocation()
    i.open()

    l.info(f'ID: {i.invocation_id}')
    l.info(f'Token: {i.auth_token}')

    with open(INVOCATION_DETAILS, 'w') as f:
        f.write(f'{i.invocation_id}--{i.auth_token}')

def close_i_func(arg):
    i_details = get_invocation_details()
    ret = 5 if arg.return_code == 0 else 6

    if len(i_details) != 2:
        l.error(f"Invalid {INVOCATION_DETAILS}!")

    l.info(f'Loaded ID: {i_details[0]}')
    l.info(f'Loaded token: {i_details[1]}')
    l.info(f'Real code: {arg.return_code}')
    l.info(f'Flattened code: {ret}')

    i = Invocation(
            invocation_id=i_details[0],
            auth_token=i_details[1],
            )
    i.update_status(ret)
    i.close()

def url_i_func(arg):
    i_details = get_invocation_details()
    print(f"https://source.cloud.google.com/results/invocations/{i_details[0]}")

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true')
    subparsers = parser.add_subparsers()

    open_i = subparsers.add_parser("open")
    open_i.set_defaults(func=open_i_func)

    close_i = subparsers.add_parser("close")
    close_i.add_argument("return_code", type=int)
    close_i.set_defaults(func=close_i_func)

    url_i = subparsers.add_parser("print_url")
    url_i.set_defaults(func=url_i_func)

    return parser

def main():
    parser = get_parser()

    if (len(sys.argv) == 1):
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.v:
        logging.root.setLevel(logging.INFO)
    else:
        logging.root.setLevel(logging.WARNING)

    args.func(args)

if __name__ == '__main__':
    main()
