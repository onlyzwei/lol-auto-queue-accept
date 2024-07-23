from asyncio import sleep
from lcu_driver import Connector

connector = Connector()


@connector.ready
async def connect(connection):
    print('LCU API is ready to be used.')


@connector.close
async def disconnect(_):
    print('The client has been closed!')
    await connector.stop()


@connector.ws.register('/lol-gameflow/v1/session', event_types=('UPDATE',))
async def phase_changed(connection, event):
    phase = event.data["phase"]
    if phase == "ReadyCheck":
        await sleep(5)
        request = await connection.request('post', '/lol-matchmaking/v1/ready-check/accept')

connector.start()
