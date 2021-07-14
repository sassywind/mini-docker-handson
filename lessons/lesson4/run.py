""" Lesson4: リソースを制御してみよう
$ ./mini-docker run echo hello world
"""
import os
import linux
import cgroups
import uuid
from typing import List

def pre_exec(cpus: int, command: List[str]):

    pid = os.getpid()
    print(f"in container process ID: {pid}")

    # control group の設定
    print(f'set control group')
    container_id = uuid.uuid4()
    cg = cgroups.Cgroup(container_id)
    cg.set_cpu_limit(cpus)
    cg.add(pid)

    try:
        os.execvp(command[0], command)
    except Exception as e:
        exit(1)

def exec_run(cpus: int, command: List[str]):

    print(f"options: \n cpu = {cpus}, command = {command}")

    flags = (
        linux.CLONE_NEWPID # PID名前空間: プロセスIDの分離。異なる名前空間同士では、同一のプロセスIDを持つことが可能になる
    )
    pid = linux.clone(pre_exec, flags, (cpus, command))
    print(f'container process ID: {pid}')
