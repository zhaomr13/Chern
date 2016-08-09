#!/usr/bin/python

import os
import sys
import Chern as chen

# ------------------------------------------------------------
if __name__ == "__main__" :
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(dest="command", nargs='+', help="list all the projects existing")
    parser.add_argument("--std_command_path", help="standard command output, don't specifiy it if you are only a user")
    args = parser.parse_args()

    return_value = ""
    if args.command[0] == "projects" :
        return_value = chen.projects.main(args.command[1:])

    if args.command[0] == "clean" :
        chen.clean()

    if args.command[0] == "config":
        from subprocess import call
        call("vim " + os.environ["HOME"] + "/.Chern/config.py", shell=True)

    if args.command[0] == "brother":
        pass
    #print args.projects

    if args.command[0] == "start":
        import subprocess
        if os.path.exists(os.environ["HOME"] + "/.Chern/server.closed"):
            os.remove(os.environ["HOME"] + "/.Chern/server.closed")
        subprocess.Popen("python " + os.environ["CHERNSYSROOT"]+"/Chern/server.py", shell=True)

    if args.command[0] == "stop":
        open(os.environ["HOME"] + "/.Chern/server.closed", "a").close()

    if type(return_value) == str :
        std_command_output_file = open(args.std_command_path, "w")
        print "return value is ", return_value
        std_command_output_file.write(return_value)
        std_command_output_file.close()
