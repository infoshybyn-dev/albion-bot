import discord
from discord import app_commands
from discord.ext import commands

class Refine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="refine", description="Калькулятор перекрафту")
    async def refine(self, interaction: discord.Interaction, raw_amount: int, return_rate: float):
        returned = raw_amount * return_rate
        result = raw_amount + returned

        embed = discord.Embed(
            title="⛏️ Результат перекрафту",
            color=discord.Color.blue()
        )
        embed.add_field(name="Сирий ресурс", value=raw_amount)
        embed.add_field(name="Повернення", value=f"{returned:.2f}")
        embed.add_field(name="Разом", value=f"{result:.2f}")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Refine(bot))
