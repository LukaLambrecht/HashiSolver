# Graphical interface implementation with PyQt5 and matplotlib

This serves as an alternative for the `bokeh` based approach (see the `gui-bokeh` folder).

### Prerequisites
On top of the general prerequisites (see the [general instructions](https://github.com/LukaLambrecht/HashiSolver)), you'll need the `matplotlib` and `PyQt5` packages.
The former can be installed with (for example) `pip3 install matplotlib`, and the latter with `pip3 install 'PyQt5<5.15` (the version restriction seems to be needed to avoid conflicts).

### Preparing the input
You'll need your Hashi puzzle to solve in the form of a `.txt` file.
See the [general instructions](https://github.com/LukaLambrecht/HashiSolver) for more info.

### Launching the GUI
Run `./launch.sh` or alternatively `python3 gui.py`.

### Using the GUI
After launching the GUI, you will see this display:

![](../docs/gui-pyqt5/welcome.png)

Click the `Load` button, navigate to your prepared input `.txt` file, and open it. For example:

![](../docs/gui-pyqt5/initial.png)

Then click the `Solve` button. If the puzzle can be solved, you will see something like this:

![](../docs/gui-pyqt5/solved.png)
