import discord
from discord import app_commands
from discord.ext import commands

class CTAView(discord.ui.View):
    def __init__(self, max_players):
        super().__init__(timeout=None)
        self.players = []
        self.max_players = max_players

    def build_embed(self, activity):
        embed = discord.Embed(
            title=f"⚔ {activity}",
            color=discord.Color.red()
        )

        player_list = "\n".join([p.mention for p in self.players]) if self.players else "Поки нікого"

        embed.add_field(name="Учасники", value=player_list, inline=False)
        embed.add_field(name="Місця", value=f"{len(self.players)}/{self.max_players}")

        return embed

    @discord.ui.button(label="✅ Записатись", style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user in self.players:
            await interaction.response.send_message("Ти вже записаний.", ephemeral=True)
            return

        if len(self.players) >= self.max_players:
            await interaction.response.send_message("Група повна!", ephemeral=True)
            return

        self.players.append(interaction.user)

        embed = self.build_embed(interaction.message.embeds[0].title)

        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="❌ Вийти", style=discord.ButtonStyle.red)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user in self.players:
            self.players.remove(interaction.user)

        embed = self.build_embed(interaction.message.embeds[0].title)

        await interaction.response.edit_message(embed=embed)

class CTA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cta", description="Створити активність")
    async def cta(self, interaction: discord.Interaction, activity: str, players: int):

        view = CTAView(players)
        embed = view.build_embed(activity)

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(CTA(bot))
