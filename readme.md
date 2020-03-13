# cloud_shell_ssh_config

Small script for adding Google Cloud Shell to your SSH config.
Requires gcloud cli tools to be installed.

## Usage

```
usage: cloud_shell_ssh_config.py [-h] [--ssh_config SSH_CONFIG] [--host HOST]

optional arguments:
  -h, --help            show this help message and exit
  --ssh_config SSH_CONFIG
                        Path to SSH config file
  --host HOST           Host name to use/replace in ssh_config file
```

Example:
```
❯ ./cloud_shell_ssh_config.py 

❯ ssh cloud-shell
Welcome to Cloud Shell! Type "help" to get started.
username@cs-6000-devshell-vm-2570685e-de5f-4774-845a-1959d53a1562:~$ 
```

You should re-run every time you start a session - Google will shut down your shell after a period of inactivity.

If you see an error, run `gcloud alpha cloud-shell ssh` directly and make sure it works.

## Why?

- Some applications require that the remote host is configured in your SSH config file (e.g. VS Code).
- Once set up, you can use standard tooling (`ssh`, `scp`) rather than using `gcloud`.
