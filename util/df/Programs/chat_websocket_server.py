#!/usr/bin/env python3
import asyncio
import websockets

clients = set()

async def echo(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast to all clients
            for client in clients:
                await client.send(f"{message}")
    finally:
        clients.remove(websocket)

start_server = websockets.serve(echo, "localhost", 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
