# Data Animations

**Insert badges here**

Transform time series data into smooth video animations.

**Insert preview image here**

## Table of Contents

- [Usage Guide](#usage-guide)
    - [Quick Start](#quick-start)
    - [Configuration](#configuration)
    - [Custom Data](#custom-data)
    - [Examples](#examples)
- [Development Guide](#development-guide)
    - [Installation](#installation)
- [Glossary](#glossary)
- [Credits](#credits)

## Usage Guide

### Quick Start

1. Clone this repository.

```sh
git clone git@github.com:j-freddy/data-animations.git
```

2. Create virtual environment with Python 3.10+.

```sh
# Go inside repo
cd lorem-ipsum
# Check Python 3.10+ is used
python --version
# Create virtual environment
python -m venv venv
# Activate virtual environment
source venv/bin/activate
```

3. Install dependencies.

```sh
pip install -r requirements.txt
```

To check everything has been set up correctly, let's try a test run. This
animation is ~30 seconds.
```sh
python -m main
```

Cool! Now, let's try to save this animation as a video. Run the following
command.

> [!NOTE]
> You may find the window is too large to fit on your screen (depending on your
> display size). That is OK. Simply wait until it finishes running. You can
> also let it run in the background. You can even drag the window and it will
> not affect the final video. Alternatively, you can close the window before
> the animation finishes, but only part of the animation gets saved.
```sh
python -m main -prod
```

### Configuration

See [Quick Start](#quick-start) to get started.

Run the following command for a description of usage options.
[Examples](#examples) are also provided below.

```sh
python -m main -h
```
```sh
usage: main.py [-h] [-data DATA] [-title TITLE] [-fpe FPE] [-visible VISIBLE] [-prod] [-out OUT]

optional arguments:
  -h, --help        show this help message and exit
  -data DATA        Input data filename (without extension). Must be .csv and reside in data/. Default: example
  -title TITLE      Title displayed in video. (default: IQs over time)
  -fpe FPE          Frames per timestamp. A larger value results in slower animation. Default: 2.5
  -visible VISIBLE  Number of top visible series. Default: 10
  -prod             If True, enter production mode to record and save animation as .mp4 file. Default: False (default:
                    False)
  -out OUT          If in production mode, specifies output filename (without extension). Default: video
```

### Custom Data

This section explains how to pass in a custom CSV file and have it animated.

Firstly, the CSV data must respect the following criteria.
1. The first column must contain evenly spaced timestamps. Otherwise, the
    animation will speed up and slow down according to the spacing.
2. The first row must contain series names.
3. The remaining cells, apart from the timestamps, must be numerical.

For an example, see `data/example.csv`. You are responsible for providing your
own ETL pipeline to produce a CSV file that meets these criteria.

Place the CSV file in the `data` directory.

Then, run the following command. You may need to adjust the `fpe`. A larger
value results in a slower animation.
```sh
python -m main -data <filename-without-extension> -title <any-title> -fpe <fpe>
```

### Examples

Let's use the example data, but make the animation really fast! Let's also show
more data.

```sh
python -m main -data example -title "Fast Animation: IQs over time" -fpe 0.5 -visible 14
```

Cool! Now, let's render the video and save it. (You can let the video run in the
background.)

```sh
python -m main -data example -title "Fast Animation: IQs over time" -fpe 0.5 -visible 14 -prod -out speedyvid
```

## Development Guide

Read this section if you want to make changes or contribute to this repository.
It is not necessary if you only want to use the program.

### Installation

1. Go through [Quick Start](#quick-start) in the Usage Guide.
2. Install the [Black Formatter][black-formatter]. For example, use the [Black
   Formatter Extension][black-formatter-vscode] for Visual Studio Code. The
   settings in `.vscode/` configures Black to auto-format your code on save.

[black-formatter]: https://black.readthedocs.io/en/stable/
[black-formatter-vscode]: https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

### Project Structure

This project decouples the GUI (view) from the logic (model).

- `main.py` - Entry point for the program.
- `model/` - Contains the logic for the program. The main file is
  `model/data_handler.py`, which performs calculations to prepare the data for
  animation.
- `view/` - Contains GUI-related code. The main entry point is `view/gui.py`,
  which uses [pyglet][pyglet-docs] as a multimedia library for rendering
  visuals.
- `data/` - All CSV raw data files are stored here.
- `out/` - All output video animation files are saved here.

[pyglet-docs]: https://pyglet.readthedocs.io/en/latest/

## Glossary

| Term           | Description                                                 |
|----------------|------------------------------------------------------------ |
| Series         | An individual entity or element being tracked over time (e.g. a specific city within the dataset of city populations). |
| Timestamp      | A specific point in time at which measurements or observations are recorded for all series in the dataset (e.g. a particular date when population figures were collected). |

## Credits

Inspired by @carykh's [data animations program][carykh-drawer] written in Processing.

[carykh-drawer]: https://github.com/carykh/AbacabaTutorialDrawer
