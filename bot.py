import time
from tinydb import TinyDB, where
from tabulate import tabulate
from betstrategy import high_user_betcount_strategy,high_user_betamount_strategy,only_bear
from contract import get_bnb_balance, make_bet,is_bet_win_claimable,claim_winnings


userbull_table = TinyDB("userbullbetting.json")
userbear_table = TinyDB("userbearbetting.json")


def new_round_started(epoch):
    # Set the countdown time in seconds
    timer = 270  # 4 minutes and 30seconds
    time.sleep(timer)
    # get data of userbull and userbear of this epouch
    userbullbettingdata = userbull_table.search(where("epoch") == epoch)
    userbearbettingdata = userbear_table.search(where("epoch") == epoch)

    if userbearbettingdata == [] or userbullbettingdata == []:
        userbullbettingdata = [{"amount": 1, "bettingcount": 2}]
        userbearbettingdata = [{"amount": 2, "bettingcount": 5}]

    userbullbettingdata=userbullbettingdata[0]
    userbearbettingdata=userbearbettingdata[0]


    data = [
        {
            "bet": "bull",
            "betting amount": userbullbettingdata["amount"],
            "betting count": userbullbettingdata["bettingcount"],
        },
        {
            "bet": "bear",
            "betting amount": userbearbettingdata["amount"],
            "betting count": userbearbettingdata["bettingcount"],
        },
    ]
    # writing betting strategy
    my_betting_data = only_bear(data)
    make_bet(epoch, my_betting_data["bet"], my_betting_data["amount"])
    print(f"✅ traded : {my_betting_data["bet"]}")


def end_round(epoch, price):
    if is_bet_win_claimable(epoch):
        print(f"🎉 you won a trade")
        claim_winnings(epoch)
        print("💵 your winnings claimed")  
    else:
        print("😞sorry! you lose a trade")
    print("<<---------------------------------------------------------->>")
    print(f"⏰ new round will start in 5minutes -- Round No: {epoch+1}")
    print(f"your current balance is {get_bnb_balance()}BNB")


def add_user_betting_data(bet, eventdata):
    amount = eventdata[1]
    epoch = eventdata[2]

    userbetting_table = userbear_table
    if bet == "bull":
        userbetting_table = userbull_table

    # check if already avilable epoch just increase amount and also add betting count
    if userbetting_table.search(where("epoch") == epoch):
        # get amount and increase and update
        userbetting_table.update(
            {
                "amount": amount
                + userbetting_table.search(where("epoch") == epoch)[0]["amount"]
            },
            where("epoch") == epoch,
        )
        # increasse betting count
        userbetting_table.update(
            {
                "bettingcount": userbetting_table.search(where("epoch") == epoch)[0][
                    "bettingcount"
                ]
                + 1
            },
            where("epoch") == epoch,
        )
    else:
        userbetting_table.insert({"epoch": epoch, "amount": amount, "bettingcount": 1})

