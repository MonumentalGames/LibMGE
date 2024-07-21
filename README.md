# MGE 

Version: 0.9.8  

## Installing
```
pip install MGE
```

## Dependencies
[`numpy`](https://pypi.org/project/numpy/)

## Example of use
```py
import MGE

MGE.init()

window = MGE.Window(resolution=(500, 500), flags=MGE.WindowFlag.Shown)
window.frameRateLimit = 60

gif = MGE.Object2D([0, 0], 0, [500, 500])
gif.material = MGE.Material(MGE.Texture(MGE.LoadImage("./image.gif")))

while True:
    MGE.update()
    window.update()

    window.title = f"LibMGE OpenGif | FPS: {int(window.fps)}"

    if MGE.QuitEvent() or MGE.keyboard(MGE.KeyboardButton.F1):
        exit()

    gif.drawObject(window)
```
