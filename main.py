from contract import get_contract
from bot import add_user_betting_data, end_round, new_round_started
import threading
import time
import socket


contract = get_contract()


startroundevent = contract.events.StartRound.create_filter(
    fromBlock="0x0", argument_filters={}, topics=[]
)
endroundevent = contract.events.EndRound.create_filter(
    fromBlock="0x0", argument_filters={}, topics=[]
)
betbullevent = contract.events.BetBull.create_filter(
    fromBlock="0x0", argument_filters={}, topics=[]
)
betbearevent = contract.events.BetBear.create_filter(
    fromBlock="0x0", argument_filters={}, topics=[]
)


def gei_to_bnb(gei_amount):
    bnb_amount = gei_amount / 10**18
    return bnb_amount


def collect_bet(eventdata):
    user = eventdata["sender"]
    amount = gei_to_bnb(eventdata["amount"])
    epoch = eventdata["epoch"]
    return [user, amount, epoch]


def forstartround():
    while True:
        try:
            startroundeventdata = startroundevent.get_new_entries()
            if startroundeventdata != []:
                for event in startroundeventdata:
                    new_round_started(event["args"]["epoch"])
        except:
            pass


def forendround():
    while True:
        try:
            endroundeventdata = endroundevent.get_new_entries()
            if endroundeventdata != []:
                for event in endroundeventdata:
                    end_round(event["args"]["epoch"], event["args"]["price"])
        except:
            pass


def forbetbull():
    while True:
        try:
            betbulleventdata = betbullevent.get_new_entries()
            if betbulleventdata != []:
                for event in betbulleventdata:
                    add_user_betting_data("bull", collect_bet(event["args"]))
        except:
            pass


def forbetbear():
    while True:
        try:
            betbeareventdata = betbearevent.get_new_entries()
            if betbeareventdata != []:
                for event in betbeareventdata:
                    add_user_betting_data("bear", collect_bet(event["args"]))
        except:
            pass


def run():
    thread = threading.Thread(target=forstartround)
    thread.start()

    thread1 = threading.Thread(target=forendround)
    thread1.start()

    thread2 = threading.Thread(target=forbetbear)
    thread2.start()

    thread3 = threading.Thread(target=forbetbull)
    thread3.start()

    thread.join()
    thread1.join()
    thread2.join()
    thread3.join()


# check internet connect to run bot
def check_internet_connection():
    try:
        # Try connecting to a well-known website or server that is likely to be online.
        host = "www.google.com"
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


while not check_internet_connection():
    print("Waiting for an internet connection...")
    time.sleep(5)


# To Start Bot
run()
