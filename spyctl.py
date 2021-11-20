import argparse
import json
from sys import exit

__version__="1.0.0"
__author__="NurTasin"
__appname__="spyctl"
__repo__="https://github.com/NurTasin/instaspy"

if __name__=="__main__":
    parser=argparse.ArgumentParser(prog="spyctl")
    parser.add_argument("-a","--add-targets",help="Target's Instagram handle. Separated by white space.",action="store")
    parser.add_argument("-r","--remove-targets",help="Removes targets from target list. Separated by white space.",action="store")
    parser.add_argument("-d","--delay",help="Delay between 2 scan cycles",action="store")
    parser.add_argument("-u","--username",help="Username handle to login",action="store")
    parser.add_argument("-I","--init",help="Initializes the spy for first time (user interactive)",action="store_true")
    parser.add_argument("-U","--enable-update",help="Updates the targets instagram account instead of downloading the whole account",action="store_true")
    parser.add_argument("-dU","--disable-update",help="Everytime the spy downloads the whole instagram account",action="store_true")
    parser.add_argument("-C","--enable-comment",help="Downloads the comments also for every post.",action="store_true")
    parser.add_argument("-dC","--disable-comment",help="Disables downloading the comments for posts.",action="store_true")
    args=parser.parse_args()
    if args.init:
        uname=input("Username: ")
        targets=[]
        c=1
        print("Enter targets Instagram handle. (leave blank to complete)")
        while True:
            i=input(f"[{c}]: ")
            if not i=="":
                targets.append(i)
            else:
                break
            c+=1
        del c
        update=input("Enable Update? [Y/n] : ") in ["","y","Y"]
        comments=input("Enable Fetching Comments? [y/N] : ") in ["y","Y"]
        delay=int(input("Delay in seconds [1800]: ") or 1800)
        with open("./conf.json","w+") as handle:
            json.dump(fp=handle,obj={
                "login-data":{
                    "username":uname
                },
                "targets":targets,
                "update":update,
                "fetch-comments":comments,
                "delay":delay
            },indent=4)
        print("Done!\nChanges will take place from the next scan cycle.")
        exit(0)
    else:
        try:
            with open("./conf.json") as handle:
                try:
                    conf=json.load(handle)
                except json.decoder.JSONDecodeError:
                    with open("./conf.json","w+") as handle2:
                        json.dump({
                            "login-data":{
                                "username":""
                            },
                            "targets":[],
                            "delay":1800,
                            "update":True,
                            "fetch-comments":False
                        },handle2)
                    conf=json.load(handle)
        except FileNotFoundError:
            conf={
                "login-data":{
                    "username":""
                },
                "targets":[],
                "delay":0,
                "update":True,
                "fetch-comments":False
            }
        
        changed=False
        if args.add_targets:
            targets=str(args.add_targets).split(' ')
            for target in targets:
                if target in conf["targets"]:
                    print(f"Target {target} is already present in the targets' list.")
                else:
                    conf["targets"].append(target)
                    changed=True

        if args.remove_targets:
            targets=str(args.remove_targets).split(' ')
            for target in targets:
                if target in conf["targets"]:
                    conf["targets"].remove(target)
                    changed=True
                else:
                    print(f"Target {target} is not present in the targets' list.")

        if args.delay:
            try:
                conf["delay"]=int(args.delay)
            except ValueError:
                print(f"Delay must be a number. Can't convert `{args.delay}` to a base 10 number.")
                exit(1)
            changed=True

        if args.username:
            conf["login-data"]["username"]=args.username
            changed=True

        if args.enable_update and args.disable_update:
            print("Unwanted user activity detected!!\nTold to enable and disable update at the same time!")

        if args.enable_update:
            conf["update"]=True
            changed=True

        if args.disable_update:
            conf["update"]=False
            changed=True

        if args.enable_comment and args.disable_comment:
            print("Unwanted user activity detected!!\nTold to enable and disable downloading comments at the same time!")
        
        if args.enable_comment:
            conf["fetch-comments"]=True
            changed=True

        if args.disable_comment:
            conf["fetch-comments"]=False
            changed=True
        if changed:
            with open("./conf.json","w+") as handle:
                json.dump(conf,handle,indent=4)
                print("Success! Changes will take place from the next scan cycle.")
        
        if (not args.add_targets) and (not args.remove_targets) and (not args.delay) and (not args.username) and (not args.enable_update) and (not args.disable_update) and (not args.enable_comment) and (not args.disable_comment):
            print(f"spyctl.py\nVersion: {__version__}\nAuthor: {__author__}\nRepo: {__repo__}")