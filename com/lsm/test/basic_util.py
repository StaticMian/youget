import shlex
import subprocess


def exec_command(command, cwd=None, error_keywords=None, print_logs=True):
    print('[EXEC] %s' % command)
    err = 'exec [%s] error.' % command
    cmd = shlex.split(command)
    exec_logs = []
    try:
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
        while True:
            return_code = p.poll()
            line = p.stdout.readline()
            line = str(line.strip(), encoding='utf-8')
            if line:
                exec_logs.append(line)
                if print_logs:
                    print(line)
            if return_code is not None:
                break
        if p.returncode != 0:
            if not print_logs:
                for line in exec_logs:
                    print(line)
            raise RuntimeError(err, error_keywords or "exec_command ERROR")
        return exec_logs
    except OSError as e:
        raise RuntimeError(e)