import disnake
from disnake.ext import commands
from modules.lfg import LFGView
from modules.economy import craft_profit, refine_profit
from config import DISCORD_TOKEN, RRA
from database.db import init_db

bot = commands.InteractionBot()

@bot.event
async def on_ready():
    await init_db()
    print(f"Albion Bot готовий як {bot.user}")


# -----------------------------
# LFG – модальне вікно
# -----------------------------
class LFGModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Локація", 
                placeholder="Введіть місце",
                custom_id="location"
            ),
            disnake.ui.TextInput(
                label="Ролі (через кому)",
                placeholder="Танк, Хіл, Порізка, Дд, Дд",
                custom_id="roles"
            )
        ]
        super().__init__(title="Створити збір", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        location = self.text_values["location"]
        roles_raw = self.text_values["roles"]

               roles_needed = {}
        try:
            parts = [part.strip() for part in roles_raw.split(",") if part.strip()]

            if not parts:
                raise ValueError("empty")

            for role in parts:
                roles_needed[role] = roles_needed.get(role, 0) + 1

        except Exception:
            await inter.response.send_message(
                "❌ Некоректний формат ролей. Використовуй: Танк, Хіл, Порізка, Дд, Дд",
                ephemeral=True
            )
            return

        view = LFGView(location, inter.user, roles_needed)
        await inter.response.send_message(embed=view.build_embed(), view=view)


@bot.slash_command(description="Створити збір PvE")
async def lfg(inter):
    await inter.response.send_modal(LFGModal())


# -----------------------------
# Craft – модальне вікно
# -----------------------------
class CraftModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label="Ціна предмета", custom_id="item_price"),
            disnake.ui.TextInput(label="Вартість матеріалів", custom_id="material_cost"),
            disnake.ui.TextInput(label="Податок станка", custom_id="station_tax"),
            disnake.ui.TextInput(label="Місто", custom_id="city"),
            disnake.ui.TextInput(label="Преміум? (так/ні)", custom_id="premium")
        ]
        super().__init__(title="Розрахунок крафту", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            item_price = int(self.text_values["item_price"])
            material_cost = int(self.text_values["material_cost"])
            station_tax = int(self.text_values["station_tax"])
            city = self.text_values["city"]
            premium = self.text_values["premium"].lower() == "так"
        except Exception:
            await inter.response.send_message("❌ Некоректні дані", ephemeral=True)
            return

        rra = RRA.get(city)
        profit = craft_profit(item_price, material_cost, station_tax, rra, premium)

        embed = disnake.Embed(title="💰 Прибуток від крафту", color=0x00ff9c)
        embed.add_field(name="Місто", value=city)
        embed.add_field(name="Прибуток", value=f"{profit} срібла")
        await inter.response.send_message(embed=embed)


@bot.slash_command(description="Розрахунок крафту")
async def craft(inter):
    await inter.response.send_modal(CraftModal())


# -----------------------------
# Refine – модальне вікно
# -----------------------------
class RefineModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label="Ціна вихідного предмета", custom_id="output_price"),
            disnake.ui.TextInput(label="Вартість входу", custom_id="input_cost"),
            disnake.ui.TextInput(label="Податок станка", custom_id="station_tax"),
            disnake.ui.TextInput(label="Місто", custom_id="city")
        ]
        super().__init__(title="Розрахунок рефайну", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            output_price = int(self.text_values["output_price"])
            input_cost = int(self.text_values["input_cost"])
            station_tax = int(self.text_values["station_tax"])
            city = self.text_values["city"]
        except Exception:
            await inter.response.send_message("❌ Некоректні дані", ephemeral=True)
            return

        rra = RRA.get(city)
        profit = refine_profit(output_price, input_cost, station_tax, rra)

        embed = disnake.Embed(title="⚒ Прибуток від рефайну", color=0x00ffff)
        embed.add_field(name="Місто", value=city)
        embed.add_field(name="Прибуток", value=f"{profit} срібла")
        await inter.response.send_message(embed=embed)


@bot.slash_command(description="Розрахунок рефайну")
async def refine(inter):
    await inter.response.send_modal(RefineModal())


# -----------------------------
# Запуск бота
# -----------------------------
bot.run(DISCORD_TOKEN)
