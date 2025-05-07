import subprocess
import re

# Path to your version file
VERSION_FILE = "version.txt"

def get_current_version():
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

def bump_version(version):
    parts = list(map(int, version.split(".")))
    parts[-1] += 1  # bump patch
    return ".".join(map(str, parts))

def update_version_file(new_version):
    with open(VERSION_FILE, "w") as f:
        f.write(new_version)

def git_commit_and_push(new_version):
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"version {new_version}"], check=True)
    subprocess.run(["git", "push", "-u", "groupify", "main"], check=True)

def main():
    current = get_current_version()
    new_version = bump_version(current)
    update_version_file(new_version)
    print(f"Updated version: {current} → {new_version}")
    git_commit_and_push(new_version)

if __name__ == "__main__":
    main()
