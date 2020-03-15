#!/usr/bin/env python

import subprocess
import shlex
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--ssh_config', help='Path to SSH config file', default='~/.ssh/config')
parser.add_argument('--host', help='Host name to use/replace in ssh_config file', default='cloud-shell')
args = parser.parse_args()

cloud_shell_output = subprocess.run(['gcloud', 'alpha', 'cloud-shell', 'ssh', '--boosted', '--dry-run'], 
    stdout=subprocess.PIPE, check=True).stdout.decode()

cs_parser = argparse.ArgumentParser()
cs_parser.add_argument('-p', '--Port')
cs_parser.add_argument('-i', '--IdentityFile')
cs_parser.add_argument('-o', '--options', action='append')
cs_parser.add_argument('-t', '--tty', action='store_true')
cs_parser.add_argument('command')
cs_parser.add_argument('destination')
cs_args, _ = cs_parser.parse_known_args(shlex.split(cloud_shell_output))

# Barely adequate SSH config file parsing
file_path = os.path.abspath(os.path.expanduser(args.ssh_config))
new_file = []
try:
    in_section = False
    with open(file_path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.strip().startswith('Host '):
                if line.strip().split(maxsplit=1)[1] == args.host:
                    in_section = True
                else:
                    in_section = False
            if not in_section:
                new_file.append(line.rstrip('\n'))
except FileNotFoundError:
    pass

TAB = '    '
if len(new_file) and new_file[-1].strip() != '':
    new_file.append('')
new_file.append(f'Host {args.host}')
for k, v in vars(cs_args).items():
    # Plain option
    if k[0].isupper():
        new_file.append(f'{TAB}{k} {v}')
    elif k == 'options':
        for opt in v:
            new_file.append(TAB + opt)
    elif k == 'destination':
        items = v.split('@')
        if len(items) == 2:
            new_file.append(f'{TAB}User "{items[0]}"')
            host = items[1]
        else:
            host = items[0]
        new_file.append(f'{TAB}HostName "{host}"')

with open(file_path, 'w') as f:
    f.write('\n'.join(new_file) + '\n')
