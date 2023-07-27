import logging
import asyncio
import aiocoap
from aiocoap import *

logging.basicConfig(level=logging.INFO)
logging.getLogger('coap').setLevel(logging.ERROR)


async def main():
    protocol = await Context.create_client_context()

    # Lettura delle risorse osservabili del robot
    resources = ['battery_level']
    for resource in resources:
        request = Message(code=aiocoap.GET, uri=f'coap://127.0.0.1:5699/{resource}', observe=0, mid=None)
        try:
            observation_is_active = True
            while observation_is_active:
                response = await protocol.request(request).response
                print(f"{resource}: {response.payload.decode('utf-8')}")

                if response.code.is_successful():
                    # Continua ad osservare la risorsa fino a quando si interrompe manualmente
                    await asyncio.sleep(1)
                else:
                    observation_is_active = False

        except Exception as e:
            print(f'Failed to observe resource {resource}:')
            print(e)

if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(main())
    asyncio.run(main())
