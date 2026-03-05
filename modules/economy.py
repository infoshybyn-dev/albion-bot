from config import PREMIUM_TAX, NO_PREMIUM_TAX, SETUP_FEE


def craft_profit(item_price, material_cost, station_tax, rra, premium=True):

    auction_tax = item_price * (PREMIUM_TAX if premium else NO_PREMIUM_TAX)

    setup_fee = item_price * SETUP_FEE

    returned = material_cost * rra

    profit = (
        item_price
        - auction_tax
        - setup_fee
        - material_cost
        - station_tax
        + returned
    )

    return round(profit)


def refine_profit(output_price, input_cost, station_tax, rra):

    returned = input_cost * rra

    total_cost = input_cost - returned + station_tax

    profit = output_price - total_cost

    return round(profit)
