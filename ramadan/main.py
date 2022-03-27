import sys
import os
import time
from datetime import datetime
import json
import shutil
from more import *


columns = shutil.get_terminal_size().columns

try:
    arg = sys.argv[1].lower()
    try:
        arg2 = sys.argv[2].lower()
    except:
        arg2 = ""
except:
    arg = ""

if not (arg in ["", "--banner", "--reset", "--custom"]):
    psb("\n    \033[92m[\033[91m!\033[92m] You Have Entered an Invailed Argument\033[37m\n")
    sys.exit()
else:
    (arg == "")
    

if (arg == "--reset"):
    reset()

#SomeImportantFunctions#

#EquationOfMinus
def minus_data(main_data, add_data, hour_data):
    if (main_data < add_data):
        hr = str(hour_data - 1)
        mn = str(main_data + 60 - add_data)
    else:
        hr = str(hour_data)
        mn =  str(main_data - add_data)
    if (len(mn) == 1):
        mn = "0"+mn
    data = hr+":"+mn
    return data

#EquationOfPlus
def plus_data(main_data, add_data, hour_data):
    mn = main_data + add_data
    if (mn > 60):
        mn = str(mn - 60)
        hr = str(hour_data + 1)
    else:
        mn = str(mn)
        hr  = str(hour_data)
    if (len(mn) == 1):
        mn = "0"+mn
    data = hr+":"+mn
    return data

##EquationOfRemainingTime
#Sehehi
def remain_sehri(data):
    pre_hour = int(hour)
    pre_min = int(minu)
    
    temp = data.split(":")
    temp_hour = int(temp[0])
    temp_min = int(temp[1])
    
    if (pre_hour > 5):
        new_hour = str((24 - pre_hour) + temp_hour)
    else:
        new_hour = str(temp_hour - pre_hour)
    
    if (pre_min > temp_min):
        new_min = str(pre_min - temp_min)
    else:
        new_min = str(temp_min - pre_min)
        new_hour = str(int(new_hour) + 1)
    if (len(new_hour) == 1):
        new_hour = "0" + new_hour
    if (len(new_min) == 1):
        new_min = "0" + new_min
    return new_hour, new_min

#Iftar
def remain_iftar(data):
    pre_hour = int(hour)
    pre_min = int(minu)
    
    temp = data.split(":")
    temp_hour = int(temp[0])
    temp_min = int(temp[1])
    
    if (pre_hour > 18):
        new_hour = str((24 - pre_hour) + (temp_hour + 12))
    else:
        new_hour = str((temp_hour + 12) - pre_hour)
    
    if (pre_min > temp_min):
        new_min = str(pre_min - temp_min)
    else:
        new_min = str(temp_min - pre_min)
        new_hour = str(int(new_hour) + 1)
    if (len(new_hour) == 1):
        new_hour = "0" + new_hour
    if (len(new_min) == 1):
        new_min = "0" + new_min
    return new_hour, new_min

#GetSeheriTime
def sehri_get(main_data, add_data):
    hour = 4
    if  ("+" in  add_data):
        main_data = int(main_data)
        add_data = int(add_data.replace("+", ""))
        data =  plus_data(main_data, add_data, hour)
    elif ("-" in add_data):
        add_data = int(add_data.replace("-", ""))
        main_data = int(main_data)
        data = minus_data(main_data, add_data, hour)
    else:
        if (int(main_data) > 55):
            data = "3:"+main_data
        else:
            data = "4:"+main_data
    return data

#GetIftarTime
def iftar_get(main_data, add_data):
    hour = 6
    if  ("+" in  add_data):
        main_data = int(main_data)
        add_data = int(add_data.replace("+", ""))
        data =  plus_data(main_data, add_data, hour)
    elif ("-" in add_data):
        add_data = int(add_data.replace("-", ""))
        main_data = int(main_data)
        data = minus_data(main_data, add_data, hour)
    else:
        data = "6:"+main_data
    return data


#FetchRamadanDateData
def is_ramadan():
    import requests
    try:
        res = requests.get("https://raw.githubusercontent.com/Toxic-Noob/PersonalRepository/main/ramadan_approval.txt").text
        file = open(".approval", "w")
        file.write(res)
        file.close()
    except requests.exceptions.ConnectionError:
        print("\n\033[92m[\033[91m!\033[92m] Please Connent To The Interner")
        l = input("\n\033[92m[\033[91m!\033[92m] Press Enter To Countinue...\033[37m")
        is_ramadan()

#CheckMonthDays
def check_month():
    tone = ["1", "3", "5", "7", "8", "10", "12"]
    tzero = ["4", "6", "9", "11"]
    teight = ["2"]
    if (month in tone):
        data = "31"
    elif (month in tzero):
        data = "30"
    elif (month in teight):
        data = "28"
    return data

#Print_ComingSoon
def coming_soon():
    print_dist = "\033[95m District : \033[37m"+dist.title()
    if (year == "2022"):
        if (int(month) < 4):
            mon = 4 - int(month)
            wait = "Wait \033[37m"+str(mon)+" \033[95mMonth(\033[37ms\033[95m) Till Ramadan!!"
            if (mon == 1):
                days = check_month()
                nd = (int(days) - int(day)) + 3
                wait = "Wait \033[37m"+str(nd)+" \033[95mDay(\033[37ms\033[95m) Till Ramadan!!"
        elif (month == "4"):
            days = check_month()
            if (int(day) < 3 ):
                nd = (3 - int(day))
            elif (int(day) > 3):
                nd = (int(days) - 3) + int(days)
            else:
                nd = "0"
            wait = "Wait \033[37m"+str(nd)+" \033[95mDay(\033[37ms\033[95m) Till Ramadan!!"
        else:
                wait = "Wait For Next Year!!\033[37m\033[37m\033[37m\033[37m"
    else:
        wait = "Wait Some Days or Months!!\033[37m\033[37m\033[37m\033[37m"
    
    print_wait = "\033[95m Ramadan Is Coming Soon!!"
    print_wait_time = "\033[95m "+wait
    
    if (columns > 58):
        print_date  = "\033[95mRamadan No : \033[37m--  │\033[95m Date : \033[37m"+str(now.date())
    else:
        print_date  = "\033[95m    Ramadan No : \033[37m--  │\033[95m Date : \033[37m"+str(now.date())
    
    if (columns > 58):
        print("\033[94m┌", end = "")
        print("\033[94m─" * (57), end = "")
        print("\033[94m┐")
        print("\033[94m│", end="")
        print(print_dist.center(66), end="")
        print("\033[94m │")
        print("\033[94m│", end="")
        print("\033[93m-" * (57), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_date.center(77), end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (57), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_wait.center(62), end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (57), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_wait_time.center(82), end="")
        print("\033[94m│")
        print("\033[94m└", end = "")
        print("\033[94m─" * (57), end = "")
        print("\033[94m┘\033[0;37m")
    else:
        print("\033[94m┌", end = "")
        print("\033[94m─" * (columns - 2), end = "")
        print("\033[94m┐")
        print("\033[94m│", end="")
        print(print_dist.center(columns + 8), end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (columns - 2), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_date.center(columns + 18), end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (columns - 2), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_wait.center(columns + 3), end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (columns - 2), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_wait_time.center(columns + 23), end="")
        print("\033[94m│")
        print("\033[94m└", end = "")
        print("\033[94m─" * (columns - 2), end = "")
        print("\033[94m┘\033[0;37m")


#PrintData#
def print_data(sehri, iftar, no):
    if (len(no) == 1):
        no ="0" + no
    
    temp_seh = remain_sehri(sehri)
    temp_iftar = remain_iftar(iftar)
    
    
    print_dist = "\033[95m District : \033[37m"+dist.title()
    
    if (columns < 50):
        print_date  = "\033[95mRamadan No : \033[37m"+no+"  │\033[95m Date : \033[37m"+str(now.date())+ "      "
        remain_seheri = temp_seh[0] + "\033[95m Hour & \033[37m" +temp_seh[1]+" \033[95mMin"
        remain_iftari = temp_iftar[0] + "\033[95m Hour & \033[37m" +temp_iftar[1]+" \033[95mMin"
        
        print_seheri = "\033[95mSeheri : \033[37m"+ sehri +" AM │\033[95m Wait : \033[37m"+ remain_seheri
        print_iftar = "\033[95mIftar  : \033[37m"+ iftar +" PM │\033[95m Wait : \033[37m"+ remain_iftari
    elif (columns > 50) and (columns < 55):
        print_date  = "\033[95m   Ramadan No : \033[37m"+no+"  │\033[95m Date : \033[37m"+str(now.date())+ "             "
        remain_seheri = temp_seh[0] + "\033[95m Hour & \033[37m" +temp_seh[1]+" \033[95mMinutes   "
        remain_iftari = temp_iftar[0] + "\033[95m Hour & \033[37m" +temp_iftar[1]+" \033[95mMinutes   "
        
        print_seheri = "   \033[95mSeheri : \033[37m"+ sehri +" AM │\033[95m Wait : \033[37m"+ remain_seheri
        print_iftar = "   \033[95mIftar  : \033[37m"+ iftar +" PM │\033[95m Wait : \033[37m"+ remain_iftari
    elif (columns > 44) and (columns < 54):
        print_date  = "\033[95m Ramadan No : \033[37m"+no+"  │\033[95m Date : \033[37m"+str(now.date())+ "           "
        remain_seheri = temp_seh[0] + "\033[95m Hours & \033[37m" +temp_seh[1]+" \033[95mMinutes"
        remain_iftari = temp_iftar[0] + "\033[95m Hours & \033[37m" +temp_iftar[1]+" \033[95mMinutes"
        
        print_seheri = " \033[95mSeheri : \033[37m"+ sehri +" AM │\033[95m Wait : \033[37m"+ remain_seheri
        print_iftar = " \033[95mIftar  : \033[37m"+ iftar +" PM │\033[95m Wait : \033[37m"+ remain_iftari
    else:
        print_date  = "\033[95m    Ramadan No : \033[37m"+no+"  │\033[95m Date : \033[37m"+str(now.date())+ "                 "
        remain_seheri = temp_seh[0] + "\033[95m Hours and \033[37m" +temp_seh[1]+" \033[95mMinutes    "
        remain_iftari = temp_iftar[0] + "\033[95m Hours and \033[37m" +temp_iftar[1]+" \033[95mMinutes    "
        
        print_seheri = "    \033[95mSeheri : \033[37m"+ sehri +" AM │\033[95m Wait : \033[37m"+ remain_seheri
        print_iftar = "    \033[95mIftar  : \033[37m"+ iftar +" PM │\033[95m Wait : \033[37m"+ remain_iftari
        
    if (columns > 58):
        print("\033[94m┌", end = "")
        print("\033[94m─" * (57), end = "")
        print("\033[94m┐")
        print("\033[94m│", end="")
        print(print_dist.center(66), end="")
        print("\033[94m │")
        print("\033[94m│", end="")
        print("\033[93m-" * (57), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_date, end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (57), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_seheri, end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (57), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_iftar, end="")
        print("\033[94m│")
        print("\033[94m└", end = "")
        print("\033[94m─" * (57), end = "")
        print("\033[94m┘\033[0;37m")
    else:
        print("\033[94m┌", end = "")
        print("\033[94m─" * (columns - 2), end = "")
        print("\033[94m┐")
        print("\033[94m│", end="")
        print(print_dist.center(columns + 8), end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (columns - 2), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_date, end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (columns - 2), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_seheri, end="")
        print("\033[94m│")
        print("\033[94m│", end="")
        print("\033[93m-" * (columns - 2), end = "")
        print("\033[94m│")
        print("\033[94m│", end="")
        print(print_iftar, end="")
        print("\033[94m│")
        print("\033[94m└", end = "")
        print("\033[94m─" * (columns - 2), end = "")
        print("\033[94m┘\033[0;37m")

#FetchingDates

now = datetime.now()
year  = str(now.year)
month= str(now.month)
day = str(now.day)
hour = str(now.strftime("%H"))
minu = str(now.minute)

#FetchingData
try:
    main_data = json.loads(open("main_data.json", "r").read())
    time_data = json.loads(open("time_data.json", "r").read())
    if not (arg == "--custom"):
        try:
            dist = open(".district", "r").read().replace("\n", "")
        except:
            if (arg == "--banner"):
                setup("banner")
                os.system("clear")
                os.system("cd $HOME && bash .bashrc")
                sys.exit()
            elif (arg == ""):
                setup("")
    else:
        dist = arg2
        if (dist == ""):
            psb("\n    \033[92m[\033[91m!\033[92m] You Have Not Entered Any District Name!")
            dist = input("\n    \033[92m[\033[37m*\033[92m] Enter Your District Name:> \033[37m").lower()
            while not (dist in main_data):
                if (dist == ""):
                    psb("\n    \033[92m[\033[91m!\033[92m] You Have Not Entered Any District Name!")
                else:
                    psb("\n    \033[92m[\033[91m!\033[92m] You Have Entered An Invalid District Name!")
                dist = input("\n    \033[92m[\033[37m*\033[92m] Enter Your District Name:> \033[37m").lower()
        else:
            dist = dist
        print("\033[37m")


    seh_add = main_data[dist]["seheri"]
    ift_add = main_data[dist]["iftar"]

    roja_no = time_data[day]["no"]
    seh_main = int(time_data[day]["seheri"])
    if (int(hour) > 5):
        seh_main = str(time_data[str(int(day) + 1)]["seheri"])
    ift_main = time_data[day]["iftar"]

    sehri_got = sehri_get(seh_main, seh_add)
    iftar_got = iftar_get(ift_main, ift_add)
except Exception as e:
    print("[*] En Error Occured!!")
    print("[*] Error: "+str(e))
    sys.exit()


try:
    is_ok = open(".approval", "r").read().replace("\n", "")
    if (int(month) > 4) and (int(day) >= 2) and (int(hour) > 18):
        remove_banner()
except FileNotFoundError:
    if (int(month) > 4) and (int(day) >= 2):
        try:
            opn = open("/data/data/com.termux/files/home/.bashrc", "r").read()
            if ("ramadan" in opn):
                remove_banner()
                sys.exit()
        except:
            pass
    if not (month == "4"):
        coming_soon()
        sys.exit()
    if (arg == "--banner"):
            sys.exit()
    else:
        is_ramadan()
        is_ok = open(".approval", "r").read().replace("\n", "")

if not (is_ok == "OK"):
    coming_soon()
    try:
        os.system("rm .approval")
    except:
        pass
    sys.exit()


#StartProcess
if __name__ == "__main__":
    print_data(sehri_got, iftar_got, roja_no)
