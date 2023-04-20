# Data Animations

Using [pyglet][3] as a multimedia library.

## Setup

### Virtual environment

```bash
# Create virtual environment
$ python -m venv venv
# Activate on Linux, OS X
$ source venv/bin/activate
# Activate on Windows
$ source venv/Scripts/activate
# Check Python 3.10.8 is used. Some scripts may fail on Python 3.11
$ python
Python 3.10.8
>>> exit()
# Install requirements
$ pip install -r requirements.txt
```

## Run

### Development

Set `PROD = False` in `const.py`.

```bash
$ python main.py
```

### Production

Set `PROD = True` in `const.py` and `FILEOUT = video.mp4` or whatever you want
the filename to be.

```bash
$ python main.py
```

At the end of the animation, the video can be found under `out/video.mp4`.

## Contribute

### Update requirements

```bash
$ pip freeze > requirements.txt
```

## Credits

Inspired by @carykh's drawer written in Processing ([repo][1] and
[tutorial][2]). If you are a beginner, I fully recommend his tutorial as it is
simple and easy to follow. That said, I have extended many features and made
numerous improvements in optimisation and code hygiene.

[1]: https://github.com/carykh/AbacabaTutorialDrawer
[2]: https://www.youtube.com/playlist?list=PLsRQr3mpFF3Khoca0cXA8-_tSloCwlZK8
[3]: https://pyglet.readthedocs.io/en/latest/
