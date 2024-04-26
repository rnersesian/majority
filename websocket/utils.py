import datetime

def log(*args):
    curren_time = datetime.datetime.now().strftime("%d/%m/%y - %H:%M:%S")
    print(">>>", curren_time, "->", *args)