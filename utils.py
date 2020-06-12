import time
import json
import sanic
import aiofiles
import requests
import fortnitepy

from get_cosmetic import *
from events.ready import *
from events.friends import *
from events.party import *
from events.message import event_message
from functools import partial,wraps

# Basically useless but I also don't want to make it to easy #And change this sucks...
SecretKey = 'Lupus_12$sEcReTKeYDoNoTlEaKThIs$12_Leaks_securit_sucks_because_its_open_source'

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator

async def add_event_handlers(client: fortnitepy.Client):
    # Start, Logout, Auth Refresh
    async def _ready(): await event_ready(client)
    client.add_event_handler("ready", _ready)

    async def _logout(): await event_logout(client)
    client.add_event_handler("logout", _logout)

    async def _auth_refresh(): await event_auth_refresh(client)
    client.add_event_handler("auth_refresh", _auth_refresh)

    # Device Auth

    async def _device_auth_generate(details, email): pass # await event_device_auth_generate(client, email, details)
    client.add_event_handler("device_auth_generate", _device_auth_generate)

    # Message

    async def _friend_message(message): await event_message(client, message)
    client.add_event_handler('friend_message', _friend_message)

    async def _party_message(message): await event_message(client, message)
    client.add_event_handler('party_message', _party_message)

    # Friends

    async def _friend_add(friend): await event_friend_add(client, friend)
    client.add_event_handler('friend_add', _friend_add)

    async def _friend_remove(friend): await event_friend_remove(client, friend)
    client.add_event_handler('friend_remove', _friend_remove)

    async def _friend_request(request): await event_friend_request(client, request)
    client.add_event_handler('friend_request', _friend_request)

    # Party

        # Accept /Decline Party invitation
    async def _party_invite(invitation): await event_party_invite(client, invitation)
    client.add_event_handler('party_invite', _party_invite)

        # Send a message if someone promotes
    async def _party_member_promote(old_leader, new_leader): await event_party_member_promote(client, old_leader, new_leader)
    client.add_event_handler('party_member_promote', _party_member_promote)

        # Send a welcome message
    async def _party_member_join(member): await event_party_member_join(client, member)
    client.add_event_handler('party_member_join', _party_member_join)

    async def _party_member_leave(member): await event_party_member_leave(client, member)
    client.add_event_handler('party_member_leave', _party_member_leave)

    #     # Check if an user is banned and accept/decline
    # async def _party_member_confirm(member): await event_party_member_confirm(client, member)
    # client.add_event_handler('party_member_confirm', _party_member_confirm)

def cosmetic_is_id(name_or_id, backendType):
    name_or_id = name_or_id.lower()
    backendType = backendType.lower()

    if backendType == "athenacharacter": 
        if name_or_id.startswith("cid_"):
            return True
        else:
            return False

    if backendType == "athenabackpack":  
        if name_or_id.startswith("bid_"):
            return True
        else:
            return False

    if backendType == "athenapickaxe":
        if name_or_id.startswith("pickaxe_id_"):
            return True
        else:
            return False

    if backendType == "athenadance":
        if name_or_id.startswith("eid_"):
            return True
        else:
            return False

    if backendType == "athenaemoji":
        if name_or_id.startswith("emoji_"):
            return True
        else:
            return False

    if backendType == "athenapetcarrier":
        if name_or_id.startswith("petcarrier_"):
            return True
        else:
            return False

def load_defaults(client: fortnitepy.Client):
    settings = client.settings
    emoji_and_emote = False
    backpack_and_pet = False
    party_member = []
    party = {}

    party_member.append(partial(fortnitepy.ClientPartyMember.set_banner,season_level=893,color="DefaultColor43",icon="OtherBanner28"))

    # platform
    if not settings["platform"].upper() in fortnitepy.Platform.__members__:
        client.platform = fortnitepy.Platform.WINDOWS
        print(f'No such a Platform "{settings["platform"]}", switched to Windows')
    else:
        client.platform = fortnitepy.Platform[settings["platform"].upper()]
    
    # cosmetics
        # Skin
    if settings["cosmetics"]["skin"]:
        variants = settings["cosmetics_variants"]["skin"] if(type(settings["cosmetics_variants"]["skin"]) == list and len(settings["cosmetics_variants"]["skin"]) > 0) else []
        if cosmetic_is_id(settings["cosmetics"]["skin"], "AthenaCharacter"):
            party_member.append(partial(fortnitepy.ClientPartyMember.set_outfit,asset=settings["cosmetics"]["skin"],variants=variants))
            print(f'Set default CharacterID to {settings["cosmetics"]["skin"]}.')
        else:
            skin = fetch_cosmetic(settings["cosmetics"]["skin"], "en", "AthenaCharacter")
            if skin:
                party_member.append(partial(fortnitepy.ClientPartyMember.set_outfit,asset=f'{skin["path"]}.{skin["id"]}',variants=variants))
                print(f'Set default Character to {skin["names"]["en"]}.')
            else:
                print(f'Could not find the skin {settings["cosmetics"]["skin"]}.')

        # Pickaxe
    if settings["cosmetics"]["pickaxe"]:
        variants = settings["cosmetics_variants"]["pickaxe"] if(type(settings["cosmetics_variants"]["pickaxe"]) == list and len(settings["cosmetics_variants"]["pickaxe"]) > 0) else []
        if cosmetic_is_id(settings["cosmetics"]["pickaxe"], "AthenaPetCarrier"):
            party_member.append(partial(fortnitepy.ClientPartyMember.set_outfit,asset=settings["cosmetics"]["pickaxe"],variants=variants))
            print(f'Set default Pickaxe ID to {settings["cosmetics"]["pickaxe"]}.')
        else:
            pickaxe = fetch_cosmetic(settings["cosmetics"]["pickaxe"], "en", "AthenaPetCarrier")
            if pickaxe:
                party_member.append(partial(fortnitepy.ClientPartyMember.set_outfit,asset=f'{pickaxe["path"]}.{pickaxe["id"]}',variants=variants))
                print(f'Set default Pickaxe to {pickaxe["name"]}.')
            else:
                print(f'Could not find the pickaxe {settings["cosmetics"]["pickaxe"]}.')


        # Just so we need to check it once only, (set it to id automatically)
    if settings["cosmetics"]["backpack"] and settings["cosmetics"]["pet"]:
        print('You can\'t set Backpack and Pet, please check your settings file.')
        backpack_and_pet = True

        # Backpack
    if settings["cosmetics"]["backpack"]:
        variants = settings["cosmetics_variants"]["backpack"] if(type(settings["cosmetics_variants"]["backpack"]) == list and len(settings["cosmetics_variants"]["backpack"]) > 0) else []
        if cosmetic_is_id(settings["cosmetics"]["backpack"], "AthenaBackpack"):
            party_member.append(partial(fortnitepy.ClientPartyMember.set_backpack,asset=settings["cosmetics"]["backpack"],variants=variants))
            print(f'Set default BackpackID to {settings["cosmetics"]["backpack"]}.')
            if backpack_and_pet:
                print('Automatically removed Pet to be executed when joining a Party')
                client.settings["cosmetics"]["pet"] = ""
        else:
            backpack = fetch_cosmetic(settings["cosmetics"]["backpack"], "en", "AthenaBackpack")
            if backpack:
                party_member.append(partial(fortnitepy.ClientPartyMember.set_backpack,asset=f'{backpack["path"]}.{backpack["id"]}',variants=variants))
                print(f'Set default Backpack to {backpack["name"]}.')
                if backpack_and_pet:
                    print('Automatically removed Pet to be executed when joining a Party')
                    client.settings["cosmetics"]["pet"] = ""
            else:
                print(f'Could not find the backpack {settings["cosmetics"]["backpack"]}.')

        # Pet
    if settings["cosmetics"]["pet"]:
        variants = settings["cosmetics_variants"]["pet"] if(type(settings["cosmetics_variants"]["pet"]) == list and len(settings["cosmetics_variants"]["pet"]) > 0) else []
        if cosmetic_is_id(settings["cosmetics"]["pet"], "AthenaPetCarrier"):
            party_member.append(partial(fortnitepy.ClientPartyMember.set_pet,asset=settings["cosmetics"]["pet"],variants=variants))
            print(f'Set default petID to {settings["cosmetics"]["pet"]}.')
        else:
            pet = fetch_cosmetic(settings["cosmetics"]["pet"], "en", "AthenaPetCarrier")
            if pet:
                party_member.append(partial(fortnitepy.ClientPartyMember.set_pet,asset=f'{pet["path"]}.{pet["id"]}',variants=variants))
                print(f'Set default pet to {pet["name"]}.')
            else:
                print(f'Could not find the pet {settings["cosmetics"]["pet"]}.')
        
        # Just so we need to check it once only, (set it to id automatically)
    if settings["cosmetics"]["emote"] and settings["cosmetics"]["emoji"]:
        print('You can\'t set Emoji and Emote, please check your settings file.')
        emoji_and_emote = True

    if settings["cosmetics"]["emote"]:
        if cosmetic_is_id(settings["cosmetics"]["emote"], "AthenaDance"):
            print(f'Set default Emote to {settings["cosmetics"]["emote"]}')
            if emoji_and_emote:
                print('Automatically removed Emoji to be executed when joining a Party')
                client.settings["cosmetics"]["emoji"] = ""
        else:
            emote = fetch_cosmetic(settings["cosmetics"]["emote"], "en", "AthenaDance")
            if emote:
                client.settings["cosmetics"]["emote"] = f'{emote["path"]}.{emote["id"]}'
                if emoji_and_emote:
                    print('Automatically removed Emoji to be executed when joining a Party')
                    client.settings["cosmetics"]["emoji"] = ""
            else:
                print(f'Could not find the emote {settings["cosmetics"]["emote"]}.')
                client.settings["cosmetics"]["emote"] = "" # "Remove" it so auto set emote works

    if settings["cosmetics"]["emoji"]:
        if cosmetic_is_id(settings["cosmetics"]["emoji"], "AthenaEmoji"):
            print(f'Set default Emoji to {settings["cosmetics"]["emoji"]}')
        else:
            emoji = fetch_cosmetic(settings["cosmetics"]["emoji"], "en", "AthenaEmoji")
            if emoji:
                client.settings["cosmetics"]["emoji"] = f'{emoji["path"]}.{emoji["id"]}'
            else:
                print(f'Could not find the emoji {settings["cosmetics"]["emoji"]}.')

    client.default_party_config = party
    client.default_party_member_config = party_member

def update_check():
    new_status = requests.get("https://api.ezfn.net/lobbybot/status").json()
    
    if new_status["cosmetic_count"] != len(json.loads(open("data/cosmetics.json").read())):
        cosmetics = requests.get(new_status["cosmetics.json"]).json()
        open("data/cosmetics.json","w+").write(json.dumps(cosmetics))
    
    if new_status["playlist_count"] != len(json.loads(open("data/playlists.json").read())):
        playlists = requests.get(new_status["playlists.json"]).json()
        open("data/playlists.json","w+").write(json.dumps(playlists))