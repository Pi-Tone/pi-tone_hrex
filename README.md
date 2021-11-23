# Dash HREX-PiTone Sample app

This is a demo app of HappyRoad Express X Pi-Tone showing some data-Vis work wrapped by deck.gl & plotly.dash.

## Getting Started

### Running the app locally

First create a virtual environment with conda or venv inside a temp folder, then activate it.

```
virtualenv venv

# Windows
venv\Scripts\activate
# Or Linux
source venv/bin/activate

```

Clone the git repo, then install the requirements with pip

```

git clone https://github.com/Pi-Tone/pi-tone_hrex
cd pi-tone_hrex
pip install -r requirements.txt

```

Run the app

```

python app.py

```

## About the app

This Dashbaord app displays geolocation related package data and risk trend involved. There are filters at the top of the app to update the graphs below. By selecting or hovering over data in one plot will update the other plots ('cross-filtering').

## Built With

- [Dash](https://dash.plot.ly/) - Main server and interactive components
- [Plotly Python](https://plot.ly/python/) - Used to create the interactive plots
- [Deck.gl](https://deck.gl/) - Used to create good rendering results based on Web.GL

## Screenshots

The following are screenshots for the app in this repo:
- N/A
