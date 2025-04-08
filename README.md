# Pokemon Sound!
This Python program allows you to play pokemon calls from an external API. The program uses the `requests` library to fetch the pokemon's .ogg sound file.

## Features
- Login to keep different users pokemon separate.
- The ability to play the pokemon's sound.
- Storage of the pokemon's sound for easier access later on
- When asked, it can give a random pokemon's sound
- A easy to use GUI

## Requirements
To run this program, you need to install the following dependencies:

- `tkinter` to run the GUI.
- `requests` to make HTTP requests to the weather API.
- `threading` to allow for higher efficiency and the ability to run programs simultaniously
- `os` to store the .ogg file
- `random` to generate a random pokemon
- `pathlib` to read, write, move and delete files
- `time` to pause for download time
- `csv` to have a place to store the login

### Install dependencies
To install the required dependencies, you can run:

```bash
pip install -r requirements.txt