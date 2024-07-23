import asyncio
import json
import websockets

async def send_json_data(websocket, path):
    while True:
        try:
            with open('/tmp/robot_state.json', 'r') as f:
                data = json.load(f)
                await websocket.send(json.dumps(data))
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Error reading or sending JSON data: {e}")

            
async def main():
    async with websockets.serve(send_json_data, "localhost", 6789):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
