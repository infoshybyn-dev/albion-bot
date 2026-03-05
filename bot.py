import disnake
from disnake.ext import commands

from config import TOKEN, RRA
from database.db import init_db
from modules.lfg import LFGView
from modules.economy import craft_profit
from modules.refine import refine_profit

bot = commands.InteractionBot()


@bot.event
async def on_ready():

    await init_db()

    print("Albion Guild Bot Ready")


@bot.slash_command(description="Create PvE group")
async def lfg(inter):

    embed = disnake.Embed(
        title="PvE Group",
        description="Choose your role",
        color=0xff0000
    )

    await inter.send(embed=embed, view=LFGView())


@bot.slash_command(description="Craft profit calculator")
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
        title="Craft Profit",
        color=0x00ff9c
    )

    embed.add_field(name="City", value=city)
    embed.add_field(name="Profit", value=f"{profit} silver")

    await inter.send(embed=embed)


@bot.slash_command(description="Refine profit calculator")
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
        rra,
        station_tax
    )

    embed = disnake.Embed(
        title="Refine Profit",
        color=0x00ffff
    )

    embed.add_field(name="City", value=city)
    embed.add_field(name="Profit", value=f"{profit} silver")

    await inter.send(embed=embed)


bot.run(TOKEN)
