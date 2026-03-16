#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def install_bash():
    shell_rc = os.path.expanduser("~/.zshrc") if os.environ.get("ZSH_VERSION") else os.path.expanduser("~/.bashrc")
    custom_rc = os.path.join(REPO_DIR, "bash", "bashrc")
    snippet_check = f"if [ -f {custom_rc} ]; then"
    snippet = f"\nif [ -f {custom_rc} ]; then\n    source {custom_rc}\nfi\n"

    if not os.path.exists(shell_rc):
        open(shell_rc, "w").close()

    with open(shell_rc) as f:
        content = f.read()

    if snippet_check in content:
        print(f"bash: sourcing already present in {shell_rc}, skipping.")
        return

    shutil.copy(shell_rc, shell_rc + ".bak")
    print(f"bash: backed up {shell_rc} to {shell_rc}.bak")

    with open(shell_rc, "a") as f:
        f.write(snippet)
    print(f"bash: added sourcing to {shell_rc}")


def install_git():
    aliases = [
        ("st", "status -s"),
        ("aadd", "add ."),
        ("acommit", "commit -am"),
        ("cleanup", "!git reset --hard && git clean -fd"),
        ("difflog", "!f() { git log \"$1\"..HEAD --pretty=format:\"%h %ad %s\" --date=short -- \"$2\"; }; f"),
    ]
    for name, value in aliases:
        subprocess.run(["git", "config", "--global", f"alias.{name}", value], check=True)
        print(f"git: set alias.{name}")


def install_vim():
    vimrc_src = os.path.join(REPO_DIR, "vim", "vimrc")
    vimrc_dst = os.path.expanduser("~/.vimrc")

    if not os.path.exists(vimrc_src):
        print(f"vim: error: {vimrc_src} not found, aborting.", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(vimrc_dst) and not os.path.islink(vimrc_dst):
        shutil.move(vimrc_dst, vimrc_dst + ".bak")
        print(f"vim: backed up ~/.vimrc to ~/.vimrc.bak")
    elif os.path.islink(vimrc_dst):
        os.remove(vimrc_dst)

    os.symlink(vimrc_src, vimrc_dst)
    print(f"vim: symlink created: ~/.vimrc -> {vimrc_src}")


INSTALLERS = {
    "bash": install_bash,
    "git": install_git,
    "vim": install_vim,
}


def main():
    parser = argparse.ArgumentParser(description="Apply env config to rc files.")
    parser.add_argument("targets", nargs="+", choices=[*INSTALLERS, "all"], help="What to install")
    args = parser.parse_args()

    targets = [*INSTALLERS] if "all" in args.targets else args.targets
    for target in targets:
        INSTALLERS[target]()


if __name__ == "__main__":
    main()
