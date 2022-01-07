from fastapi import FastAPI
from pydantic import BaseModel
from strip import Strip
import threading

app = FastAPI()
strip = Strip()
process = threading.Thread(target=strip.start, args=())
process.start()


class ColorRequest(BaseModel):
    color: str


class ColorsRequest(BaseModel):
    colors: str


class LoopRequest(BaseModel):
    colors: str
    delay: int


@app.get("/")
async def root():
    return 'Welcome to pi!'


@app.post('/color')
async def color(body: ColorRequest):
    strip.set_color(body.color)
    return 'received data'


@app.post('/colors')
async def colors(body: ColorsRequest):
    strip.set_colors(body.colors)
    return 'received data'


@app.post('/loop')
async def loop(body: LoopRequest):
    strip.set_color_loop(body.colors, body.delay)
    return 'received data'
