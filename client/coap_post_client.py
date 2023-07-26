import logging
import asyncio
import aiocoap
from aiocoap import *

logging.basicConfig(level=logging.INFO)


async def main():
    protocol = await Context.create_client_context()

    # Avvio del robot con la modalità di default start
    request = Message(code=aiocoap.POST, uri='coap://127.0.0.1:5693/operating_mode')
    try:
        response = await protocol.request(request).response
        if response.code.is_successful():
            print(f"Robot Started ")
        else:
            print("Failed to start the robot.")
    except Exception as e:
        print('Failed to send start command:')
        print(e)

    # Avvio del robot con la switch video di default on
    request = Message(code=aiocoap.POST, uri='coap://127.0.0.1:5693/video_switch')
    try:
        response = await protocol.request(request).response
        if response.code.is_successful():
            print(f"Video Switch ON")
        else:
            print("Failed to start the robot.")
    except Exception as e:
        print('Failed to send start command:')
        print(e)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
