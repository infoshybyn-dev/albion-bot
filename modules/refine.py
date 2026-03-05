def refine_profit(
    output_price,
    input_cost,
    rra,
    station_tax
):

    returned = input_cost * rra

    total_cost = input_cost - returned + station_tax

    profit = output_price - total_cost

    return round(profit)
