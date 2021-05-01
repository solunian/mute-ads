import subprocess

def get_computername():
    return subprocess.check_output(["scutil", "--get", "ComputerName"]).decode()[:-1]