import discord
from discord import app_commands
from discord.ext import commands

RRR_TABLE = {
    "island_bonus": {"no_focus": 0.285, "focus": 0.497},
    "city_bonus": {"no_focus": 0.367, "focus": 0.539},
    "city_no_bonus": {"no_focus": 0.152, "focus": 0.435},
}

class CraftView(discord.ui.View):
    def __init__(self, base_cost, sell_price, station_tax):
        super().__init__(timeout=120)
        self.base_cost = base_cost
        self.sell_price = sell_price
        self.station_tax = station_tax

    @discord.ui.select(
        placeholder="Оберіть тип станка",
        options=[
            discord.SelectOption(label="🏝 Острів + бонус міста", value="island_bonus"),
            discord.SelectOption(label="🏙 Місто + бонус", value="city_bonus"),
            discord.SelectOption(label="🏙 Місто без бонусу", value="city_no_bonus"),
        ],
    )
    async def select_station(self, interaction: discord.Interaction, select: discord.ui.Select):

        station_type = select.values[0]

        view = FocusView(
            self.base_cost,
            self.sell_price,
            self.station_tax,
            station_type
        )

        await interaction.response.edit_message(
            content="Оберіть режим крафту:",
            view=view
        )

class FocusView(discord.ui.View):
    def __init__(self, base_cost, sell_price, station_tax, station_type):
        super().__init__(timeout=120)
        self.base_cost = base_cost
        self.sell_price = sell_price
        self.station_tax = station_tax
        self.station_type = station_type

    @discord.ui.button(label="Без Focus", style=discord.ButtonStyle.gray)
    async def no_focus(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.calculate(interaction, False)

    @discord.ui.button(label="З Focus", style=discord.ButtonStyle.green)
    async def with_focus(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.calculate(interaction, True)

    async def calculate(self, interaction, use_focus):

        rrr = RRR_TABLE[self.station_type]["focus" if use_focus else "no_focus"]

        material_cost = self.base_cost * (1 - rrr)
        tax_cost = self.base_cost * self.station_tax
        effective_cost = material_cost + tax_cost

        profit = self.sell_price - effective_cost
        roi = (profit / effective_cost) * 100 if effective_cost > 0 else 0

        embed = discord.Embed(
            title="🛠 Albion Craft Result",
            color=discord.Color.green()
        )

        embed.add_field(name="RRR", value=f"{rrr*100:.1f}%")
        embed.add_field(name="Собівартість", value=f"{effective_cost:,.0f}")
        embed.add_field(name="Профіт", value=f"{profit:,.0f}")
        embed.add_field(name="ROI", value=f"{roi:.2f}%")

        await interaction.response.edit_message(embed=embed, view=None)

class Craft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="craft", description="Повний калькулятор Albion")
    async def craft(
        self,
        interaction: discord.Interaction,
        base_cost: int,
        sell_price: int,
        station_tax: float
    ):

        view = CraftView(base_cost, sell_price, station_tax)

        await interaction.response.send_message(
            "Оберіть тип станка:",
            view=view
        )

async def setup(bot):
    await bot.add_cog(Craft(bot))
