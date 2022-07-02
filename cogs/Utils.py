from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.errors import *
from discord import Member,AuditLogAction, Embed
from utils import *

class Utils(Cog):

    @commands.Cog.listener()
    async def on_member_update(self, before:Member, member:Member):
        if(member.nick != before.nick):
            guild = before.guild
            async for entry in guild.audit_logs(action = AuditLogAction.member_update):
                if(entry.user.id == self.bot.user.id):
                    return

                if(entry.user.id != member.id):
                    await member.edit(nick=before.nick)
    

    @commands.command()
    async def fix(self, ctx:Context):
        reference = ctx.message.reference

        if not reference:
            await ctx.send(Saying.random_get(2), delete_after = 3)
            return

        message = reference.resolved
        content = message.content.replace(' ',' ⁠')
        special_chars = ('\\', '_', '*', '`', '>', '||', '~~')
        for chr in special_chars:
            content = content.replace(chr, '\\' + chr)

        embed = Embed(description = content)
        embed.set_footer(text = f'from {message.author.display_name}', icon_url = message.author.avatar.url)
        await ctx.send(embed = embed)
    


def setup(bot: commands.Bot):
    bot.add_cog(Utils(bot))