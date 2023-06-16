# MGE 

Version: 0.2.0  
[other versions](https://github.com/lucas224112/MGE_Other_Versions)

## Installing
```
pip install MGE
```

## Dependencies
[`pygame`](https://pypi.org/project/pygame/) -
[`numpy`](https://pypi.org/project/numpy/) -
[`pillow`](https://pypi.org/project/Pillow/) -
[`opencv-python`](https://pypi.org/project/opencv-python/) -
[`pyperclip`](https://pypi.org/project/pyperclip/) -
[`screeninfo`](https://pypi.org/project/screeninfo/)

## Example of use
```py
import sys
import MGE

MGE.Program.init()

gif = MGE.Object2D([0, 0], 0, [500, 500])
gif.set_material(MGE.Material(MGE.Texture(MGE.Image("./image.gif"))))

MGE.Program.screen.set_size(500, 500)
MGE.Program.set_clock(120)

while True:
    if MGE.Program.event.type == MGE.Screen_inputs.quit or MGE.keyboard("f1"):
        sys.exit()

    gif.draw_object(MGE.Program.screen)

    MGE.Program.set_caption(f"Gif-MGE | FPS:{int(MGE.Program.get_fps())}")
    MGE.Program.update()
```
