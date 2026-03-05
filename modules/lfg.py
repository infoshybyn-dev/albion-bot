import disnake

limits = {
    "Tank": 1,
    "Healer": 2,
    "Support": 1,
    "Melee": 3,
    "Ranged": 3
}

group = {
    "Tank": [],
    "Healer": [],
    "Support": [],
    "Melee": [],
    "Ranged": []
}


class LFGView(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    async def register(self, inter, role):

        if len(group[role]) >= limits[role]:

            await inter.response.send_message(
                "❌ Slot full",
                ephemeral=True
            )
            return

        group[role].append(inter.user)

        await inter.response.send_message(
            f"✅ You joined as **{role}**",
            ephemeral=True
        )

        await check_ready(inter)


    # КНОПКИ ↓↓↓

    @disnake.ui.button(label="🛡 Tank", style=disnake.ButtonStyle.red)
    async def tank(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.register(inter, "Tank")


    @disnake.ui.button(label="💚 Healer", style=disnake.ButtonStyle.green)
    async def healer(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.register(inter, "Healer")


    @disnake.ui.button(label="⚔ Melee DPS", style=disnake.ButtonStyle.blurple)
    async def melee(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.register(inter, "Melee")


    @disnake.ui.button(label="🏹 Ranged DPS", style=disnake.ButtonStyle.blurple)
    async def ranged(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.register(inter, "Ranged")


    @disnake.ui.button(label="⭐ Support", style=disnake.ButtonStyle.gray)
    async def support(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.register(inter, "Support")


async def check_ready(inter):

    players = sum(len(v) for v in group.values())

    if players >= 5:

        mentions = []

        for role in group:
            for user in group[role]:
                mentions.append(user.mention)

        await inter.channel.send(
            "⚔ **Group Ready!**\n" + " ".join(mentions)
        )
