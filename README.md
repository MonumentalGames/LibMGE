# MGE 

Version: 0.9.4  
[other versions](https://github.com/lucas224112/MGE_Other_Versions)

## Installing
```
pip install MGE
```

## Dependencies
[`numpy`](https://pypi.org/project/numpy/)

## Example of use
```py
import sys
import MGE

MGE.init()

window = MGE.Window(resolution=(500, 500), flags=MGE.WindowFlag.Shown)
window.limit_time = 120

gif = MGE.Object2D([0, 0], 0, [500, 500])
gif.material = MGE.Material(MGE.Texture(MGE.LoadGif("./image.gif")))

while True:
    MGE.update()
    window.update()

    window.title = f"Gif-MGE | FPS:{window.fps}"

    if MGE.QuitEvent() or MGE.keyboard(MGE.KeyboardButton.F1):
        sys.exit()

    gif.draw_object(window)
```
