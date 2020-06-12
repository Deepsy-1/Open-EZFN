import fortnitepy

async def event_friend_add(client: fortnitepy.Client, friend: fortnitepy.Friend):
    try:
        await friend.send(fn_client.settings['Open EZFN Settings']['onMessage'])
    except: pass

    if client.settings["Old_Stuff"]["invite_on_add"]:
    if True:
        try:
            await friend.invite()
        except: pass

async def event_friend_remove(client: fortnitepy.Client, friend: fortnitepy.Friend):
    if client.settings["Old_Stuff"]["add_on_remove"]:
    if True:
        try:
            await client.add_friend(friend.id)
        except:
            pass

async def event_friend_request(client: fortnitepy.Client, request: fortnitepy.PendingFriend):
    if client.settings["Old_Stuff"]["accept_request"]:
    if True:
        try:
            await request.accept()
        except:
            pass