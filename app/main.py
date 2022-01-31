from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strip import Strip, Config
from threading import Thread
from queue import Queue

origins = [
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

strip = Strip()
queue = Queue()
process = Thread(target=strip.start, args=(queue, ))
process.start()


@app.post('/api/config')
async def set(body: Config):
    queue.put(body)
    return 'OK'


@app.get('/api/config')
async def config():
    return strip.config
