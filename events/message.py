
import sys
import asyncio
import aiohttp
import fortnitepy

from .get_cosmetic import *

class Access():
    def __init__(self, client: fortnitepy.Client, message):
        self.friends = client.has_friend(message.author.id)
        self.owner = message.author.id in client.settings["owners"]
        self.god_mode = True

def _check_auth(client: fortnitepy.Client, access: Access, command):
    # commands = client.commands
    # if commands[command] == "everyone":
    #     return True
    # elif commands[command] == "party_member":
    #     return access.party_member
    # elif commands[command] == "owners": 
    #     return access.owner

    return True

async def event_message(client: fortnitepy.Client, message: fortnitepy.PartyMessage):
    # if message.author.id in client.settings["blocked"]: return
    if message.author.id == client.user.id: return
    content = message.content.lower()
    args = content.split(" ")
    access = Access(client, message)

    if not client.has_friend(message.author.id):
        return await message.reply(fn_client.settings['Open EZFN Settings']['ifNotFriend'])

        # Friends
    if args[0] == f'?friends' and _check_auth(client, access, "get_friends_count"):
        try:
            await message.reply(f'Total Friends: {len(client.friends)}\nFriends Online: {sum(1 for friend in client.friends.values() if friend.is_online())}')
        except:
            await message.reply('Something wen\'t wrong sorry.')

        # Restart
    # elif args[0] == f'!restart' and _check_auth(client, access, "restart_client"):
    elif args[0] == f'!restart' and access.owner:
        try:
            await message.reply('Restarting...')
            # await client.logout(close_http=True)
            sys.exit() # Glitch should auto restart the script
        except:
            await message.reply('Something wen\'t wrong sorry.')
    
        # Join
    # elif content == '!join' and client.settings["party"]["join_on_invite"]:
    elif content == '!join' and access.owner:
        if client.has_friend(message.author.id):
            try:
                await client.get_friend(message.author.id).join_party()
                await message.reply('Joined your Party.')
            except fortnitepy.PartyError:
                await message.reply('Party was not found.')
            except fortnitepy.Forbidden:
                await message.reply('The party is private.')
            except Exception as e:
                await message.reply('Something wen\'t wrong.')
        else:
            await message.reply('Can\'t join, make sure to accept my Friend Request')
            try:
                await client.add_friend(message.author.id)
            except: pass

        # Leave
    # elif (content == "!leave party" or content == "!leave") and _check_auth(client, access, "leave_party"):
    elif (content == "!leave party" or content == "!leave") and access.owner:
        try:
            await client.user.party.me.set_emote('EID_Wave')
            await asyncio.sleep(2)
        except: pass

        try:
            await client.user.party.me.leave()
            await message.reply("Successfuly left Party.")
        except Exception as e:
            await message.reply('Something wen\'t wrong, try to restart with "!restart"')

        # Stop Emote
    elif content == "!stop emote" or content == "!stopemote" and _check_auth(client, access, "stop_emote"):
        try:
            await client.user.party.me.clear_emote()
            await message.reply("Stopped Dancing!")
        except:
            await message.reply('Something wen\'t wrong sorry.')

        # Ready Up
    elif content == "!ready" and _check_auth(client, access, "ready"):
        try:
            await client.user.party.me.set_ready(True)
            await message.reply("Successfuly set my readiness to ready")
        except:
            await message.reply('Something wen\'t wrong sorry.')

        # Unready
    elif content == "!not ready" or content == "!notready" or content == "!unready" and _check_auth(client, access, "unready"):
        try:
            await client.user.party.me.set_ready(False)
            await message.reply("Successfuly set my readiness to not ready")
        except:
            await message.reply('Something wen\'t wrong sorry.')
        
        # Cosmetic Shortcuts
    elif content == "!purpleskull" and _check_auth(client, access, "cosmetic_shortcuts"):
        try:
            await client.user.party.me.set_outfit("CID_030_Athena_Commando_M_Halloween", variants=client.user.party.me.create_variants(clothing_color=1))
            await message.reply('Skin set to Skull Trooper with Purple Glow variant!')
        except:
            await message.reply('Something wen\'t wrong sorry.')

    elif content == "!pinkghoul" and _check_auth(client, access, "cosmetic_shortcuts"):
        try:
            await client.user.party.me.set_outfit("CID_029_Athena_Commando_F_Halloween", variants=client.user.party.me.create_variants(material=3))
            await message.reply('Skin set to Ghoul Trooper with Pink variant!')
        except:
            await message.reply('Something wen\'t wrong sorry.')

    elif content == "!mintyelf" and _check_auth(client, access, "cosmetic_shortcuts"):
        try:
            await client.user.party.me.set_outfit("CID_051_Athena_Commando_M_HolidayElf", variants=client.user.party.me.create_variants(material=2))
            await message.reply('Skin set to Elf with Minty variant!')
        except:
            await message.reply('Something wen\'t wrong sorry.')

    # elif content == f'!promote' and _check_auth(client, access, "promote_member"):
    elif content == f'!promote' and access.owner:
        try:
            await message.author.promote()
            await message.reply('Successfully promoted you!')
        except Exception as e:
            await message.reply('Sorry, something wen\'t wrong!')

    elif args[0] == "!match":
        party = client.user.party
        players_left = '1'
        if len(args) > 1: players_left = args[1]
        for key,value in {'Location_s': 'InGame', 'NumAthenaPlayersLeft_U': players_left, 'HasPreloadedAthena_b': True,'SpectateAPartyMemberAvailable_b': 'true'}.items():
            try:
                await party.me.patch(updated={key: party.me.meta.set_prop(key, value)})
            except: pass
        await message.reply(f'Successfully joined a match, players left: {players_left}')

    elif content == "!leave match":
        party = client.user.party
        players_left = args[1] or '1'
        for key,value in {'Location_s': 'PreLobby', 'NumAthenaPlayersLeft_U': '0', 'HasPreloadedAthena_b': False,'SpectateAPartyMemberAvailable_b': 'false'}.items():
            try:
                await party.me.patch(updated={key: party.me.meta.set_prop(key, value)})
            except: pass
        await message.reply(f'Successfully left the match')

    elif args[0] == "!skins" and _check_auth(client, access, "cosmetic_shortcuts"):
        if args[1] == "new":
            async with aiohttp.ClientSession() as session:
                new_cosmetics = await session.get("https://benbotfn.tk/api/v1/newCosmetics")
                if new_cosmetics.status == 200:
                    new_cosmetics = await new_cosmetics.json()
                    new_skins = [cosmetic for cosmetic in new_cosmetics["items"] if cosmetic["backendType"] == "AthenaCharacter"]
                    if len(new_skins) == 0:
                        await message.reply('There are no new skins!')
                    else:
                        await message.reply(f'I will now show you {len(new_skins)} new skins, please join my Discord: https://discord.gg/GPSPwh6')
                        for cosmetic in new_skins:
                            if cosmetic["backendType"] == "AthenaCharacter":
                                await client.user.party.me.set_outfit(cosmetic["id"])
                                await asyncio.sleep(0.1)

                        for cosmetic in new_skins:
                            if cosmetic["backendType"] == "AthenaCharacter":
                                await client.user.party.me.set_outfit(cosmetic["id"])
                                await asyncio.sleep(0.1)

                        for cosmetic in new_skins:
                            if cosmetic["backendType"] == "AthenaCharacter":
                                await client.user.party.me.set_outfit(cosmetic["id"])
                                await asyncio.sleep(0.1)

                        for cosmetic in new_skins:
                            if cosmetic["backendType"] == "AthenaCharacter":
                                await client.user.party.me.set_outfit(cosmetic["id"])
                                await asyncio.sleep(0.1)

                        await message.reply('Done with showing the new skin!')
    
    elif content.startswith(("!skin", "!backpack", "!pickaxe", "!emoji","!emote")) and _check_auth(client, access, "change_cosmetics"):
        # language = client.settings.language.cosmetics
        language = "en"
        cosmetic_type = ""

        if "--lang=" in content:
            content = content + " "
            language = GetValue(content,"--lang="," ")
            content = content.replace("--lang=" + language, "").strip()
            print(f'Search language = {language}')

        if args[0] == "!skin":
            cosmetic = await get_skin(GetName("!skin", content), client, language)
            cosmetic_type = "Outfit"
        elif args[0] == "!backpack":
            cosmetic = await get_backpack(GetName("!backpack", content), client, language)
            cosmetic_type = "Back Bling"
        elif args[0] == "!pickaxe":
            cosmetic = await get_pickaxe(GetName("!pickaxe", content), client, language)
            cosmetic_type = "Harvesting Tool"
        elif args[0] == "!emoji":
            cosmetic = await get_emoji(GetName("!emoji", content), client, language)
            cosmetic_type = "Emoji"
        elif args[0] == "!emote":
            cosmetic = await get_emote(GetName("!emote", content), client, language)
            cosmetic_type = "Emote"
        else:
            await message.reply('Sorry, something wen\'t wrong!')
            return

        if not cosmetic:
            await message.reply(f'No {cosmetic_type} with this name found!')
        else:
        
            variants = []

            if content.count('--') > 0: # If there are any variants
                if not cosmetic["variants"]:
                    await message.reply('This skin has no variants!')
                else:
                    for content_variant in GetValues(content):
                        c_variant_channel_name = (content_variant.split("=")[0])[2:]
                        c_variant = content_variant.split("=")[1]

                        for variant in cosmetic["variants"]:
                            if variant["types"][language].lower() == c_variant_channel_name:
                                for option in variant["options"]:
                                    if option["names"][language].lower() == c_variant:
                                        variants.append(create_variant(variant["channel"], option["tag"], item=cosmetic["backendType"]))
            
            # cosmetic_type = (args[0])[1:].capitalize()
            asset = f'{cosmetic["path"]}.{cosmetic["id"]}'

            if args[0] == "!skin":
                await client.user.party.me.set_outfit(asset=asset, variants=variants)
            elif args[0] == "!backpack":
                await client.user.party.me.set_backpack(asset=asset, variants=variants)
            elif args[0] == "!pickaxe":
                await client.user.party.me.set_pickaxe(asset=asset, variants=variants)
            elif args[0] == "!emoji":
                await client.user.party.me.clear_emote()
                await client.user.party.me.set_emoji(asset=asset)
            elif args[0] == "!emote":
                await client.user.party.me.clear_emote()
                await client.user.party.me.set_emote(asset=asset)

            await message.reply(f'{cosmetic_type} set to {cosmetic["names"][language]}')

    elif args[0] == "!playlist" and len(args) > 0:
        if client.user.party.me.leader:
            playlist = await get_playlist(content[10:],client)
            if playlist:
                await client.user.party.set_playlist(playlist=playlist["dev_name"])
                await message.reply(f'Changed Playlist to {playlist["names"]["en"]}')
            else:
                await message.reply('Coudln\'t find that playlist!')
        else:
            await message.reply('Party leader permission needed!')
    
    elif args[0] == "!level" and len(args) == 2:
        try:
            level = int(args[1])
        except:
            await message.reply('The level must be a number!')
            level = 893

        try:
            await client.user.party.me.set_banner(season_level=level)
        except:
            await message.reply('Sorry, something wen\'t wrong!')
    
    elif content == "!hide all" and access.owner:
        if not client.user.party.me.leader:
            await message.reply('Party leader permission needed!')
        else:
            party_member = await client.fetch_profile(content[6:])
            if not party_member:
                await message.reply('Couldn\'t find a user with this ID')
            else:
                part = client.user.party.meta.set_prop('RawSquadAssignments_j', {'RawSquadAssignments': [{"memberId": client.user.id,"absoluteMemberIdx": 0}]})
                await client.user.party.patch(updated={'RawSquadAssignments_j': part})

    elif content == "!show all" and access.owner:
        if not client.user.party.me.leader:
            await message.reply('Party leader permission needed!')
        else:
            party_member = await client.fetch_profile(content[6:])
            if not party_member:
                await message.reply('Couldn\'t find a user with this ID')
            else:
                assignments = []

                i = 0
                for member in client.user.party.members.values():
                    if member.leader:
                        assignments.append({'memberId': member.id,'absoluteMemberIdx': 0})
                    else:
                        i += 1
                        assignments.append({'memberId': member.id,'absoluteMemberIdx': i})

                await client.user.party.patch(updated={'RawSquadAssignments_j': client.user.party.meta.set_prop('RawSquadAssignments_j', {'RawSquadAssignments': assignments})})

    elif args[0] == "!show" and len(args) > 1 and access.owner:
        if not client.user.party.me.leader:
            await message.reply('Party leader permission needed!')
        else:
            party_member = await client.fetch_profile(content[6:])
            if not party_member:
                await message.reply('Couldn\'t find a user with this ID')
            else:
                assignments = client.user.party.meta.get_prop('RawSquadAssignments_j')["RawSquadAssignments"]
                assignments.append({'memberId': party_member.id,'absoluteMemberIdx': len(assignments) + 1})

                await client.user.party.patch(updated={'RawSquadAssignments_j': client.user.party.meta.set_prop('RawSquadAssignments_j', {'RawSquadAssignments': assignments})})
                await message.reply("")

    elif args[0] == "!hide" and len(args) > 1 and access.owner:
        if not client.user.party.me.leader:
            await message.reply('Party leader permission needed!')
        else:
            party_member = await client.fetch_profile(content[6:])
            if not party_member:
                await message.reply('Couldn\'t find a user with this ID')
            else:
                assignments = client.user.party.meta.get_prop('RawSquadAssignments_j')["RawSquadAssignments"]
                for x in assignments:
                    if x["memberId"] == party_member.id:
                        assignments.remove(x)

                await client.user.party.patch(updated={'RawSquadAssignments_j': client.user.party.meta.set_prop('RawSquadAssignments_j', {'RawSquadAssignments': assignments})})

    await message.reply(fn_client.settings['Open EZFN Settings']['onMessage'])

def GetName(Name,Message):
    if Message.count("--") != 0:
        Item = GetValue(Message,f'{Name} ',"--")
    else:
        Item = Message[(len(Name) + 1):]

    return Item.strip()

def create_variant(VariantChannelName,Variant,item="AthenaCharacter"):
    return {'item': item,'channel': VariantChannelName,'variant': Variant}

def GetValue(fullLine,startWith,endWith):
    startIndex = fullLine.index(startWith) + len(startWith)
    endIndex = fullLine[startIndex:].index(endWith) + startIndex
    return fullLine[startIndex:endIndex]

def GetValues(fullLine):
    Variants = []
    for Variant in range(0,fullLine.count("--")):
        try:
            startIndex = fullLine.index("--")
            ValueStartIndex = fullLine[startIndex:].index("=") + startIndex + 1
        
            try:
                endIndex = fullLine[ValueStartIndex:].index("--") + ValueStartIndex
            except:
                endIndex = len(fullLine)
            Variants.append(fullLine[startIndex:endIndex])
            fullLine = fullLine.replace(fullLine[startIndex:endIndex],"")
        except:
            return None
    return Variants