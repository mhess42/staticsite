import os
import shutil

static = 'static/'
def move_static(dir):
    for node in os.listdir(dir):
        path = os.path.join(dir, node)
        if os.path.isfile(path):
            shutil.copy(path, path.replace('static/', 'public/'))
        else:
            os.mkdir(path.replace('static/', 'public/'))
            move_static(path)


def main():
    move_static(static)
    return 

main()