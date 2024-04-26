from discord.ext import commands, tasks
from discord.ext.commands.context import Context
from discord.ext.commands.errors import *
from discord import (
    Member,
    AuditLogAction,
    Embed,
    application_command,
    ApplicationContext,
)
from utils import Saying
from .keep_alive_tool.Components import ManagerView, create_domains_status_embeds
from .keep_alive_tool.DomainStatusChecker import record_domains_status


class Utils(commands.Cog):

    @tasks.loop(minutes=1)
    async def task_record_domains_status(self):
        await record_domains_status()

    @application_command(
        discretion="保持網站上線",
        guild_ids=[887196342135451648, 922851148510134293],
    )
    async def keep_alive(self, ctx: ApplicationContext):
        embeds = await create_domains_status_embeds(str(ctx.author.id))
        interaction = await ctx.respond(
            "網域狀態列表", embeds=embeds, ephemeral=True
        )
        await interaction.edit_original_response(view=ManagerView(manager_interaction=interaction))

    @commands.Cog.listener()
    async def on_member_update(self, before: Member, member: Member):
        if member.nick != before.nick:
            guild = before.guild
            async for entry in guild.audit_logs(action=AuditLogAction.member_update):
                if entry.user.id == self.bot.user.id:
                    return

                if entry.user.id != member.id:
                    await member.edit(nick=before.nick)

    @commands.command()
    async def fix(self, ctx: Context):
        reference = ctx.message.reference

        if not reference:
            await ctx.send(Saying.random_get(2), delete_after=3)
            return

        message = reference.resolved
        content = message.content.replace(" ", " ⁠")
        special_chars = ("\\", "_", "*", "`", ">", "||", "~~")
        for chr in special_chars:
            content = content.replace(chr, "\\" + chr)

        embed = Embed(description=content)
        embed.set_footer(
            text=f"from {message.author.display_name}",
            icon_url=message.author.avatar.url,
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Utils(bot))
