import asyncio
import json
import time
import websockets

from tracking import HandTracker
from gestures import GestureDetector

CONNECTED_CLIENTS = set()

async def register(websocket):
    CONNECTED_CLIENTS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTED_CLIENTS.remove(websocket)

async def broadcast(cmd_type, **kwargs):
    if not CONNECTED_CLIENTS:
        return
    message = json.dumps({"type": cmd_type, **kwargs})
    await asyncio.gather(
        *[client.send(message) for client in CONNECTED_CLIENTS],
        return_exceptions=True
    )

async def gesture_loop():
    tracker = HandTracker()
    detector = GestureDetector()
    start_time = time.time()

    try:
        while True:
            timestamp_ms = int((time.time() - start_time) * 1000)
            frame, landmarks = tracker.get_frame_landmarks(timestamp_ms)

            if landmarks:
                events = detector.process_frame(landmarks)
                for event, payload in events:
                    if event == 'SWIPE_RIGHT':
                        await broadcast('gesture', name='Swipe Right')
                        await broadcast('select', dir='next')
                    elif event == 'SWIPE_LEFT':
                        await broadcast('gesture', name='Swipe Left')
                        await broadcast('select', dir='prev')
                    elif event == 'PINCH_START':
                        await broadcast('gesture', name='Pinch Up')
                        await broadcast('slider', delta=0.05)

            await asyncio.sleep(0.03)  # Loop at ~30 FPS
            # Inside your gesture_loop / websocket send block:
    if landmarks:
        print(f"Tracking -> Wrist: {landmarks['wrist']}, Pinch distance: {abs(landmarks['thumb'][0] - landmarks['index'][0]):.2f}")
        await websocket.send(json.dumps(landmarks))
    finally:
        tracker.release()

async def main():
    async with websockets.serve(register, "localhost", 8765):
        print("Gesture Server Running on ws://localhost:8765")
        await gesture_loop()

if __name__ == "__main__":
    asyncio.run(main())