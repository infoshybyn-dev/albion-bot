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
                "Slot full",
                ephemeral=True
            )
            return

        group[role].append(inter.user)

        await inter.response.send_message(
            f"You joined as **{role}**",
            ephemeral=True
        )

        await check_ready(inter)


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
