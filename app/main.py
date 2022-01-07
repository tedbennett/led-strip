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
    colors: list[str]


class LoopRequest(BaseModel):
    colors: list[str]
    delay: int


@app.get("/")
async def root():
    return 'Welcome to pi!'


@app.post('/color')
async def color(body: ColorRequest):
    strip.set_color(body.color)
    return 'OK'


@app.post('/colors')
async def colors(body: ColorsRequest):
    strip.set_colors(body.colors)
    return 'OK'


@app.post('/loop')
async def loop(body: LoopRequest):
    strip.set_color_loop(body.colors, body.delay)
    return 'OK'
