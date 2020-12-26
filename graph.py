from transitions.extensions import GraphMachine


machine = TocMachine(
    states=["init",
            "add", "astart", "aend", "aact", "atag", 
            "show", "schedule", "statisic", 
            "change",
            "cact", "act1", "act2", 
            "ctime", "tstart", "tend", "tact", 
            "ctag", "gact", "gtag"],
    transitions=[
        {
            "trigger": "advance",
            "source": "init",
            "dest": "add",
            "conditions": "is_going_to_add",
        },
        {
            "trigger": "advance",
            "source": "add",
            "dest": "astart",
            "conditions": "is_going_to_astart",
        },
        {
            "trigger": "advance",
            "source": "astart",
            "dest": "aend",
            "conditions": "is_going_to_aend",
        },
        {
            "trigger": "advance",
            "source": "aend",
            "dest": "aact",
            "conditions": "is_going_to_aact",
        },
        {
            "trigger": "advance",
            "source": "init",
            "dest": "show",
            "conditions": "is_going_to_show",
        },
        {
            "trigger": "advance",
            "source": "show",
            "dest": "schedule",
            "conditions": "is_going_to_schedule",
        },
        {
            "trigger": "advance",
            "source": "show",
            "dest": "statistic",
            "conditions": "is_going_to_statistic",
        },
        {
            "trigger": "advance",
            "source": "init",
            "dest": "change",
            "conditions": "is_going_to_change",
        },
        {
            "trigger": "advance",
            "source": "change",
            "dest": "cact",
            "conditions": "is_going_to_cact",
        },
        {
            "trigger": "advance",
            "source": "cact",
            "dest": "act1",
            "conditions": "is_going_to_act1",
        },
        {
            "trigger": "advance",
            "source": "act1",
            "dest": "act2",
            "conditions": "is_going_to_act2",
        },
        {
            "trigger": "advance",
            "source": "change",
            "dest": "ctime",
            "conditions": "is_going_to_ctime",
        },
        {
            "trigger": "advance",
            "source": "ctime",
            "dest": "tact",
            "conditions": "is_going_to_tact",
        },
        {
            "trigger": "advance",
            "source": "tact",
            "dest": "tstart",
            "conditions": "is_going_to_tstart",
        },
        {
            "trigger": "advance",
            "source": "tstart",
            "dest": "tend",
            "conditions": "is_going_to_tend",
        },
        {
            "trigger": "advance",
            "source": "change",
            "dest": "ctag",
            "conditions": "is_going_to_ctag",
        },
        {
            "trigger": "advance",
            "source": "ctag",
            "dest": "gact",
            "conditions": "is_going_to_gact",
        },
        {
            "trigger": "advance",
            "source": "gact",
            "dest": "gtag",
            "conditions": "is_going_to_gtag",
        },
        {
            "trigger": "advance",
            "source": ["atag", "schedule", "statisic", "act2", "tend", "gtag"],
            "dest": "init",
            "conditions": "is_going_to_init",
        }
    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
)
class event:
    def __init__(self):
        self.message = msg()
class msg:
    def __init__(self):
        self.text = "go to state1"
machine.advance(event())
machine.advance(event())
machine.get_graph().draw("fsm.png", prog="dot", format="png")
