
def readFile(name):
    with open(name) as f:
        lines = f.readlines()
        return [l.strip()[3:] for l in lines]