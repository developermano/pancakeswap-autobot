def high_user_betcount_strategy(bet_data):
    platform_low_bet_amount = 0.001
    # Access the first dictionary (bet on "bull")
    bull_bet = bet_data[0]
    bull_bet_count = bull_bet["betting count"]

    # Access the second dictionary (bet on "bear")
    bear_bet = bet_data[1]
    bear_bet_count = bear_bet["betting count"]

    if bull_bet_count > bear_bet_count:
        return {"bet": "bull", "amount": platform_low_bet_amount}
    else:
        return {"bet": "bear", "amount": platform_low_bet_amount}


def high_user_betamount_strategy(bet_data):
    platform_low_bet_amount = 0.001
    # Access the first dictionary (bet on "bull")
    bull_bet = bet_data[0]
    bull_bet_amount = bull_bet["betting amount"]

    # Access the second dictionary (bet on "bear")
    bear_bet = bet_data[1]
    bear_bet_amount = bear_bet["betting amount"]

    if bull_bet_amount > bear_bet_amount:
        return {"bet": "bull", "amount": platform_low_bet_amount}
    else:
        return {"bet": "bear", "amount": platform_low_bet_amount}

def only_bear(betdata):
    platform_low_bet_amount = 0.001
    return {"bet": "bear", "amount": platform_low_bet_amount}