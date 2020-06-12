from glitch import *

import io
import os
import sys
import json
import sanic
import asyncio
import aiohttp
import aiofiles
import requests
import fortnitepy
import pkg_resources

from subprocess import call
from zipfile import ZipFile
from collections import namedtuple
from .utils import load_defaults, authorized, add_event_handlers, update_check

update_check() # Update the cosmetics,playlists

app = sanic.Sanic('')
loop = asyncio.get_event_loop()

fn_client.settings = json.loads(open("settings.json").read())
fn_client = fortnitepy.Client(status=fn_client.settings['Open EZFN Settings']['Status'],auth=fortnitepy.AdvancedAuth(prompt_exchange_code=False,delete_existing_device_auths=True))
fn_client._start = False
fn_client.exception = ""

loop.create_task(add_event_handlers(fn_client))
loop.create_task(app.create_server(return_asyncio_server=True)) # Start sanic
load_defaults(fn_client) # Load default party settings and other stuff

def _invalid_device_auth():
    settings = json.loads(open("settings.json").read())
    # Remove the not working account from the settings
    settings["account"]["deviceID"] = ""
    settings["account"]["accountID"] = ""
    settings["account"]["secret"] = ""
    open("settings.json","w+").write(json.dumps(settings,indent=2)) # Overwrite the file
    fn_client._start = False # So other accounts can be added
    print('Failed to login with the stored device')

if fn_client.settings["account"]["deviceID"] and fn_client.settings["account"]["accountID"] and fn_client.settings["account"]["secret"]:
    deviceAuth = requests.post('https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token',data={'grant_type': 'device_auth','device_id': fn_client.settings["account"]["deviceID"],'account_id': fn_client.settings["account"]["accountID"],'secret': fn_client.settings["account"]["secret"],'token_type': 'eg1'},headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}).json()

    if "errorCode" in deviceAuth:
        if deviceAuth["errorCode"] == "errors.com.epicgames.account.invalid_account_credentials":
            _invalid_device_auth()
        else:
            print(f'Unknown error, please report it {deviceAuth["errorCode"]}')
    else:
        print(f'DeviceAuth is working!\nUserName: {deviceAuth["displayName"]}')
        fn_client._start = True
        fn_client.auth = fortnitepy.DeviceAuth(device_id=fn_client.settings["account"]["deviceID"],account_id=fn_client.settings["account"]["accountID"],secret=fn_client.settings["account"]["secret"])
        fn_client.auth.initialize(fn_client)

        async def start():
            print('Starting the Bot now!')
            try:
                await fn_client.start()
            except fortnitepy.AuthException:
                print('Sorry something wen\'t wrong with your deviceAuth!')
                _invalid_device_auth()
        
        loop.create_task(start()) # Start the client
else:
    os.system("clear")
    print('Open EZFN by Deepsy\n\nObviously join the Lupus server:\nhttps://discord.gg/GPSPwh6')

# Just a simple response
@app.route('/')
async def home(request):
    return sanic.response.text('')

# Restart functions
@app.route('/api/v1/restart')
@authorized()
async def restart_script(request):
    sys.exit() #Close the script, glitch will auto restart

@app.route('/set_2_added_project')
async def successfully_added_project(request: sanic.request):
    glitch_settings = await (await aiofiles.open('.data/glitch_settings.json', mode='r')).read()
    glitch_settings["added_project"] = True
    glitch_settings["current_state"] = "done"
    await (await aiofiles.open('.data/glitch_settings.json', mode='w+')).write(json.dumps(glitch_settings)) #Overwrite the glitch settings
    sys.exit()

# Settings
@app.route('/api/v1/settings')
@authorized()
async def api_settings(request):
    return sanic.response.json(json.loads(open("settings.json").read()))

@app.route('/api/v1/settings/add_full_access')
@authorized()
async def add_full_access(request):
    if not "user_ids" in request.json(): return sanic.response.json({"error":"UserIDs payload is missing."})
    user_ids = request.json()["user_ids"]

    # Fetch the owners (UseID's because it's better)
    owners_id = [owner.id for owner in await fn_client.fetch_profiles(user_ids)]
    for owner_id in owners_id:
        if not owner_id in fn_client.settings["owners"]:
            fn_client.settings["owners"].append(owner_id) # Add the user id to the current proccess
    
    await (await aiofiles.open('settings.json', mode='w+')).write(json.dumps(fn_client.settings,indent=2)) # Add the UserID to the settings
    return sanic.response.json({"status": "done"})

# Bot
@app.route('/api/v1/bot')
@authorized()
async def api_info_bots(request):
    client = {"email":"","friends":len(fn_client.friends),"is_ready":fn_client.is_ready(),"displayName":"","user_id":"","party_members":0}
    
    if fn_client.user:
        if fn_client.user.email:
            client["email"] = fn_client.user.email
        if fn_client.user.display_name:
            client["displayName"] = fn_client.user.display_name
        if fn_client.user.id:
            client["user_id"] = fn_client.user.id
        if fn_client.user.party:
            client["party_members"] = fn_client.user.party.member_count
    
    return sanic.response.json(client)

@app.route('/api/v1/bot/leave_party')
@authorized()
async def api_leave_party(request):
    try:
        await fn_client.user.party.me.leave()
    except Exception as e:
        return sanic.response.json({"status":"failed","error":str(e)})
    finally:
        return sanic.response.json({"status":"done"})

    # Friends

@app.route('/api/v1/bot/friends')
@authorized()
async def api_info_raw_friends(request):
    return sanic.response.json([friend.id for friend in fn_client.friends.values()]) #Return the friends

@app.route('/api/v1/bot/friends/count')
@authorized()
async def api_info_friends(request):
    return sanic.response.json({"friends_count":len(fn_client.friends)}) #Return the friends

# Add Bots
@app.route('/api/v1/add_account/device_auth')
@authorized()
async def api_add_account(request):
    if not "deviceID" in request.json and not "accountID" in request.json and not "secret" in request.json:
        return sanic.response.json({"error":"Some or all parts of the device auths are missing!"})

    if fn_client._start:
        return sanic.response.json({"error":"The Client is already running!"})

    # Check if the device Auth is valid!
    async with aiohttp.ClientSession() as session:
        deviceAuth = await (await session.post('https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token',data={'grant_type': 'device_auth','device_id': request.json["deviceID"],'account_id': request.json["accountID"],'secret': request.json["secret"],'token_type': 'eg1'},headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="})).json() # Download the cosmetics
        if "errorCode" in deviceAuth:
            if deviceAuth["errorCode"] == "errors.com.epicgames.account.invalid_account_credentials":
                return sanic.response.json({"status":"failed","errorCode":"errors.com.epicgames.account.invalid_account_credentials","error":"Sorry the account credentials you are using are invalid"})
        else:
            print(f'Device Auth is working.\nUserName: {deviceAuth["displayName"]}')
            settings = json.loads(open("settings.json").read())
            settings["account"]["accountID"] = request.json["accountID"]
            settings["account"]["deviceID"] = request.json["deviceID"]
            settings["account"]["secret"] = request.json["secret"]
            open("settings.json","w+").write(json.dumps(settings,indent=2))

            fn_client._start = True
            fn_client.auth = fortnitepy.DeviceAuth(device_id=request.json["deviceID"],account_id=request.json["accountID"],secret=request.json["secret"])
            fn_client.auth.initialize(fn_client)

            def done_callback(error):
                exception = error.exception()
                fn_client.exception = str(exception)
                fn_client._start = False

            loop.create_task(fn_client.start()).add_done_callback(done_callback)

            while not fn_client.is_ready():
                if fn_client.exception:
                    return sanic.response.json({"status": "failed","error": fn_client.exception})
                await asyncio.sleep(0.1)

            if fn_client.is_ready():
                return sanic.response.json({"status": "success", "display_name":fn_client.user.display_name, "user_id":fn_client.user.id})

@app.middleware('response')
async def on_response(request, response: sanic.response):
    response.headers = {"Access-Control-Allow-Origin":"*"}
    return response

try:
    loop.run_forever()
finally:
    loop.stop()