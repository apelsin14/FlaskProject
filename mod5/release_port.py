import os
import signal
import subprocess

HOST = "127.0.0.1"
port = int(input())


def run_program():
    port = int(input())
    res = subprocess.run(['lsof', '-i', f':{port}'], input=b'some input\notherinput')
    os.kill(int(str(res)), signal.SIGTERM)

    print(res)


if __name__ == '__main__':
    run_program()
