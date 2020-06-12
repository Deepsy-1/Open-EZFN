import fortnitepy
import asyncio
import time

async def accept_inbound(client: fortnitepy.Client):
    started = time.time()
    accepted = 0
    accept = [friend.id for friend in client.pending_friends.values() if friend.inbound]
    for friend in accept:
        try:
            await client.add_friend(friend)
            accepted += 1
        finally:
            await asyncio.sleep(0.5)
    
    print(f'Accepted {accepted}/{len(accept)} Inbound Friend Request in {int(time.time() - started)} seconds :)')

async def event_ready(client: fortnitepy.Client):
    print(f'{client.user.display_name} is now ready!')

    # Accept all inbound friend requests
    client.loop.create_task(accept_inbound(client))

    # Fetch the owners (UseID's because it's better)
    owners_id = [owner.id for owner in await client.fetch_profiles(client.settings["owners"])]
    print(f'Fetched {len(owners_id)}/{len(client.settings["owners"])} owners')
    client.settings["owners"] = owners_id

    def refresh_squad_assignments():
        part = client.user.party.meta.set_prop('RawSquadAssignments_j', {'RawSquadAssignments': client.user.party.meta.get_prop('RawSquadAssignments_j')["RawSquadAssignments"]})
        return part

    client.user.party.meta.refresh_squad_assignments = refresh_squad_assignments

    part = client.user.party.meta.set_prop('RawSquadAssignments_j', {'RawSquadAssignments': [{"memberId": client.user.id,"absoluteMemberIdx": 0}]})
    await client.user.party.patch(updated={'RawSquadAssignments_j': part})

async def event_logout(client: fortnitepy.Client):
    print('Client logged out, logging in again.')
    await client.start()

async def event_auth_refresh(client: fortnitepy.Client):
    pass