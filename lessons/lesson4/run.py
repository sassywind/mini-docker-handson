""" Lesson4: リソースを制御してみよう
$ ./mini-docker run echo hello world
"""
import os
import subprocess
import linux
from cgroups import cgroup
import uuid
from typing import List

class CGroup:
    name: str
    cg: cgroup.Cgroup

    def __init__(self, name: str):
        self.name = name
        self.cg = cgroup.Cgroup(name)

    def add(self, pid: int):
        self.cg.add(pid)

    def set_cpu_limit(self, limit: float):
        if 'cpu' in self.cg.cgroups:
            cpu_period_file = self.cg._get_cgroup_file('cpu', 'cpu.cfs_period_us')
            cpu_quota = self.cg._get_cgroup_file('cpu', 'cpu.cfs_quota_us')

            print(cpu_period_file)
            print(cpu_quota)

            with open(cpu_period_file) as period_f, open(cpu_quota, 'w') as quota_f:
                period = int(period_f.read())
                quota = int(period * limit)
                quota_f.write(f'{quota}')
        else:
            raise cgroup.CgroupsException('CPU hierarchy not available in this cgroup')

def pre_exec(container_id: str, cpus: float, command: List[str]):
    pid = os.getpid()
    print(f"in container process ID: {pid}")

    # hostnameの設定
    print(f'set hostname {container_id}')
    linux.sethostname(container_id)

    # control group の設定
    print(f'set control group')
    cg = CGroup(container_id)
    cg.set_cpu_limit(cpus)
    cg.add(pid)
    print(f"cgs_pids: {cg.cg.pids}")
    print(f"cg.name: {cg.name}")

    try:
        os.execvp(command[0], command)
    except Exception as e:
        exit(1)


def exec_run(cpus: float, command: List[str]):
    print(f"options: \n cpu = {cpus}, command = {command}")

    # コンテナID
    container_id = str(uuid.uuid4())

    flags = (
        linux.CLONE_NEWPID |  # PID名前空間: プロセスIDの分離。異なる名前空間同士では、同一のプロセスIDを持つことが可能になる
        linux.CLONE_NEWUTS |  # UTS名前空間: ホスト名, ドメイン名の分離
        linux.CLONE_NEWNS  # マウント名前空間: ファイルシステムのマウントポイントの分離
    )
    pid = linux.clone(pre_exec, flags, (container_id, cpus, command))
    print(f'container process ID: {pid}')

    (_, status) = os.waitpid(pid, 0)
    print(f'{pid} exited with status {status}')
