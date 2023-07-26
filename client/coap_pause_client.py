import logging
import asyncio
import aiocoap
from aiocoap import *

logging.basicConfig(level=logging.INFO)


async def main():
    protocol = await Context.create_client_context()

    # Modifica del funzionamento del robot o cambio robot da utilizzare
    resource = "operating_mode"  # Risorsa da modificare
    new_value = "pause"  # Nuovo valore

    request = Message(code=aiocoap.PUT, uri=f'coap://127.0.0.1:5693/{resource}', payload=new_value.encode("utf-8"))
    try:
        response = await protocol.request(request).response
        if response.code.is_successful():
            print(f"{resource} updated with value: {new_value}")
        else:
            print(f"Failed to update {resource}.")
    except Exception as e:
        print(f'Failed to update {resource}:')
        print(e)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())