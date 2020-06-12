import fortnitepy
import asyncio

from .get_cosmetic import get_emote

async def event_party_invite(client: fortnitepy.Client, invitation: fortnitepy.PartyInvitation):
    if invitation.sender.id in client.settings["owners"]:
        try:
            await client.user.party.me.set_emote('EID_Wave')
            await asyncio.sleep(2)
        except: pass

        try:
            await invitation.accept()
        except:
            await invitation.sender.send('Sorry, something wen\'t wrong with accepting your invitation')
    
    # if invitation.sender.id in client.settings["blocked"]:
    #     try:
    #         await invitation.sender.send('Sorry you are on my block list and I need can\'t accept your Invite, join my Discord: https://discord.gg/GPSPwh6\nTo get your own Fortnite Lobby Bot')
    #     except: pass

async def event_party_member_promote(client: fortnitepy.Client, old_leader: fortnitepy.PartyMember, new_leader: fortnitepy.PartyMember):
    if new_leader.id == client.user.id:
        try:
            if old_leader is not None:
                await client.user.party.send(f'Thanks {old_leader.display_name} for promoting me')
            else:
                await client.user.party.send(f'Thanks for promoting me')
        finally:
            try:
                await client.user.party.me.set_emote("EID_TrueLove")
            except: pass

async def event_party_member_join(client: fortnitepy.Client, member: fortnitepy.PartyMember):
    if member.id == client.user.id:
        if client.settings["cosmetics"]["emote"]:
            await client.user.party.me.set_emote(client.settings["cosmetics"]["emote"])
        elif client.settings["cosmetics"]["emoji"]:
            await client.user.party.me.set_emoji(client.settings["cosmetics"]["emoji"])
    else:
        if not client.has_friend(member.id):
            try:
                await client.add_friend(member.id)
            except: pass
        
async def event_party_member_leave(client: fortnitepy.Client, member: fortnitepy.PartyMember):
    pass

async def event_party_member_confirm(client: fortnitepy.Client, member: fortnitepy.PartyMember):
    pass