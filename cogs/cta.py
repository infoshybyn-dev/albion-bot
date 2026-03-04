import discord
from discord import app_commands
from discord.ext import commands

class CTA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cta", description="Створити PvE активність")
    async def cta(self, interaction: discord.Interaction, activity: str, players: int):
        embed = discord.Embed(
            title=f"⚔️ {activity}",
            description=f"Потрібно гравців: {players}",
            color=discord.Color.red()
        )
        embed.add_field(name="Учасники", value="Поки що нікого", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(CTA(bot))
