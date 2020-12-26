from copy import copy

class activity:
    def __init__(self, start, end, act, tag):
        self.start = []
        self.end = []
        tmp = start.split(":")
        self.start.append(int(tmp[0]))
        self.start.append(int(tmp[1]))
        tmp = end.split(":")
        self.end.append(int(tmp[0]))
        self.end.append(int(tmp[1]))
        self.act = act
        self.tag = tag
    
    def change_time(self, start, end):
        tmp = start.split(":")
        self.start[0] = int(tmp[0])
        self.start[1] = int(tmp[1])
        tmp = end.split(":")
        self.end[0] = int(tmp[0])
        self.end[1] = int(tmp[1])

start_odr = []
tags = []

"""
start = ["3:40", "2:35", "21:08", "5:00", "9:23", "6:48", "9:04", "0:03", "7:50", "1:30", "3:40"]
end = ["4:50", "9:00", "23:50", "23:59", "19:07", "17:04", "11:19", "24:00", "14:33", "8:22", "17:04"]
act = ["ag sfsef", "bee edse", "cgt eddes", "dsrfrs", "da esfre sfsf", "f", "g", "h", "i", "j", "k"]
tag = ["a", "b" ,"a", "h", "c", "b", "h", "c", "h", "i", "a"]
"""

def add_act(start, end, act, tag):
    tmp = activity(start, end, act, tag)
    c = 0
    flag = False
    for t in tags:
        if t == tag:
            flag = True
    if not flag:
        tags.append(tag)
    if len(start_odr) == 0:
        start_odr.insert(0, tmp)
        return
    for k in start_odr:
        if k.start[0] > tmp.start[0] or (k.start[0] == tmp.start[0] and k.start[1] > tmp.start[1]):
            start_odr.insert(c, copy(tmp))
            break
        elif k.start[0] == tmp.start[0] and k.start[1] == tmp.start[1]:
            if k.end[0] > tmp.end[0] or (k.end[0] == tmp.end[0] and k.end[1] > tmp.end[1]):
                start_odr.insert(c, copy(tmp))
                break
        c += 1
    if c == len(start_odr):
        start_odr.append(copy(tmp))

def change_act(act, chg):
    for k in start_odr:
        if is_equal(k.act, act):
            tmp = k.act
            k.act = chg
            return tmp + " is already changed to " + k.act
    return "change failed"

def change_time(start, end, act):
    for i in range(0, len(start_odr)):
        if is_equal(start_odr[i].act, act):
            start_odr[i].change_time(start, end)
            tmp = start_odr[i]
            if len(start_odr) != 0:
                start_odr.remove(tmp)
                c = 0
                for k1 in start_odr:
                    if k1.start[0] > tmp.start[0] or (k1.start[0] == tmp.start[0] and k1.start[1] > tmp.start[1]):
                        start_odr.insert(c, tmp)
                        break
                    elif k1.start[0] == tmp.start[0] and k1.start[1] == tmp.start[1]:
                        if k1.end[0] > tmp.end[0] or (k1.end[0] == tmp.end[0] and k1.end[1] > tmp.end[1]):
                            start_odr.insert(c, tmp)
                            break
                    c += 1
                if c == len(start_odr):
                    start_odr.append(tmp)
            return start_odr[i].act + " time change success" 
    return "invalid activity " + act

def change_tag(act, tag):
    for k in start_odr:
        if is_equal(act, k.act):
            tmp = k.tag
            k.tag = tag
            return tmp + " in " + k.act + " is already changed to " + k.tag
    return "no activity's tag change"

def show_schedule():
    s = ""
    for k in start_odr:
        s += time_concat(k.start)
        s += " - "
        s += time_concat(k.end)
        s += (" " + k.act + " " + k.tag + "\n")
    return s

def cal_time():
    s = ""
    time = [0, 0]
    for t in tags:
        s += (t + ": ")
        for k in start_odr:
            if k.tag == t:
                time[0] += (k.end[0] - k.start[0])
                time[1] += (k.end[1] - k.start[1])
                if time[1] >= 60:
                    time[0] += int(time[1] / 60)
                    time[1] %= 60
                elif time[1] < 0:
                    time[0] += (int(time[1] / 60) - 1)
                    time[1] %= 60
        s += (str(time[0]) + " hours " + str(time[1]) + " minutes\n")
        time = [0, 0]
    return s

def time_concat(time):
    s = ""
    if int(time[0] / 10) == 0:
        s += ("0" + str(time[0]))
    else:
        s += str(time[0])
    s += ":"
    if int(time[1] / 10) == 0:
        s += ("0" + str(time[1]))
    else:
        s += str(time[1])
    return s

def is_equal(act1, act2):
    tmp1 = act1.split()
    tmp2 = act2.split()
    if len(tmp1) != len(tmp2):
        return False
    else:
        for i in range(0, len(tmp1)):
            if tmp1[i] != tmp2[i]:
                return False
    return True

"""
for i in range(0, 11):
    add_act(start[i], end[i], act[i], tag[i])
print(len(start_odr))
print("start")
for i in start_odr:
    print(i.start)

print(show_schedule())
print(cal_time())
for t in tags:
    print(t)
#change_act("da esfre sfsf", "dedef")
print(change_time("5:00", "6:00", "da esfre sfsf"))
print(show_schedule())
"""
