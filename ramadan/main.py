"""
Description:
    Name: RamadanTime
    Tool: Show current date Ramadan Sehri & Iftar Time
    Author: ToxicNoob Inc.
    GitHub: https://github.com/Toxic-Noob
    Version: 2.0
"""

import os, sys, time, json, shutil
from datetime import datetime

# Global Variables
year = 0
month = 0
day = 0
hour = 0
minute = 0

timeData = {}
timeDifferance = {}
ramadanNo = 0
dailyQuote = {}
todayDate = {}
userDistrict = ""
endDate = {}

columns = shutil.get_terminal_size().columns
if not (columns%2 == 0):
    columns -= 1

sourceBanner = False
customDistrict = None

# Find every index of any item from a String
def findAll(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


# Reset Settings
def reset():
    os.system("rm .district > /dev/null 2>&1")
    os.system("rm timeData.json > /dev/null 2>&1")
    print("\n    \033[37m[\033[91m!\033[37m] Settings Reset Successfull")
    sys.exit("")

# Get the Time Data from Database
def getTimeData():
    print("\n    [\033[92m*\033[37m] Parsing Data\033[92m: \033[37m", end="")
    import requests
    data = requests.get("https://raw.githubusercontent.com/Toxic-Noob/PersonalRepository/main/ramadan/timeData.json").text
    open("timeData.json", "w").write(data)
    
    if not (os.path.exists("timeData.json")):
        time.sleep(0.5)
        print("Error")
        print("\n    [\033[91m!\033[37m] Please Connect to Internet to Parse Data")
        input("    [\033[92m!\033[37m] Press Enter to Try again...")
        getTimeData()
    
    print("Done\n")

# Set Today Time
def setTime():
    global year, month, day, hour, minute
    now = datetime.now()
    
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

# Set the Time Data and Differance Data
def setTimeData():
    global timeData, timeDifferance, endDate
    file = open("timeData.json", "r")
    data = json.loads(file.read())
    file.close()
    status = data.get("status")
    if (status == "running"):
        startDate = data.get("startDate")
        startDay = startDate.get("day")
        startMonth = startDate.get("month")
        startYear = startDate.get("year")
        if (startYear > year) or (startMonth > month) or ((startMonth == month) and (startDay > day)):
            showNotRunning({"date": startDate})
        
        timeData = data.get("timeData")
        endDate = data.get("endDate")
    elif (status == "none"):
        msg = data.get("msg")
        os.remove("timeData.json")
        showNotRunning(msg)
    
    file = open("timeDifferance.json", "r")
    timeDifferance = json.loads(file.read())
    file.close()

# Save User District From User
def saveDistrict():
    districtList = json.loads(open("districtList.json", "r").read()).get("data")
    
    print("\n    [\033[92m*\033[37m] Please Select Your District from Below:\n")
    
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
    
    print("")
    district = districtList[int(op)-1]
    open(".district", "w").write(district)

# Set User's District
def setDistrict(custom=None):
    global userDistrict
    if (custom):
        districtList = json.loads(open("districtList.json", "r").read()).get("data")
        tmp = custom.title()
        if (custom == "cox's bazar"):
            tmp = "Cox's Bazar"
        
        if not (tmp in districtList):
            print("\n    \033[37m[\033[91m!\033[37m] Invalid District Name: \033[92m" + custom)
            sys.exit("\033[37m")
        else:
            userDistrict = tmp
            return
    
    if (os.path.exists(".district")):
        district = open(".district", "r").read().replace("\n", "")
        userDistrict = district
        return
        if (district == ""):
            saveDistrict()
            setDistrict()
            return
    else:
        saveDistrict()
        setDistrict()
        return

# Formate the text For Printing
"""
Try to keep text in the center no matter what the terminal size is:
    (Columns - length of Text to Print - (5 * colors) -2)/2
Explain:
    Columns - length of text will remove the length of text, the [+ (5 * colors)] will add the colors lengths as they will be ignored, so the blank spaces only stays. Remove 2 for the border charecters. Divide by two to get the one side spaces. (The main Process)

if text length is odd then add an extra space before the text to avoid space glitch
And, I cannot discrib the Down part of this function's code. I already forgot what I wrote!
    
"""
def formatText(text, quote=False):
    colors = len(list(findAll(text, "\033")))
    
    if not (quote):
        blankSpaces = int((columns - len(text) + (5 * colors) - 2) /2)
        line = "\033[94m│" + (" " * (blankSpaces if (len(text)-(5 * colors))%2==0 else blankSpaces+1)) + text + (" " * blankSpaces) + "\033[94m│"
    
    else:
        textLen = len(text) - (5 * colors)
        if (textLen > columns-2):
            lines = []
            tmp_line = text
            color = text[(text.find("\033")+2):(text.find("\033")+5)]
            while not ((len(tmp_line) - (5*colors)) < columns):
                spaces = list(findAll(text, " "))
                space = 0
                for i in spaces[::-1]:
                    if (i < columns-2):
                        space = i
                        break
                
                subLine = tmp_line[:space]
                lines.append(formatText(subLine))
                tmp_line = "\033[" + color + tmp_line[space:].strip()
                colors = len(list(findAll(tmp_line, "\033")))
            
            lines.append(formatText(tmp_line))
            line = "\n".join(lines)
        else:
            line = formatText(text)
    
    
    return line

# Get Data from Date Key
def getKeyData(todayKey, saveQuote=False):
    key = f"{todayKey.get('day')}:{todayKey.get('month')}:{todayKey.get('year')}"
    
    data = timeData.get(key)
    
    global ramadanNo, dailyQuote, todayDate
    ramadanNo = data.get("serial")
    if (saveQuote):
        dailyQuote = data.get("quote")
    todayDate = todayKey
    
    sehriTime = data.get("sehri")
    iftarTime = data.get("iftar")
    
    return sehriTime, iftarTime

# Calculate District Time from Dhaka Time
# data = Time Data, period = sehri or iftar :: 0 or 1
def calculateDistrict(data, period):
    districtData = timeDifferance.get(userDistrict)
    # districtData = timeDifferance[userDistrict]
    if (period == 0):
        differance = districtData.get("sehri")
    elif (period == 1):
        differance = districtData.get("iftar")
    
    hour = data.get("hour")
    minute = data.get("minute")
    
    # The Time Differance Database contains minutes with + or - symbols: -4, +5. Eval'ng will return the differance.
    newMinute = eval(f"{minute}{differance}")
    newHour = hour
    
    if (newMinute > 60):
        newMinute -= 60
        newHour += 1
    elif (newMinute < 0):
        newMinute = 60 - int(newMinute*newMinute/2)
        newHour -= 1
    elif (newMinute == 60):
        newMinute = 0
        newHour += 1
    
    data = {"hour": newHour, "minute": newMinute}
    return data

# Calculate the Time left for the Period via finding differance between Period time and current time
def calculateTimeDiff(period, current):
    pHour = period.get("hour")
    pMinute = period.get("minute")
    cHour = current.get("hour")
    cMinute = current.get("minute")
    
    newHour = pHour - cHour
    newMinute = pMinute - cMinute
    
    # If Left Hour is minus Number or 0 hours left and minute is minus number, then the Period time passed, thus, Blank (00:00) and give the time passed to Calculate farther actions
    
    if (newHour < 0) or ((newHour == 0) and (newMinute < 0)):
        diff = (abs(newHour)*60) + abs(newMinute)
        data = {"hour": 0, "minute": 0, "diff": diff}
        return data
    
    if (newMinute > 60):
        newMinute -= 60
        newHour += 1
    elif (newMinute < 0):
        newMinute = 60 - abs(newMinute)
        newHour -= 1
    elif (newMinute == 60):
        newMinute = 0
        newHour += 1
    
    data = {"hour": newHour, "minute": newMinute} # No need for diff time, if Time is still left
    
    return data
    

# Parse Today's Time of Sehri and Iftar
# If the iftar time passed 20 minutes ago, show the next ramadan Sehri time, date and Sl No
def parseTodayTime():
    todayKey = {"day": day, "month": month, "year": year}
    
    endYear = endDate.get("year")
    endMonth = endDate.get("month")
    endDay = endDate.get("day")
    if (year > endYear) or ((month == endMonth) and (day > endDay)) or (month > endMonth):
        showNotRunning({"date": todayKey, "status": "gone"})
    
    sehriPrime, iftarPrime = getKeyData(todayKey, True)
    
    sehriUser = calculateDistrict(sehriPrime, 0)
    iftarUser = calculateDistrict(iftarPrime, 1)
    
    currentTime = {"hour": hour, "minute": minute}
    sehriLeft = calculateTimeDiff(sehriUser, currentTime)
    iftarLeft = calculateTimeDiff(iftarUser, currentTime)
    
    if (sehriLeft.get("diff")):
        if (sehriLeft.get("diff") > 20):
            sehriUser = {"hour": "--", "minute": "--"}
            sehriLeft = {"hour": 0, "minute": 0}
    
    if (iftarLeft.get("diff")):
        if (iftarLeft.get("diff") > 20):
            dayPlus = day + 1
            
            # Check if the day is getting out of Hand!
            if (dayPlus == 29):
                if (month == 2):
                    if not (year%4 == 0):
                        todayKey["month"] += 1
                        dayPlus = 1
            elif (dayPlus > 29):
                if (month == 2):
                    todayKey["month"] += 1
                    dayPlus = 1
                elif (dayPlus == 31):
                    if (month in [4, 6, 9, 11]):
                        todayKey["month"] += 1
                        dayPlus = 1
                elif (dayPlus > 31):
                    todayKey["month"] += 1
                    dayPlus = 1
            
            todayKey["day"] = dayPlus
            sehriPrime, tmp = getKeyData(todayKey)
            sehriUser = calculateDistrict(sehriPrime, 0)
            hourBlank, minuteBlank = 24-hour, 60-minute
            hourLeft = sehriUser.get("hour") + hourBlank
            minuteLeft = sehriUser.get("minute") + minuteBlank
            if (minuteLeft >= 60):
                minuteLeft -= 60
                hourLeft += 1
            
            sehriLeft = {"hour": hourLeft, "minute": minuteLeft}
            iftarUser = {"hour": "--", "minute": "--"}
            iftarLeft  = {"hour": 0, "minute": 0}
    
    allTime = [[sehriUser, iftarUser], [sehriLeft, iftarLeft]]
    
    return allTime

# Show the Error msg if Data doesn't exist
def showNotRunning(authorMsg):
    date  = authorMsg.get("date")
    yearNo = date.get("year")
    monthNo = date.get("month")
    dayNo = date.get("day")
    
    yearLeft = yearNo - year
    if (yearLeft > 0):
        monthLeft = (12 - month) + monthNo # Months left this year + The month num next Ramadan
    else:
        monthLeft = monthNo - month
    if (monthLeft > 0):
        monthLeft -= 1
        dayLeft = (30 - day) + dayNo # Same as above
    else:
        dayLeft = dayNo - day
    
    if (dayLeft > 30):
        monthLeft += 1
        dayLeft -= 30
    
    if (authorMsg.get("status") == "gone"):
        msg = "Till next Year"
    elif (authorMsg.get("status") == "unknown"):
        msg = "Some Time!"
    else:
        if (monthLeft < 1):
            msg = f"About \033[37m{dayLeft} \033[95mDay(s)"
        else:
            msg = f"About \033[37m{monthLeft} \033[95mMonth(s) & \033[37m{dayLeft} \033[95mDay(s)"
    
    # Print Upper Border
    print("\033[94m┌", end="")
    print("─"*(columns-2), end="")
    print("┐")
    
    # Print Data
    print(formatText("\033[95mDistrict : \033[37m" + userDistrict)) # Print District Name
    print("\033[94m│\033[93m" + ("-" * (columns-2)) + "\033[94m│") # Border
    
    showRamadanSl = "--"
    
    showDay = str(day)
    if (len(showDay) == 1): showDay = "0" + showDay
    showMonth = str(month)
    if (len(showMonth) == 1): showMonth = "0" + showMonth
    showYear = str(year)
    
    print(formatText(f"\033[95mRamadan No : \033[37m{showRamadanSl}  │  \033[95mDate : \033[37m{showDay}-{showMonth}-{showYear}")) # Print Ramadan SL and Date
    print("\033[94m│\033[93m" + ("-" * (columns-2)) + "\033[94m│") # Border
    print(formatText("\033[95mRamadan is Coming Soon!"))
    print("\033[94m│\033[93m" + ("-" * (columns-2)) + "\033[94m│") # Border
    print(formatText(f"\033[95mWait {msg}"))
    
    if (authorMsg.get("msg")):
        print("\033[94m│\033[93m" + ("-" * (columns-2)) + "\033[94m│") # Border
        print(formatText(f"\033[95m{authorMsg.get('msg').get('text')} \033[93m- \033[37m{authorMsg.get('msg').get('author')}", True))
    
    # Print Down Border
    print("\033[94m└", end="")
    print("─"*(columns-2), end="")
    print("┘\033[37m")
    
    os.system("rm timeData.json > /dev/null 2>&1")
    
    sys.exit()

# Show the Time left and When the period is and do the Necessary Formating
def showTimeData(data):
    sehriTime = data[0][0]
    iftarTime = data[0][1]
    sehriLeft = data[1][0]
    iftarLeft = data[1][1]
   
    # Print Upper Border
    print("\033[94m┌", end="")
    print("─"*(columns-2), end="")
    print("┐")
    
    # Print Data
    print(formatText("\033[95mDistrict : \033[37m" + userDistrict)) # Print District Name
    print("\033[94m│\033[93m" + ("-" * (columns-2)) + "\033[94m│") # Border
    
    showRamadanSl = str(ramadanNo)
    if (len(showRamadanSl) == 1): showRamadanSl = "0" + showRamadanSl
    
    showDay = str(todayDate.get("day"))
    if (len(showDay) == 1): showDay = "0" + showDay
    showMonth = str(todayDate.get("month"))
    if (len(showMonth) == 1): showMonth = "0" + showMonth
    showYear = str(todayDate.get("year"))
    
    print(formatText(f"\033[95mRamadan No : \033[37m{showRamadanSl}  │  \033[95mDate : \033[37m{showDay}-{showMonth}-{showYear}")) # Print Ramadan SL and Date
    print("\033[94m│\033[93m" + ("-" * (columns-2)) + "\033[94m│") # Border
    
    timeHour = str(sehriTime.get("hour"))
    if len(timeHour)==1: timeHour = "0" + timeHour
    timeMinute = str(sehriTime.get("minute"))
    if (len(timeMinute)==1): timeMinute = "0" + timeMinute
    leftHour = str(sehriLeft.get("hour"))
    if (len(leftHour) == 1): leftHour = "0" + leftHour
    leftMinute = str(sehriLeft.get("minute"))
    if (len(leftMinute)==1): leftMinute = "0" + leftMinute
        
    print(formatText(f"\033[95mSehri: \033[37m{timeHour}:{timeMinute} AM │ \033[95mWait: \033[37m{leftHour} \033[95mHours & \033[37m{leftMinute} \033[95m" + ("Min" if (columns < 50) else "Minutes"))) # Print Sehri Time
    print("\033[94m│\033[93m" + ("-" * (columns-2)) + "\033[94m│") # Border
    
    timeHour = str(iftarTime.get("hour"))
    if (timeHour.isdigit()):
        if (int(timeHour) > 12):
            timeHour = str(int(timeHour) - 12)
    if len(timeHour)==1: timeHour = "0" + timeHour
    timeMinute = str(iftarTime.get("minute"))
    if (len(timeMinute)==1): timeMinute = "0" + timeMinute
    leftHour = str(iftarLeft.get("hour"))
    if (len(leftHour) == 1): leftHour = "0" + leftHour
    leftMinute = str(iftarLeft.get("minute"))
    if (len(leftMinute)==1): leftMinute = "0" + leftMinute
    
    print(formatText(f"\033[95mIftar: \033[37m{timeHour}:{timeMinute} PM │ \033[95mWait: \033[37m{leftHour} \033[95mHours & \033[37m{leftMinute} \033[95m" + ("Min" if (columns < 50) else "Minutes"))) # Print Iftar Time
    print("\033[94m│\033[93m" + ("-" * (columns-2)) + "\033[94m│") # Border
    print(formatText(f"\033[95m{dailyQuote.get('quote')} \033[93m-\033[37m {dailyQuote.get('source')}", True)) # Show a Daily Quote
    
     # Print Down Border
    print("\033[94m└", end="")
    print("─"*(columns-2), end="")
    print("┘\033[37m")



# Main Process
def main():
    if (not os.path.exists("timeData.json")):
        if (sourceBanner):
            sys.exit()
        
        getTimeData()
    
    setTime()
    setDistrict(customDistrict)
    setTimeData()
    todayTime = parseTodayTime()
    showTimeData(todayTime)

if (__name__ == "__main__"):
    args = sys.argv
    if ("--reset" in args):
        reset()
    elif ("--banner" in args):
        sourceBanner = True
    elif ("--custom" in args):
        try:
            customDistrict = args[args.index("--custom")+1]
        except:
            print("\n    \033[37m[\033[91m!\033[37m] No District name Spacified!")
            sys.exit("")
    else:
        if (len(args) > 2):
            print("\n    \033[37m[\033[91m!\033[37m] Unknown argument: " + args[2])
            sys.exit("")
    """
    try:
        main()
    except Exception as e:
        print(e)
        showNotRunning({"status": "unknown", "date": {"day": 1, "month": 1, "year": 3310}})
    """
    main()
