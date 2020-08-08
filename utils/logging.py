import time

def info(text): #Info Level Log Output
    print("[" +str(time.ctime()) +"] [INFO] " +text)

def warn(text): #Warn Level Log Output
    print("[" +str(time.ctime()) +"] [WARNING] " +text)

def error(text): #Error Level Log Output
    print("[" +str(time.ctime()) +"] [ERROR] " +text)

def debug(text): #Error Level Log Output
    try:
        if debug:
            print("[" +str(time.ctime()) +"] [DEBUG] " +text)
    except NameError: #debug value not set, assume false
        return
