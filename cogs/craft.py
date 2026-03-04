import discord
from discord import app_commands
from discord.ext import commands

# Реальні RRR
RRR_TABLE = {
    "island_bonus": {"no_focus": 0.285, "focus": 0.497},
    "city_bonus": {"no_focus": 0.367, "focus": 0.539},
    "city_no_bonus": {"no_focus": 0.152, "focus": 0.435},
}

class CraftModal(discord.ui.Modal, title="Калькулятор крафту Albion"):

    base_cost = discord.ui.TextInput(
        label="Собівартість ресурсів (срібло)",
        placeholder="Наприклад: 100000"
    )

    sell_price = discord.ui.TextInput(
        label="Ціна продажу (срібло)",
        placeholder="Наприклад: 160000"
    )

    iv_value = discord.ui.TextInput(
        label="IV (Item Value)",
        placeholder="Наприклад: 200"
    )

    food_price = discord.ui.TextInput(
        label="Ціна за 100 їжі (срібло)",
        placeholder="Наприклад: 350"
    )

    async def on_submit(self, interaction: discord.Interaction):

        base_cost = float(self.base_cost.value)
        sell_price = float(self.sell_price.value)
        iv = float(self.iv_value.value)
        food_price = float(self.food_price.value)

        view = StationView(base_cost, sell_price, iv, food_price)

        await interaction.response.send_message(
            "Оберіть тип станка:",
            view=view,
            ephemeral=True
        )

class StationView(discord.ui.View):

    def __init__(self, base_cost, sell_price, iv, food_price):
        super().__init__(timeout=120)
        self.base_cost = base_cost
        self.sell_price = sell_price
        self.iv = iv
        self.food_price = food_price

    @discord.ui.select(
        placeholder="Тип станка",
        options=[
            discord.SelectOption(label="🏝 Острів + бонус міста", value="island_bonus"),
            discord.SelectOption(label="🏙 Місто + бонус", value="city_bonus"),
            discord.SelectOption(label="🏙 Місто без бонусу", value="city_no_bonus"),
        ],
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):

        station_type = select.values[0]
        view = FocusView(
            self.base_cost,
            self.sell_price,
            self.iv,
            self.food_price,
            station_type
        )

        await interaction.response.edit_message(
            content="Використовувати Focus?",
            view=view
        )

class FocusView(discord.ui.View):

    def __init__(self, base_cost, sell_price, iv, food_price, station_type):
        super().__init__(timeout=120)
        self.base_cost = base_cost
        self.sell_price = sell_price
        self.iv = iv
        self.food_price = food_price
        self.station_type = station_type

    async def calculate(self, interaction, use_focus):

        # 1️⃣ Nutrition
        nutrition = self.iv * 0.1125

        # 2️⃣ Податок станка
        tax_cost = (nutrition / 100) * self.food_price

        # 3️⃣ RRR
        rrr = RRR_TABLE[self.station_type]["focus" if use_focus else "no_focus"]

        returned_value = self.base_cost * rrr
        effective_resource_cost = self.base_cost - returned_value

        total_cost = effective_resource_cost + tax_cost
        profit = self.sell_price - total_cost
        roi = (profit / total_cost) * 100 if total_cost > 0 else 0

        embed = discord.Embed(
            title="📊 Результат крафту",
            color=discord.Color.green()
        )

        embed.add_field(name="Nutrition", value=f"{nutrition:.2f}")
        embed.add_field(name="Повернення ресурсів", value=f"{rrr*100:.1f}%")
        embed.add_field(name="Повернуто срібла", value=f"{returned_value:,.0f}")
        embed.add_field(name="Податок станка", value=f"{tax_cost:,.0f}")
        embed.add_field(name="Фактична собівартість", value=f"{total_cost:,.0f}", inline=False)
        embed.add_field(name="Чистий прибуток", value=f"{profit:,.0f}")
        embed.add_field(name="ROI", value=f"{roi:.2f}%")

        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="Без Focus", style=discord.ButtonStyle.gray)
    async def no_focus(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.calculate(interaction, False)

    @discord.ui.button(label="З Focus", style=discord.ButtonStyle.green)
    async def focus(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.calculate(interaction, True)

class Craft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="крафт", description="Відкрити повний калькулятор крафту")
    async def craft(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CraftModal())

async def setup(bot):
    await bot.add_cog(Craft(bot))
