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

    print args.command
    if args.command[0] == "projects" :
        if len(args.command) == 1 :
            chen.projects.main(None)
        else :
            chen.projects.main(args.command[1])

    if args.command[0] == "clean" :
        chen.clean()

    if args.command[0] == "config":
         chen.Popen()

    if args.command[0] == "brother":
        pass
    #print args.projects
    #std_command_output_file = open(args.std_command_path, "w")
    #std_command_output_file.close()
