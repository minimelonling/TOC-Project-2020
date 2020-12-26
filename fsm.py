from transitions.extensions import GraphMachine
from utils import send_text_message
from time_management import activity, add_act, change_act, change_time, change_tag, show_schedule, cal_time, start_odr, tags


start = ""
end = ""
act = ""
tag = ""
chg = ""
tmps = []
tmpe = []
back = 0

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_add(self, event):
        global back
        text = event.message.text
        if back == 0:
            return text.lower() == "add"
        else:
            return text.lower() == "continue"

    def is_going_to_astart(self, event):
        global start
        global tmps
        global back
        back = 1
        start = event.message.text
        tmps = start.split(":")
        if len(tmps) != 2:
            return False
        if int(tmps[0]) >= 0 and int(tmps[0]) < 25 and int(tmps[1]) >= 0 and int(tmps[1]) < 61:
            return True
        else:
            return False

    def is_going_to_aend(self, event):
        global end
        global tmps
        global tmpe
        end = event.message.text
        tmpe = end.split(":")
        if len(tmpe) != 2:
            return False
        if int(tmpe[0]) >= 0 and int(tmpe[0]) < 25 and int(tmpe[1]) >= 0 and int(tmpe[1]) < 61:
            if int(tmps[0]) < int(tmpe[0]) or (int(tmps[0]) == int(tmpe[0]) and int(tmps[1]) < int(tmpe[1])):
                return True
        return False

    def is_going_to_aact(self, event):
        global act
        act = event.message.text
        return True

    def is_going_to_atag(self, event):
        global tag
        tag = event.message.text
        return True

    def is_going_to_show(self, event):
        global back
        text = event.message.text
        if len(start_odr) != 0:
            if back == 0:
                return text.lower() == "show"
            else:
                return text.lower() == "continue"
        else:
            return False

    def is_going_to_schedule(self, event):
        global back
        back = 1
        text = event.message.text
        return text.lower() == "schedule"

    def is_going_to_statistic(self, event):
        global back
        back = 1
        text = event.message.text
        return text.lower() == "statistic"

    def is_going_to_change(self, event):
        global back
        text = event.message.text
        if len(start_odr) != 0:
            if back == 0:
                return text.lower() == "change"
            else:
                return text.lower() == "continue"
        else:
            return False

    def is_going_to_cact(self, event):
        global back
        back = 1
        text = event.message.text
        return text.lower() == "act"

    def is_going_to_act1(self, event):
        global act
        act = event.message.text
        for k in start_odr:
            if k.act == act:
                return True
        return False

    def is_going_to_act2(self, event):
        global chg
        chg = event.message.text
        return True

    def is_going_to_ctime(self, event):
        global back
        back = 1
        text = event.message.text
        return text.lower() == "time"

    def is_going_to_tact(self, event):
        global act
        act = event.message.text
        for k in start_odr:
            if k.act == act:
                return True
        return False

    def is_going_to_tstart(self, event):
        global start
        global tmps
        start = event.message.text
        tmps = start.split(":")
        if len(tmps) != 2:
            return False
        if int(tmps[0]) >= 0 and int(tmps[0]) < 25 and int(tmps[1]) >= 0 and int(tmps[1]) < 61:
            return True
        else:
            return False

    def is_going_to_tend(self, event):
        global end
        global tmpe
        end = event.message.text
        tmpe = end.split(":")
        if len(tmpe) != 2:
            return False
        if int(tmpe[0]) >= 0 and int(tmpe[0]) < 25 and int(tmpe[1]) >= 0 and int(tmpe[1]) < 61:
            if int(tmps[0]) < int(tmpe[0]) or (int(tmps[0]) == int(tmpe[0]) and int(tmps[1]) < int(tmpe[1])):
                return True
        return False

    def is_going_to_ctag(self, event):
        global back
        back = 1
        text = event.message.text
        return text.lower() == "tag"

    def is_going_to_gact(self, event):
        global act
        act = event.message.text
        for k in start_odr:
            if k.act == act:
                return True
        return False

    def is_going_to_gtag(self, event):
        global tag
        tag = event.message.text
        return True

    def is_going_to_init(self, event):
        global back
        back = 0
        text = event.message.text
        return text.lower() == "back"

    def on_enter_init(self, event):
        s = "Welcome~~\n\n\n"
        s += "Please enter one of the following options:\n\n"
        s += "1. add (add new activity)\n"
        s += "2. show (show the infos in detail)\n"
        s += "3. change (change the data)\n"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_add(self, event):
        s = ""
        s += "Add a new activity to your schedule!\n\n"
        s += "Enter start time:"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_astart(self, event):
        s = "Enter end time:"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_aend(self, event):
        s = "Enter activity name: "
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_aact(self, event):
        s = ""
        s += "***current tags:\n"
        for t in tags:
            s += (t + "\n")
        s = "\n\nEnter tag name:"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_atag(self, event):
        add_act(start, end, act, tag)
        s = "New activity " + act + " is already added, please enter \"back\" to return to the main part or enter \"continue\" to continue adding activities"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_show(self, event):
        s = "Please enter one of the following options:\n\n"
        s += "1. schedule (list all the activities in the order of start time)\n"
        s += "2. statistic (list the time spent in each kind of activities)"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_schedule(self, event):
        s = show_schedule()
        s += "\n\nPlease enter \"back\" to the main part"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_statistic(self, event):
        s = cal_time()
        s += "\n\nPlease enter \"back\" to the main part"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_change(self, event):
        s = "Please enter one of the following options to choose which kind of data to be changed:\n\n"
        s += "1. act (change activity)\n"
        s += "2. time (change the particular activity time)\n"
        s += "3. tag (change the attribute of the particular activity)\n"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_cact(self, event):
        s = "***current activities:\n\n"
        for k in start_odr:
            s += (k.act + "\n")
        s += "\n\nPlease choose an activity to be replaced"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_act1(self, event):
        s = "Please enter the new name of this activities"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_act2(self, event):
        change_act(act, chg)
        s = "activity " + act + " is already changed to " + chg
        s += "\n\nPlease enter \"back\" to return to the main part, or if you want to keep changing other data, just enter \"continue\""
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_ctime(self, event):
        s = "***current activities:\n\n"
        for k in start_odr:
            s += (k.act + "\n")
        s += "\n\nPlease choose an activity, and update it's time"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_tact(self, event):
        s = "Please enter the new start time"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_tstart(self, event):
        s = "Please enter the new end time"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_tend(self, event):
        change_time(start, end, act)
        s = "the activity " + act + " time is already updated"
        s += "\n\nPlease enter \"back\" to return to the main part, or if you want to keep changing other data, just enter \"continue\""
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_ctag(self, event):
        s = "***current activities:\n\n"
        for k in start_odr:
            s += (k.act + "\n")
        s += "\n\nPlease choose an activity, and  change it tag"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_gact(self, event):
        s = "Please enter the new tag for this activity"
        reply_token = event.reply_token
        send_text_message(reply_token, s)

    def on_enter_gtag(self, event):
        s = change_tag(act, tag)
        s += "\n\nPlease enter \"back\" to return to the main part, or if you want to keep changing other data, just enter \"continue\""
        reply_token = event.reply_token
        send_text_message(reply_token, s)

