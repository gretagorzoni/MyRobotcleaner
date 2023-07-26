import logging
import asyncio
import aiocoap
from aiocoap import *

logging.basicConfig(level=logging.INFO)


async def main():
    protocol = await Context.create_client_context()

    # Lettura delle risorse del robot
    resources = ['battery_level', 'position', 'operating_mode', 'video_switch']

    for resource in resources:
        request = Message(code=aiocoap.GET, uri=f'coap://127.0.0.1:5693/{resource}')
        try:
            response = await protocol.request(request).response
            print(f"{resource}: {response.payload.decode('utf-8')}")
        except Exception as e:
            print(f'Failed to fetch resource {resource}:')
            print(e)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
