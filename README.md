# LibMGE 

Version: 1.0.0  

## Installing
```
pip install MGE
```

## Dependencies
[`numpy`](https://pypi.org/project/numpy/)

## Example of use
```py
import MGE  # Import the LibMGE

MGE.init()  # Initialize the library

window = MGE.Window(resolution=(500, 500), flags=MGE.WindowFlag.Shown)  # Create a window
window.frameRateLimit = 60  # Set frame rate limit

gif = MGE.Object2D((0, 0), 0, (500, 500))  # Create a 2D object
gif.material = MGE.Material(MGE.Texture(MGE.LoadImage("./image.gif")))  # Load the GIF and assign to object

while True:
    MGE.update()  # Update logic
    window.update()  # Update window

    window.title = f"LibMGE OpenGif | FPS: {window.frameRate}"  # Display FPS in window title

    if MGE.QuitEvent() or MGE.keyboard(MGE.KeyboardButton.F1):  # Exit if quit event or F1 key is pressed
        exit()

    gif.drawObject(window)  # Draw GIF object on window
```
