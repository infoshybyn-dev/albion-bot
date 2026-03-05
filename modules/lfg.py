import disnake

class LFGView(disnake.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.roles = {
            "Tank": [],
            "Healer": [],
            "Support": [],
            "Melee": [],
            "Ranged": []
        }

        self.limits = {
            "Tank": 1,
            "Healer": 2,
            "Support": 1,
            "Melee": 3,
            "Ranged": 3
        }


    def build_embed(self):

        embed = disnake.Embed(
            title="⚔ PvE Group",
            description="Click button to join",
            color=0xff0000
        )

        for role in self.roles:

            players = self.roles[role]

            if players:
                value = "\n".join(p.mention for p in players)
            else:
                value = "-"

            embed.add_field(name=role, value=value)

        return embed


    async def update_message(self, inter):

        await inter.message.edit(embed=self.build_embed(), view=self)


    async def register(self, inter, role):

        user = inter.user

        for r in self.roles:
            if user in self.roles[r]:
                self.roles[r].remove(user)

        if len(self.roles[role]) >= self.limits[role]:

            await inter.response.send_message(
                "❌ Slot full",
                ephemeral=True
            )
            return

        self.roles[role].append(user)

        await inter.response.defer()

        await self.update_message(inter)

        await self.check_ready(inter)


    async def leave(self, inter):

        user = inter.user

        for role in self.roles:
            if user in self.roles[role]:
                self.roles[role].remove(user)

        await inter.response.defer()

        await self.update_message(inter)


    async def check_ready(self, inter):

        total = sum(len(v) for v in self.roles.values())

        if total >= 5:

            players = []

            for role in self.roles:
                for user in self.roles[role]:
                    players.append(user.mention)

            await inter.channel.send(
                "⚔ **GROUP READY**\n" + " ".join(players)
            )


    @disnake.ui.button(label="🛡 Tank", style=disnake.ButtonStyle.red)
    async def tank(self, button, inter):
        await self.register(inter, "Tank")


    @disnake.ui.button(label="💚 Healer", style=disnake.ButtonStyle.green)
    async def healer(self, button, inter):
        await self.register(inter, "Healer")


    @disnake.ui.button(label="⚔ Melee", style=disnake.ButtonStyle.blurple)
    async def melee(self, button, inter):
        await self.register(inter, "Melee")


    @disnake.ui.button(label="🏹 Ranged", style=disnake.ButtonStyle.blurple)
    async def ranged(self, button, inter):
        await self.register(inter, "Ranged")


    @disnake.ui.button(label="⭐ Support", style=disnake.ButtonStyle.gray)
    async def support(self, button, inter):
        await self.register(inter, "Support")


    @disnake.ui.button(label="❌ Leave", style=disnake.ButtonStyle.secondary)
    async def leave_btn(self, button, inter):
        await self.leave(inter)
