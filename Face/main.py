import webbrowser
import asyncio
from reaction import get_random_expression

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import time
import uvicorn
import threading

app = FastAPI()


def start_voice_processor():
    from audio import VoiceProcessor
    vp = VoiceProcessor()
    vp.listen()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    voice_thread = threading.Thread(target=start_voice_processor)
    voice_thread.start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
