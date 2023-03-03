"""
Description:
    Name: RamadanTime
    Tool: Ramadan Time Table Setup for Bangladeshi Termux Users
    Author: ToxicNoob Inc.
    GitHub: https://github.com/toxic-noob/
    Version: 2.0
"""

import os
import sys
import time
import json
import shutil
import subprocess as sb

# Const
home = "/data/data/com.termux/files/home"
binPath = "/data/data/com.termux/files/usr/bin"
sitePkg = "/data/data/com.termux/files/usr/lib/python3.11/site-packages"

columns = shutil.get_terminal_size().columns

# Logo
def logo():
    os.system("clear")
    print("\033[94m┌────────────────────────────────────────┐".center(columns+5))
    print("\033[94m│ \033[92m▛▀▖            ▌        ▞▀▖   ▐      \033[94m  │".center(columns+15))
    print("\033[94m│ \033[92m▙▄▘▝▀▖▛▚▀▖▝▀▖▞▀▌▝▀▖▛▀▖▄▄▚▄ ▞▀▖▜▀ ▌ ▌▛▀▖\033[94m│".center(columns+15))
    print("\033[94m│ \033[92m▌▚ ▞▀▌▌▐ ▌▞▀▌▌ ▌▞▀▌▌ ▌  ▖ ▌▛▀ ▐ ▖▌ ▌▙▄▘\033[94m│".center(columns+15))
    print("\033[94m│ \033[92m▘ ▘▝▀▘▘▝ ▘▝▀▘▝▀▘▝▀▘▘ ▘  ▝▀ ▝▀▘ ▀ ▝▀▘▌  \033[94m│".center(columns+15))
    print("\033[94m│                              \033[94m          │".center(columns+10))
    print("\033[94m│ \033[95mAuthor : ToxicNoob Inc.                \033[94m│".center(columns+15))
    print("│ \033[95mTool   : Ramadan Time-Table Setup      \033[94m│".center(columns+10))
    print("│ \033[95mGitHub : https://github.com/Toxic-Noob \033[94m│".center(columns+10))
    print("│ \033[95mCoder  : HunterSl4d3              V2.0 \033[94m│".center(columns+10))
    print("\033[94m└────────────────────────────────────────┘".center(columns+5))

# Get user District
def getDistrict():
    districtList = json.loads(open("ramadan/districtList.json", "r").read()).get("data")
    print("\n    \033[37m[\033[92m*\033[37m] Please Select Your District from Below:\n")
    
    for i in range(0, 32):
        dis_01 = districtList[i]
        dis_02 = districtList[i+32]
        
        if (len(dis_01) < 7):
            print(f"    [\033[92m{(str(i+1) if (len(str(i+1)) > 1) else '0' + str(i+1))}\033[37m] {dis_01}\t\t[\033[92m{i+33}\033[37m] {dis_02}")
        elif (len(dis_01) < 14):
            print(f"    [\033[92m{(str(i+1) if (len(str(i+1)) > 1) else '0' + str(i+1))}\033[37m] {dis_01}\t[\033[92m{i+33}\033[37m] {dis_02}")
        else:
            print(f"    [\033[92m{(str(i+1) if (len(str(i+1)) > 1) else '0' + str(i+1))}\033[37m] {dis_01}\t[\033[92m{i+33}\033[37m] {dis_02}")
    
    print("\n    [\033[92m00\033[37m] Exit")
    
    op = input("\n    [\033[92m*\033[37m] Enter your District\033[92m:> \033[37m")
    if not (op=="") and not (op == "0"):
        if (op[0] == "0"):
            op = op[1:]
    
    while not (op in [str(x) for x in range(0, 65)]):
        print("\n    [\033[91m!\033[37m] Not an Option!")
        op = input("\n    [\033[92m*\033[37m] Enter your District\033[92m:> \033[37m")
        if not (op=="") and not (op == "0"):
            if (op[0] == "0"):
                op = op[1:]
    
    if (op == "0"):
        sys.exit("\033[37m")
    
    district = districtList[int(op)-1]
    return district

# Setup Ramadan Time Table
def setupSettings():
    logo()
    
    district = getDistrict()
    file = open("ramadan/.district", "w")
    file.write(district)
    file.close()
    
    time.sleep(0.5)
    print("\n    \033[37m[\033[92m*\033[37m] Selected District: \033[92m" + district)
    time.sleep(0.5)
    
    if (os.path.exists(sitePkg+"/ramadan")):
        os.system(f"rm -rf {sitePkg}/ramadan > /dev/null 2>&1")
    
    os.system(f"cp -r ramadan {sitePkg} > /dev/null 2>&1")
    
    callCmd = f"#!/bin/bash\ncd {sitePkg}/ramadan && python main.py $1 $2"
    file = open(binPath+"/ramadan", "w")
    file.write(callCmd)
    file.close()
    
    os.system(f"chmod +x {binPath}/ramadan")
    
    banner = input("\n    \033[37m[\033[92m*\033[37m] Set as Termux Banner with Your Name? [\033[92my\033[37m/\033[92mn\033[37m]: \033[92m")
    while not (banner.lower() in ["", "y", "n"]):
        print("\n    \033[37m[\033[91m!\033[37m] Only \033[92my \033[37mOr \033[92mn\033[37m!")
        banner = input("\n    \033[37m[\033[92m*\033[37m] Set as Termux Banner with Your Name? [\033[92my\033[37m/\033[92mn\033[37m]: \033[92m")
    
    if (banner == "y"):
        setupBanner(False)
    
    time.sleep(1)
    
    print("""\n    \033[37m[\033[92m!\033[37m] Note:
      
      Ramadan Time Table setting successfull
      Need Internet Connection everytime Untill Ramadan Starts
      Once Ramadan starts and Time Table data is parsed, You can use it Offline
      
      Type "ramadan" to Show Time Table
      Type "ramadan --custom districtName" to use Custom district
      Type "ramadan --reset" to Reset Settings""")
    if (banner == "y"):
        print("""      Data will not autometically Be parsed while Using Banner.
      You need To type "ramadan" in the Terminal to Parse Data
        
      Restart your Termux""")
    
    print("\n    [\033[94m*\033[37m] Ramadan Mobarak [\033[94m*\033[37m]\n")
    sys.exit()


# Setup with Banner
def setupBanner(direct=True):
    if (direct):
        if (not os.path.exists(sitePkg+"/ramadan")) or (not os.path.exists(binPath+"/ramadan")):
            setupSettings()
    
    print("\n    \033[37m[\033[92m*\033[37m] Your Old Banner will be Temporarily Removed")
    name = input("\n    \033[37m[\033[92m*\033[37m] Enter Name to Display:> \033[92m")
    
    while (name == ""):
        print("\n    \033[37m[\033[91m!\033[37m] Please Enter a Name")
        name = input("\n    \033[37m[\033[92m*\033[37m] Enter Name to Display:> \033[92m")
    
    if not (os.path.exists(home+"/.bashrc")):
        os.system(f"touch {home}/.bashrc > /dev/null 2>&1")
    else:
        if (os.path.exists(home+"/.bashrc.tnr")):
            os.system(f"rm {home}/.bashrc > /dev/null 2>&1")
        else:
            os.system(f"mv {home}/.bashrc {home}/.bashrc.tnr > /dev/null 2>&1")
    
    if (any(sb.getoutput(f"command -v {x}")=="" for x in ["figlet", "lolcat"])):
        print("\n    \033[37m[\033[92m*\033[37m] Installing Packeges\033[92m: \033[37m", end="")
        os.system("pkg install figlet > /dev/null 2>&1")
        os.system("pip install lolcat > /dev/null 2>&1")
        print("Done")
    
    bannerText = f"""clear
    figlet {name} | lolcat
    ramadan --banner"""
    
    file = open(f"{home}/.bashrc", "w")
    file.write(bannerText)
    file.close()
    
    if (direct):
        print("\n    \033[37m[\033[92m*\033[37m] Banner added Successfully!\n    [\033[92m*\033[37m] Restart Termux")
        sys.exit("")

# Remove Banner
def removeBanner():
    remove = input("\n    \033[37m[\033[92m*\033[37m] Are you sure You want to Remove Banner? [\033[92my\033[37m/\033[92mn\033[37m]: \033[92m")
    while not (remove.lower() in ["y", "n"]):
        print("\n    \033[37m[\033[91m!\033[37m] Only \033[92my \033[37mOr \033[92mn\033[37m!")
        remove = input("\n    \033[37m[\033[92m*\033[37m] Are you sure You want to Remove Banner? [\033[92my\033[37m/\033[92mn\033[37m]: \033[92m")
    
    if (remove == "n"):
        sys.exit("\n    \033[37m[\033[92m*\033[37m] Exiting...\n")
    
    if (os.path.exists(home+"/.bashrc")):
        bannerData = open(home+"/.bashrc", "r").read()
        if ("ramadan --banner" in bannerData):
            if (os.path.exists(home+"/.bashrc.bak")):
                os.system(f"rm {home}/.bashrc > /dev/null 2>&1")
                os.system(f"mv {home}/.bashrc.bak {home}/.bashrc > /dev/null 2>&1")
                print("\n    \033[37m[\033[92m*\033[37m] Banner Removed Successfully\n")
                sys.exit()
    
    print("\n    \033[37m[\033[91m!\033[37m] Banner is Not Installed!\n")
    sys.exit()


# Reset Settings
def resetSettings():
    reset = input("\n    \033[37m[\033[92m*\033[37m] Are you sure You want to Reset Settings? [\033[92my\033[37m/\033[92mn\033[37m]: \033[92m")
    while not (reset.lower() in ["y", "n"]):
        print("\n    \033[37m[\033[91m!\033[37m] Only \033[92my \033[37mOr \033[92mn\033[37m!")
        reset = input("\n    \033[37m[\033[92m*\033[37m] Are you sure You want to Reset Settings? [\033[92my\033[37m/\033[92mn\033[37m]: \033[92m")
    
    if (reset == "n"):
        sys.exit("\n    \033[37m[\033[92m*\033[37m] Exiting...\n")
    
    os.system("ramadan --reset > /dev/null 2>&1")
    os.system("rm ramadan/.district > /dev/null 2>&1")
    print("\n    \033[37m[\033[92m*\033[37m] Settings Reseted Successfully!\n")
    sys.exit()


# Main Menu
def main():
    logo()
    
    print("\n    \033[37m[\033[92m*\033[37m] Choose your Option:\n")
    print("    [\033[92m01\033[37m] Setup Ramadan Time Table")
    print("    [\033[92m02\033[37m] Setup Ramadan Time Table with Banner")
    print("    [\033[92m03\033[37m] Remove Time Table Banner")
    print("    [\033[92m04\033[37m] Reset Time Table Settings")
    print("    [\033[92m05\033[37m] Exit")
    
    op = input("\n    [\033[92m*\033[37m] Enter Your Choice\033[92m:> \033[37m").replace("0", "")
    
    while not (op in ["1", "2", "3", "4", "5"]):
        print("\n    [\033[91m!\033[37m] Wrong Input!")
        op = input("\n    [\033[92m*\033[37m] Enter Your Choice\033[92m:> \033[37m").replace("0", "")
    
    if (op == "1"):
        setupSettings()
    elif (op == "2"):
        setupBanner()
    elif (op == "3"):
        removeBanner()
    elif (op == "4"):
        resetSettings()
    elif (op == "5"):
        sys.exit("")


if (__name__ == "__main__"):
    main()