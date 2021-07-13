import linux

def pre_exec(arg1: str, arg2: int):
    try:
        print(arg1)
        print(arg2)
    except Exception as e:
        exit(1)

def exec_run():
    flags = (
            linux.CLONE_NEWPID |  # PID名前空間: プロセスIDの分離。異なる名前空間同士では、同一のプロセスIDを持つことが可能になる
            linux.CLONE_NEWUTS |  # UTS名前空間: ホスト名, ドメイン名の分離
            linux.CLONE_NEWNS |  # マウント名前空間: ファイルシステムのマウントポイントの分離
            linux.CLONE_NEWNET  # ネットワーク名前空間: 分離されたネットワークスタックを提供する
    )

    print(f'run command called!')
    linux.clone(pre_exec, flags, ("test", 1))
