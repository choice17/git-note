import subprocess as sp


def run():

    cmd = "app_client"
    pipe = sp.Popen(cmd, stdout=sp.PIPE, shell=1, bufsize=-1)
    print(cmd,"running!")
    while (1):
        l = pipe.stdout.readline()
        if l != b'':
            print("out:", l)
        if pipe.poll() is not None:
            exit("return!")


run()
