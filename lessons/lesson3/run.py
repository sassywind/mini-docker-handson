""" Lesson3: 子プロセスでpidを出力して、確認してみよう
$ ./mini-docker run echo hello world
"""
import os
import linux
from typing import List

def pre_exec(option: str, command: List[str]):

    pid = os.getpid()
    print(f"in container process ID: {pid}")

    print(option)
    try:
        os.execvp(command[0], command)
    except Exception as e:
        exit(1)

def exec_run(command):
    flags = (
        linux.CLONE_NEWPID # PID名前空間: プロセスIDの分離。異なる名前空間同士では、同一のプロセスIDを持つことが可能になる
    )
    option = "non_option"
    pid = linux.clone(pre_exec, flags, (option, command))
    print(f'container process ID: {pid}')

