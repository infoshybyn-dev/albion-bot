import discord
from discord import app_commands
from discord.ext import commands

class Craft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="craft", description="Калькулятор крафту")
    async def craft(self, interaction: discord.Interaction, cost: int, sell_price: int):
        profit = sell_price - cost

        embed = discord.Embed(
            title="🛠️ Крафт результат",
            color=discord.Color.green()
        )
        embed.add_field(name="Собівартість", value=cost)
        embed.add_field(name="Продаж", value=sell_price)
        embed.add_field(name="Профіт", value=profit)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Craft(bot))
