import discord
from discord import app_commands
from discord.ext import commands

CITY_BONUSES = {
    "lymhurst": 0.15,
    "bridgewatch": 0.15,
    "martlock": 0.15,
    "fort_sterling": 0.15,
    "thetford": 0.15,
    "brecilien": 0.10
}

class Craft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="craft", description="Крафт з RRR + місто + premium")
    async def craft(
        self,
        interaction: discord.Interaction,
        base_cost: int,
        sell_price: int,
        rrr: float,          # приклад: 0.35
        city: str,           # тепер є місто
        premium: bool
    ):

        premium_bonus = 0.005 if premium else 0
        city_bonus = CITY_BONUSES.get(city.lower(), 0)

        # головна формула
        effective_cost = base_cost * (1 - rrr - city_bonus) * (1 - premium_bonus)

        profit = sell_price - effective_cost
        roi = (profit / effective_cost) * 100 if effective_cost > 0 else 0

        embed = discord.Embed(
            title="🛠️ Albion Craft Result",
            color=discord.Color.green()
        )

        embed.add_field(name="Базова вартість", value=f"{base_cost:,}")
        embed.add_field(name="RRR", value=f"{rrr*100:.1f}%")
        embed.add_field(name="Бонус міста", value=f"{city_bonus*100:.1f}%")
        embed.add_field(name="Premium", value="Так" if premium else "Ні", inline=False)
        embed.add_field(name="Фактична собівартість", value=f"{effective_cost:,.0f}")
        embed.add_field(name="Профіт", value=f"{profit:,.0f}")
        embed.add_field(name="ROI", value=f"{roi:.2f}%")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Craft(bot))
