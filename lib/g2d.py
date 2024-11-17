#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

from tkinter import Tk, messagebox, simpledialog
from urllib.request import urlopen
import io, math, subprocess, sys
try:
    import pygame as pg
    import os 
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "pygame",
                     "--break-system-packages"])
    import pygame as pg
    
    # no need to install libraries because os is a standard lib

Point = tuple[float, float]
Color = tuple[float, float, float]

_tkmain = Tk()
_tkmain.withdraw()  # hide the main window
_ws, _hs = _tkmain.winfo_screenwidth(), _tkmain.winfo_screenheight()
_tkmain.geometry(f"+{_ws // 2}+{_hs // 2}")

_canvas, _display, _tick = None, None, None
_size, _color = (640, 480), (127, 127, 127)
_mouse_pos, _mouse_down = (0, 0), 0
_curr_keys, _prev_keys = set(), set()
_loaded = {}
loaded_fonts = []

def _tup(t: tuple, vmin=-math.inf, vmax=math.inf) -> tuple:
    return tuple(min(max(round(v), vmin), vmax) for v in t)

def init_canvas(size: Point, scale=1):
    """Set size of first CANVAS and return it"""
    global _canvas, _display, _draw, _size
    pg.init()
    _size = _tup(size)
    w, h = _size
    _display = pg.display.set_mode((w * scale, h * scale))
    _canvas = pg.Surface(_size, pg.SRCALPHA) if scale != 1 else _display
    _draw = pg.Surface(_size, pg.SRCALPHA)
    clear_canvas()

def canvas_size() -> Point:
    return _size

def set_color(color: Color) -> None:
    global _color
    _color = _tup((list(color) + [255])[:4], 0, 255)

def clear_canvas() -> None:
    _canvas.fill((255, 255, 255))

def update_canvas() -> None:
    global _prev_keys
    _prev_keys = set(_curr_keys)
    if _canvas is not _display:
        scaled = pg.transform.scale(_canvas, _display.get_size())
        _display.blit(scaled, (0, 0))
    pg.display.update()
    pg.time.wait(0)

def drawing_surface() -> pg.Surface:
    if len(_color) > 3 and _color[3] != 255:
        _draw.fill((0, 0, 0, 0))
        return _draw
    return _canvas

def blit_drawing_surface():
    if len(_color) > 3 and _color[3] != 255:
        _canvas.blit(_draw, (0, 0))

def draw_line(pt1: Point, pt2: Point, width: float=1) -> None:
    surf = drawing_surface()
    pg.draw.line(surf, _color, _tup(pt1), _tup(pt2), int(width))
    blit_drawing_surface()

def draw_circle(center: Point, radius: float) -> None:
    surf = drawing_surface()
    pg.draw.circle(surf, _color, _tup(center), int(radius))
    blit_drawing_surface()

def draw_rect(pos: Point, size: Point) -> None:
    surf = drawing_surface()
    rect = pg.Rect(*_tup(pos + size))
    rect.normalize()
    pg.draw.rect(surf, _color, rect)
    blit_drawing_surface()

def draw_text(txt: str, pos: Point, size: int, fname: str, align: str) -> None:
    fonts = pg.font.get_fonts()
    
    fonts_folder = "./fonts"
    loaded_fonts = load_fonts_from_folder(fonts_folder)
    
    if loaded_fonts != False and fname in loaded_fonts:
        font = pg.font.Font(("./lib/fonts/" + fname), int(size))
    elif fname in fonts:
        font = pg.font.SysFont(fname, int(size))
    else:
        font = pg.font.SysFont("freesansbold", int(size))
        
    surface = font.render(txt, True, _color)
    if len(_color) > 3 and _color[3] != 255:
        surface.set_alpha(_color[3])
    (x, y), (w, h) = _tup(pos), surface.get_size()
    if align == "center":
        x = x - w//2
    if align == "end":  
        x = x - w
    _canvas.blit(surface, (x, y))

def draw_polygon(points: list[Point]) -> None:
    surf = drawing_surface()
    pg.draw.polygon(surf, _color, [_tup(p) for p in points])
    blit_drawing_surface()

def load_image(src: str) -> str:
    gh = "https://fondinfo.github.io/sprites/"
    if src not in _loaded:
        try:
            _loaded[src] = pg.image.load(src)
        except:
            url = src if src.startswith("http") else gh + src
            image = io.BytesIO(urlopen(url).read())
            _loaded[src] = pg.image.load(image)
    return src

def draw_image(src: str, pos: Point,
               clip_pos: Point=None, clip_size: Point=None) -> None:
    area = None
    if clip_pos and clip_size:
        area=_tup(clip_pos) + _tup(clip_size)
    _canvas.blit(_loaded[load_image(src)], _tup(pos), area=area)

def load_audio(src: str) -> str:
    if src not in _loaded:
        try:
            _loaded[src] = pg.mixer.Sound(src)
        except:
            audio = io.BytesIO(urlopen(src).read())
            _loaded[src] = pg.mixer.Sound(audio)
    return src

def play_audio(src: str, loop=False) -> None:
    _loaded[load_audio(src)].play(-1 if loop else 0)

def pause_audio(src: str) -> None:
    _loaded[load_audio(src)].stop()

def alert(message: str) -> None:
    if _canvas:
        update_canvas()
    messagebox.showinfo("", message)

def confirm(message: str) -> bool:
    if _canvas:
        update_canvas()
    return messagebox.askokcancel("", message)

def prompt(message: str) -> str:
    if _canvas:
        update_canvas()
    return simpledialog.askstring("", message) or ""

def mouse_pos() -> Point:
    return _mouse_pos

def _mb_name(key: int) -> str:
    return ["LeftButton", "MiddleButton", "RightButton"][min(key - 1, 2)]

def _kb_name(key: int) -> str:
    fixes = {"up" : "ArrowUp", "down" : "ArrowDown",
             "right" : "ArrowRight", "left" : "ArrowLeft",
             "space": "Spacebar", "return": "Enter"}
    name = pg.key.name(key)
    if name in fixes:
        name = fixes[name]
    elif len(name) > 1:
        name = "".join(w.capitalize() for w in name.split())
    return name

def current_keys() -> list[str]:
    return list(_curr_keys)

def previous_keys() -> list[str]:
    return list(_prev_keys)

def mouse_clicked() -> bool:
    return key_released("LeftButton")

def mouse_right_clicked() -> bool:
    return key_released("RightButton")

def key_pressed(key: str) -> bool:
    return key in _curr_keys and key not in _prev_keys

def key_released(key: str) -> bool:
    return key in _prev_keys and key not in _curr_keys

def main_loop(tick=None, fps: int=30) -> None:
    global _mouse_pos, _tick
    _tick = tick
    clock = pg.time.Clock()
    update_canvas()
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                break
            elif e.type == pg.KEYDOWN:
                _curr_keys.add(_kb_name(e.key))
            elif e.type == pg.KEYUP:
                _curr_keys.discard(_kb_name(e.key))
            elif e.type == pg.MOUSEBUTTONDOWN:
                _curr_keys.add(_mb_name(e.button))
            elif e.type == pg.MOUSEBUTTONUP:
                _curr_keys.discard(_mb_name(e.button))
        if _tick:
            _mouse_pos = pg.mouse.get_pos()
            _tick()
            update_canvas()
        clock.tick(fps)
    close_canvas()

def close_canvas() -> None:
    pg.quit()
    sys.exit()

def load_fonts_from_folder(folder_path: str) -> dict[str, pg.font.FontType] or False:
    """
    load fonts in folder ./fonts
    """
    
    fonts_folder = os.path.join(os.path.dirname(__file__), "fonts")
    
    loaded_fonts = {}
    supported_formats = (".ttf", ".otf")  # Supported Formats
    
    # Read all file in the dir
    if os.path.exists(fonts_folder) and os.path.isdir(fonts_folder) : 
        for font_file in os.listdir(fonts_folder):
            if font_file.lower().endswith(supported_formats):
                font_path = os.path.join(fonts_folder, font_file)
                try:
                    font = pg.font.Font(font_path, 24)
                    fontName = font_file.split(".")[0]
                    loaded_fonts[font_file] = font
                except Exception as e:
                    print(f"Failed to load font {font_file}: {e}")
        if loaded_fonts != {}:
            return loaded_fonts
        return False
            
    else:
        print("folder path does not exist")
        return False

def resize_canvas(new_size: Point):
    global _canvas, _display, _size
    _size = _tup(new_size)
    _display = pg.display.set_mode((new_size[0], new_size[1])) 
    _canvas = pg.Surface(_size, pg.SRCALPHA) 
    update_canvas() 
