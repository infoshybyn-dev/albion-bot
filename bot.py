import disnake
from disnake.ext import commands

from config import TOKEN, RRA
from modules.economy import craft_profit, refine_profit
from modules.lfg import LFGView
from database.db import init_db

bot = commands.InteractionBot()


@bot.event
async def on_ready():

    await init_db()

    print("Albion Bot Ready")


@bot.slash_command(description="Create PvE group")
async def lfg(inter):

    view = LFGView()

    await inter.send(
        embed=view.build_embed(),
        view=view
    )


@bot.slash_command(description="Craft profit")
async def craft(
    inter,
    item_price: int,
    material_cost: int,
    station_tax: int,
    city: str,
    premium: bool = True
):

    rra = RRA.get(city)

    profit = craft_profit(
        item_price,
        material_cost,
        station_tax,
        rra,
        premium
    )

    embed = disnake.Embed(
        title="💰 Craft Profit",
        color=0x00ff9c
    )

    embed.add_field(name="City", value=city)
    embed.add_field(name="Profit", value=f"{profit} silver")

    await inter.send(embed=embed)


@bot.slash_command(description="Refine profit")
async def refine(
    inter,
    output_price: int,
    input_cost: int,
    station_tax: int,
    city: str
):

    rra = RRA.get(city)

    profit = refine_profit(
        output_price,
        input_cost,
        station_tax,
        rra
    )

    embed = disnake.Embed(
        title="⚒ Refine Profit",
        color=0x00ffff
    )

    embed.add_field(name="City", value=city)
    embed.add_field(name="Profit", value=f"{profit} silver")

    await inter.send(embed=embed)


bot.run(TOKEN)
