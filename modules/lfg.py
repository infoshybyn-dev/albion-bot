import disnake


class RoleButton(disnake.ui.Button):
    def __init__(self, role_name: str):
        self.role_name = role_name
        super().__init__(
            label=role_name[:80],
            style=disnake.ButtonStyle.secondary
        )

    async def callback(self, inter: disnake.MessageInteraction):
        view = self.view
        if not isinstance(view, LFGView):
            await inter.response.send_message("❌ Помилка view", ephemeral=True)
            return

        await view.register(inter, self.role_name)


class LeaveButton(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            label="❌ Покинути групу",
            style=disnake.ButtonStyle.danger,
            row=1
        )

    async def callback(self, inter: disnake.MessageInteraction):
        view = self.view
        if not isinstance(view, LFGView):
            await inter.response.send_message("❌ Помилка view", ephemeral=True)
            return

        await view.leave(inter)


class LFGView(disnake.ui.View):
    def __init__(self, location, event_time, organizer, roles_needed, activity_name="Групік 8.2"):
        super().__init__(timeout=3600)

        self.location = location
        self.event_time = event_time
        self.organizer = organizer
        self.activity_name = activity_name

        self.roles = {role: [] for role in roles_needed}
        self.limits = roles_needed

        row = 0
        for role in self.roles.keys():
            self.add_item(RoleButton(role_name=role))
        self.add_item(LeaveButton())

    def build_embed(self):
        embed = disnake.Embed(
            title="🛡️ ФОРМУВАННЯ ЗАГОНУ",
            color=0x3498DB
        )

        embed.description = (
            f"👑 **ОРГ:** {self.organizer.mention}  |  📍 **ДЕ:** {self.location}\n"
            f"⚔️ **ЩО:** {self.activity_name}\n"
            f"🕒 **ЧАС:** {self.event_time}\n"
            f"────────────────────────"
        )

        lines = []
        for role, players in self.roles.items():
            limit = self.limits[role]

            if players:
                filled = len(players)
                mentions = ", ".join(user.mention for user in players)
                lines.append(f"**{role}:** {'🟢' * filled} {mentions}")
            else:
                lines.append(f"**{role}:** 🟢 *Вільне місце*")

            if limit > 1 and players:
                for _ in range(limit - len(players)):
                    lines.append(f"**{role}:** 🟢 *Вільне місце*")
            elif limit > 1 and not players:
                for _ in range(limit - 1):
                    lines.append(f"**{role}:** 🟢 *Вільне місце*")

        embed.add_field(
            name="Склад групи",
            value="\n".join(lines),
            inline=False
        )

        total = sum(len(players) for players in self.roles.values())
        total_needed = sum(self.limits.values())
        embed.set_footer(text=f"Зібрано {total}/{total_needed}")

        return embed

    async def register(self, inter: disnake.MessageInteraction, role: str):
        user = inter.user

        old_role = None
        for r in self.roles:
            if user in self.roles[r]:
                old_role = r
                break

        if old_role == role:
            await inter.response.send_message(
                f"Ти вже записаний як **{role}**",
                ephemeral=True
            )
            return

        if old_role:
            self.roles[old_role].remove(user)

        if len(self.roles[role]) >= self.limits[role]:
            await inter.response.send_message("❌ У цій ролі вже немає місця", ephemeral=True)
            return

        self.roles[role].append(user)

        await inter.response.edit_message(
            embed=self.build_embed(),
            view=self
        )

        await self.check_ready(inter)

    async def leave(self, inter: disnake.MessageInteraction):
        user = inter.user
        removed = False

        for role in self.roles:
            if user in self.roles[role]:
                self.roles[role].remove(user)
                removed = True

        if not removed:
            await inter.response.send_message(
                "Ти ще не записаний у групу",
                ephemeral=True
            )
            return

        await inter.response.edit_message(
            embed=self.build_embed(),
            view=self
        )

    async def check_ready(self, inter: disnake.MessageInteraction):
        total = sum(len(v) for v in self.roles.values())
        total_needed = sum(self.limits.values())

        if total >= total_needed:
            mentions = []
            for role_users in self.roles.values():
                for user in role_users:
                    mentions.append(user.mention)

            await inter.channel.send(
                f"✅ **Група зібрана!**\n{' '.join(mentions)}"
            )
