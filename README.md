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
