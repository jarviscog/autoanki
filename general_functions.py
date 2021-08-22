import os

def file_len(fname):
    with open(fname, encoding='utf-8') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def file_exists(filename):
    if os.path.exists(filename):
        return True
    else:
        return False