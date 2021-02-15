#!/usr/bin/env python3

import argparse, sys, os, logging, tempfile, requests
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth
from distantrs import Invocation

INVOCATION_DETAILS = os.path.join(
        tempfile.gettempdir(),
        'distant-rs-invocation.txt'
        )

INVOCATION_URL = "https://source.cloud.google.com/results/invocations/{}"

GITHUB_API_URL = "https://api.github.com"

logging.basicConfig(format="[%(asctime)s] %(levelname)-8s| %(message)s")

l = logging.getLogger(__name__)

def get_invocation_details():
    try:
        with open(INVOCATION_DETAILS, 'r') as f:
            return f.read().replace("\n","").split("--")
    except IOError as e:
        l.error(str(e))
        sys.exit(1)

def get_invocation_from_file():
    i_details = get_invocation_details()

    if len(i_details) != 2:
        l.error(f"Invalid {INVOCATION_DETAILS}!")
        sys.exit(1)

    l.info(f'Loaded ID: {i_details[0]}')
    l.info(f'Loaded token: {i_details[1]}')

    return Invocation(
            invocation_id=i_details[0],
            auth_token=i_details[1],
            )

def gh_checks_func(arg):
    i = get_invocation_from_file()
    i_proto = i.invocation_viewer.get_invocation()

    repo = arg.repo or os.environ.get("GITHUB_REPOSITORY")
    sha = arg.sha or os.environ.get("GITHUB_SHA")
    ctx = arg.ctx

    u = arg.user or os.environ.get("GH_SERVICE_ACCOUNT_NAME")
    p = arg.token or os.environ.get("GH_SERVICE_ACCOUNT_TOKEN")

    status_mapping = {
            1: "pending",
            5: "success",
            6: "failure",
            9: "error",
    }

    json_body = {
            "state": status_mapping[i_proto.status_attributes.status],
            "target_url": INVOCATION_URL.format(i.invocation_id),
            "context": "Build Results",
    }

    post_url = urljoin(GITHUB_API_URL, f'/repos/{repo}/statuses/{sha}')

    r = requests.post(
            post_url,
            json=json_body,
            auth=HTTPBasicAuth(u, p)
            )
    r.raise_for_status()

def open_i_func(arg):
    i = Invocation()
    i.open(timeout=arg.timeout)

    l.info(f'ID: {i.invocation_id}')
    l.info(f'Token: {i.auth_token}')
    l.info(f'Timeout: {arg.timeout}')

    with open(INVOCATION_DETAILS, 'w') as f:
        f.write(f'{i.invocation_id}--{i.auth_token}')

def close_i_func(arg):
    i = get_invocation_from_file()
    ret = 5 if arg.return_code == 0 else 6

    l.info(f'Real code: {arg.return_code}')
    l.info(f'Flattened code: {ret}')

    i.update_status(ret)
    i.close()

def upload_log_func(arg):
    i = get_invocation_from_file()
    i.send_file('build.log', arg.file)

def url_i_func(arg):
    i_details = get_invocation_details()
    print(INVOCATION_URL.format(i_details[0]))

def get_parser():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda a: parser.print_help())
    parser.add_argument('-v', action='store_true', help="verbose logging")
    subparsers = parser.add_subparsers()

    open_i = subparsers.add_parser("open", help="create a new invocation")
    open_i.add_argument("--timeout", type=int, help="time in minutes after which the invocation will be automatically finalized", default=30)
    open_i.set_defaults(func=open_i_func)

    close_i = subparsers.add_parser("close", help="finalize the invocation")
    close_i.add_argument("return_code", type=int)
    close_i.set_defaults(func=close_i_func)

    upload_log = subparsers.add_parser("upload_log", help="upload main invocation log")
    upload_log.add_argument("file", type=str)
    upload_log.set_defaults(func=upload_log_func)

    url_i = subparsers.add_parser("print_url", help="print the invocation URL")
    url_i.set_defaults(func=url_i_func)

    gh_checks = subparsers.add_parser("gh_checks", help="create a commit status from invocation")
    gh_checks.add_argument("--user", type=str, help="GitHub username")
    gh_checks.add_argument("--token", type=str, help="GitHub Personal Access Token")
    gh_checks.add_argument("--repo", type=str, help="full repository slug")
    gh_checks.add_argument("--sha", type=str, help="commit SHA")
    gh_checks.add_argument("--ctx", type=str, default="Build Results", help="status context")
    gh_checks.set_defaults(func=gh_checks_func)

    inv_file = subparsers.add_parser("file_location", help="get location of invocation details file")
    inv_file.set_defaults(func=lambda a: print(INVOCATION_DETAILS))

    return parser

def main():
    parser = get_parser()

    args = parser.parse_args()

    if args.v:
        logging.root.setLevel(logging.INFO)
    else:
        logging.root.setLevel(logging.WARNING)

    args.func(args)

if __name__ == '__main__':
    main()
