import disnake

class LFGView(disnake.ui.View):
    def __init__(self, location, organizer, roles_needed):
        super().__init__(timeout=None)
        # roles_needed = {"Танк": 1, "Хіл": 2, "Меле": 2, "Рейндж": 2, "Саппорт":1}
        self.roles = {role: [] for role in roles_needed}
        self.limits = roles_needed
        self.location = location
        self.organizer = organizer

    def build_embed(self):
        embed = disnake.Embed(
            title=f"⚔ Збір на {self.location}",
            description=f"Організатор: {self.organizer.mention}\nНатисніть кнопку, щоб приєднатись",
            color=0xff0000
        )
        for role, players in self.roles.items():
            embed.add_field(name=role, value="\n".join(p.mention for p in players) if players else "-", inline=False)
        return embed

    async def register(self, inter, role):
        user = inter.user
        for r in self.roles:
            if user in self.roles[r]:
                self.roles[r].remove(user)
        if len(self.roles[role]) >= self.limits[role]:
            await inter.response.send_message("❌ Слот зайнятий", ephemeral=True)
            return
        self.roles[role].append(user)
        await inter.response.defer()
        await inter.message.edit(embed=self.build_embed(), view=self)
        await self.check_ready(inter)

    async def leave(self, inter):
        user = inter.user
        for role in self.roles:
            if user in self.roles[role]:
                self.roles[role].remove(user)
        await inter.response.defer()
        await inter.message.edit(embed=self.build_embed(), view=self)

    async def check_ready(self, inter):
        total = sum(len(v) for v in self.roles.values())
        total_needed = sum(self.limits.values())
        if total >= total_needed:
            mentions = [user.mention for role in self.roles for user in self.roles[role]]
            await inter.channel.send("⚔ **ГРУПА ГОТОВА!**\n" + " ".join(mentions))

    # Кнопки для всіх ролей
    @disnake.ui.button(label="🛡 Танк", style=disnake.ButtonStyle.red)
    async def tank(self, button, inter):
        await self.register(inter, "Танк")

    @disnake.ui.button(label="💚 Хіл", style=disnake.ButtonStyle.green)
    async def healer(self, button, inter):
        await self.register(inter, "Хіл")

    @disnake.ui.button(label="⚔ Меле", style=disnake.ButtonStyle.blurple)
    async def melee(self, button, inter):
        await self.register(inter, "Меле")

    @disnake.ui.button(label="🏹 Рейндж", style=disnake.ButtonStyle.blurple)
    async def ranged(self, button, inter):
        await self.register(inter, "Рейндж")

    @disnake.ui.button(label="⭐ Саппорт", style=disnake.ButtonStyle.gray)
    async def support(self, button, inter):
        await self.register(inter, "Саппорт")

    @disnake.ui.button(label="❌ Вийти", style=disnake.ButtonStyle.secondary)
    async def leave_btn(self, button, inter):
        await self.leave(inter)
