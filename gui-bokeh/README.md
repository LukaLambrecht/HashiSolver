# Simple graphical user interface implementation

This GUI implementation uses [bokeh](https://bokeh.org/).
It has the basic functionality of loading an input `.txt` encoding a Hashi puzzle and solving it.

Note: for an alternative implementation not using the webbrowser-based `bokeh`, but rather the standard GUI toolkit `PyQt5`, see the `gui-pyqt5` folder instead.

### Prerequisites
On top of the general prerequisites (see the [general instructions](https://github.com/LukaLambrecht/HashiSolver)), you'll need the `bokeh` package.
Install it for example with `pip install bokeh`.

### Preparing the input
You'll need your Hashi puzzle to solve in the form of a `.txt` file.
See the [general instructions](https://github.com/LukaLambrecht/HashiSolver) for more info.

### Launching the GUI
Run `./launch.sh` or alternatively `bokeh serve --show launch.py`.

### Using the GUI
After launching the GUI, you will see this display:

![](../docs/gui-bokeh/welcome.png)

Click the `Load` button, navigate to your prepared input `.txt` file, and open it. For example:

![](../docs/gui-bokeh/initial.png)

Then click the `Solve` button. If the puzzle can be solved, you will see something like this:

![](../docs/gui-bokeh/solved.png)

### Closing the GUI
You can just close the browser window. But to stop the actual underlying process, use the `ctrl`+`c` keys (or alternatively `ctrl`+`z`, but in that case you won't be able to launch again until you close the terminal and open a new one, or manually free the socket used by this application).
