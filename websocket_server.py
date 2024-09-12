import asyncio
import json
import websockets

# Function to send JSON data to the websocket client
async def send_json_data(websocket, path):
    while True:
        try:
            # Read the robot state from the JSON file
            with open('robot_state.json', 'r') as f:
                data = json.load(f)
                # Send the JSON data to the client
                await websocket.send(json.dumps(data))
            # Wait for 0.5 seconds before sending the next update
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Error reading or sending JSON data: {e}")

# Main function to start the websocket server            
async def main():
    async with websockets.serve(send_json_data, "localhost", 6789):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
