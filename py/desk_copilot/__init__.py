import os
import sys
import subprocess


def get_pip_location():
    result = subprocess.run(['pip', 'show', 'pip'], stdout=subprocess.PIPE)
    lines = result.stdout.decode('utf-8').split('\n')
    return next(
        (
            line.split(': ')[1]
            for line in lines
            if line.startswith('Location: ')
        ),
        None,
    )


for x in sys.path:
    if os.path.isdir(x) and x.endswith("python3.9"):
        sys.path.append(f"{x}/site-packages")

sys.path.append(get_pip_location())

if __name__ == '__main__':

    print(get_pip_location())
