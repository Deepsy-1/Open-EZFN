import json
import time
import fortnitepy
import aiofiles

banner_colors = {"Gray" : "DefaultColor1","Red" : "DefaultColor2","Orange" : "DefaultColor3","Orange Yellow" : "DefaultColor4","Yellow" : "DefaultColor5","Green" : "DefaultColor8","Green Blue" : "DefaultColor12","Blue" : "DefaultColor13","Purple" : "DefaultColor17","Purple Pink" : "DefaultColor19","Pink" : "DefaultColor20","Gray Dark" : "DefaultColor22","Gray Light" : "DefaultColor23","Red Dark" : "DefaultColor24","Red Light" : "DefaultColor25","Orange Light" : "DefaultColor26","Orange Yellow Dark" : "DefaultColor27","Orange Yellow Light" : "DefaultColor28","Yellow Dark" : "DefaultColor29","Green Dark" : "DefaultColor30","Green Light" : "DefaultColor31","Green Dark" : "DefaultColor32","Green Light" : "DefaultColor34","Green Blue Dark" : "DefaultColor36","Blue Dark" : "DefaultColor37","Blue Light" : "DefaultColor39","Purple Dark" : "DefaultColor40","Purple Light" : "DefaultColor41","Pink Dark" : "DefaultColor43","Pink Light": "DefaultColor44"}

def fetch_cosmetic(name, language, backend_type):
    start = time.time()

    # They should already be lowercase but just to make sure they are...
    name = name.lower()
    backend_type = backend_type.lower()
    language = language.lower()

    # Playlist
    if backend_type == "AthenaPlaylist":
        playlists = json.loads(open("data/playlists.json").read())
        for playlist in playlists:
            try:
                if playlist["names"][language].lower() == name:
                    # print(f'Loaded Playlist by file in {time.time() - start} seconds')
                    return playlist
            except:
                pass

        for playlist in playlists:
            try:
                if playlist["names"][language].lower().startswith(name):
                    # print(f'Loaded Playlist by file in {time.time() - start} seconds')
                    return playlist
            except:
                pass

    # Banner 
    elif backend_type == "AthenaBanner":
        banners = json.loads(open("data/banners.json").read())
        for banner in banners:
            try:
                if banner["name"].lower() == name:
                    # print(f'Loaded Banner by file in {time.time() - start} seconds')
                    return banner
            except:
                pass
        
        for banner in banners:
            try:
                if banner["name"].lower().startswith(name):
                    # print(f'Loaded Banner by file in {time.time() - start} seconds')
                    return banner
            except:
                pass
    else:
        # If not found in the cache search in the file
        cosmetics = json.loads(open("data/cosmetics.json").read())
        
        for cosmetic in cosmetics:
            try:
                if cosmetic["names"][language].lower() == name and backend_type == cosmetic["backendType"].lower():
                    # print(f'Loaded Item by file in {time.time() - start} seconds')
                    return cosmetic
            except:
                pass

        for cosmetic in cosmetics:
            try:
                if cosmetic["names"][language].lower().startswith(name) and backend_type == cosmetic["backendType"].lower():
                    # print(f'Loaded Item by file in {time.time() - start} seconds')
                    return cosmetic
            except:
                pass

    return None # No item found

async def _fetch_cosmetic(name, language, backend_type, client: fortnitepy.Client):
    start = time.time()

    # They should already be lowercase but just to make sure they are...
    name = name.lower()
    backend_type = backend_type.lower()
    language = language.lower()

    # Playlist
    if backend_type == "athenaplaylist":
        playlists = json.loads(await (await aiofiles.open('data/playlists.json', mode='r')).read())
        for playlist in playlists:
            try:
                if playlist["names"][language].lower() == name:
                    # print(f'Loaded Playlist by file in {time.time() - start} seconds')
                    return playlist
            except:
                pass

        for playlist in playlists:
            try:
                if playlist["names"][language].lower().startswith(name):
                    # print(f'Loaded Playlist by file in {time.time() - start} seconds')
                    return playlist
            except:
                pass

    # Banner 
    elif backend_type == "athenabanner":
        banners = json.loads(await (await aiofiles.open('data/banners.json', mode='r')).read())
        for banner in banners:
            try:
                if banner["name"].lower() == name:
                    # print(f'Loaded Banner by file in {time.time() - start} seconds')
                    return banner
            except:
                pass
        
        for banner in banners:
            try:
                if banner["name"].lower().startswith(name):
                    # print(f'Loaded Banner by file in {time.time() - start} seconds')
                    return banner
            except:
                pass
    else:
        # If not found in the cache search in the file
        cosmetics = json.loads(await (await aiofiles.open('data/cosmetics.json', mode='r')).read())
        
        for cosmetic in cosmetics:
            try:
                if cosmetic["names"][language].lower() == name and backend_type == cosmetic["backendType"].lower():
                    # print(f'Loaded Item by file in {time.time() - start} seconds')
                    return cosmetic
            except:
                pass

        for cosmetic in cosmetics:
            try:
                if cosmetic["names"][language].lower().startswith(name) and backend_type == cosmetic["backendType"].lower():
                    # print(f'Loaded Item by file in {time.time() - start} seconds')
                    return cosmetic
            except:
                pass

    return None # No item found

async def get_skin(name_or_id, client, language="en",): return await _fetch_cosmetic(name_or_id, language, "AthenaCharacter", client)
async def get_backpack(name_or_id, client, language="en",): return await _fetch_cosmetic(name_or_id, language, "AthenaBackpack", client)
async def get_pickaxe(name_or_id, client, language="en",): return await _fetch_cosmetic(name_or_id, language, "AthenaPickaxe", client)
async def get_emote(name_or_id, client, language="en",): return await _fetch_cosmetic(name_or_id, language, "AthenaDance", client)
async def get_emoji(name_or_id, client, language="en",): return await _fetch_cosmetic(name_or_id, language, "AthenaEmoji", client)
async def get_pet(name_or_id, client, language="en",): return await _fetch_cosmetic(name_or_id, language, "AthenaPetCarrier", client)
async def get_banner(name_or_id, client, language="en",): return await _fetch_cosmetic(name_or_id, language, "AthenaBanner", client)
async def get_playlist(name_or_id, client, language="en",): return await _fetch_cosmetic(name_or_id, language, "AthenaPlaylist" , client)