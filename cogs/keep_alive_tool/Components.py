from discord.ui import View, Modal, InputText, button, Select
from discord import Interaction, Embed, ButtonStyle, SelectOption
from .FileHandler import *
from .DomainManager import *


async def create_domains_status_embeds(uid: str):
    embeds = {
        "ONLINE": Embed(title="😀 運行中", color=0xA3BE8C),
        "TIMEOUT": Embed(title="😴 連線逾時", color=0xD08770),
        "ERROR": Embed(title="😵 錯誤", color=0xBF616A)
    }

    for domain, domain_status in (await get_domains_status(uid)).items():
        embeds[domain_status['status']].add_field(
            name="\u200b",
            value=f"```{domain} ({domain_status['ping']:.0f}ms)```",
            inline=False,
        )
    return embeds.values()


class ManagerView(View):
    def __init__(self, *args, manager_interaction:Interaction, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.manager_interaction = manager_interaction

    @button(label="添加", row=0, style=ButtonStyle.blurple)
    async def first_button_callback(self, button, interaction: Interaction):
        await interaction.response.send_modal(AddDomainModal(manager_interaction=self.manager_interaction))

    @button(label="移除", row=0, style=ButtonStyle.red)
    async def second_button_callback(self, button, interaction:Interaction):
        await interaction.response.defer(ephemeral=True, invisible=False)
        await interaction.followup.send(view=RemoveDomainView(uid=str(interaction.user.id),manager_interaction = self.manager_interaction), ephemeral=True)

class AddDomainModal(Modal):
    def __init__(self, *args, manager_interaction:Interaction, **kwargs) -> None:
        super().__init__(title="添加網域", *args, **kwargs)
        self.add_item(InputText(label="輸入網域/網址"))
        self.edit_original_response = manager_interaction.edit_original_response

    async def callback(self, interaction: Interaction):
        target = self.children[0].value
        uid = str(interaction.user.id)
        res = await add_domain(uid, target)
        if res == RETURNCODE.SUCCESS:
            await self.edit_original_response(embeds=await create_domains_status_embeds(uid))
            await interaction.response.send_message("添加成功" ,ephemeral=True,delete_after=2)
        elif res == RETURNCODE.FAILED:
            await interaction.response.send_message("添加失敗，請檢查是否輸入正確的網域" ,ephemeral=True,delete_after=2)
        elif res == RETURNCODE.DUPLICATE:
            await interaction.response.send_message("網域已經在列表中" ,ephemeral=True,delete_after=2)


class RemoveDomainView(View):
    def __init__(self, *args, uid, manager_interaction:Interaction, **kwargs):
        super().__init__(*args, **kwargs)
        domains = get_domains(uid)
        self.edit_original_response = manager_interaction.edit_original_response
        select = Select(
            placeholder="選擇要移除的網域",
            options=[SelectOption(label=domain, value=domain) for domain in domains],
        )
        select.callback = self.create_select_callback()
        self.add_item(select)

    def create_select_callback(self):
        async def callback(interaction: Interaction):
            target_domain = interaction.data['values'][0]
            uid = str(interaction.user.id)
            if remove_domain(uid, target_domain) == RETURNCODE.SUCCESS:
                await interaction.response.send_message(f"成功移除 `{target_domain}`" ,ephemeral=True,delete_after=2)
                await self.edit_original_response(embeds=await create_domains_status_embeds(uid))
            else:
                await interaction.response.send_message("移除失敗" ,ephemeral=True,delete_after=2)
        return callback
