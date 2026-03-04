import discord
from discord import app_commands
from discord.ext import commands

class JoinView(discord.ui.View):
    def __init__(self, max_players):
        super().__init__(timeout=None)
        self.players = []
        self.max_players = max_players

    @discord.ui.button(label="✅ Записатись", style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user

        if user in self.players:
            await interaction.response.send_message("Ти вже записаний.", ephemeral=True)
            return

        if len(self.players) >= self.max_players:
            await interaction.response.send_message("Група вже повна!", ephemeral=True)
            return

        self.players.append(user)

        embed = interaction.message.embeds[0]
        player_list = "\n".join([p.mention for p in self.players])

        embed.set_field_at(
            0,
            name="Учасники",
            value=player_list if player_list else "Поки що нікого",
            inline=False
        )

        await interaction.response.edit_message(embed=embed, view=self)

class CTA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cta", description="Створити PvE активність")
    async def cta(self, interaction: discord.Interaction, activity: str, players: int):
        embed = discord.Embed(
            title=f"⚔️ {activity}",
            color=discord.Color.red()
        )

        embed.add_field(
            name="Учасники",
            value="Поки що нікого",
            inline=False
        )

        view = JoinView(players)

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(CTA(bot))
