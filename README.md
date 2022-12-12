# Medical Textual Data Analysis

The project extracts important information from the medical data and covers visualizations of the data with respect to different parameters.

## Team Members

The following is the list of our team members, all of us belonging to Computer Engineering (4th year).

- [Shrawak Bhattarai (11)](https://github.com/Shrawak)
- [Ramraj Chimouriya (14)](https://github.com/RamrajCh)
- [Deependra Kumar Gupta (18)](https://github.com/Deependra12)
- [Shreyam Pokharel (40)](https://github.com/pshreyam)

## Get Started

The project uses python3. Any version of python3 above python3.6 should be compatible. Python3 can be downloaded from [https://www.python.org/downloads/](https://www.python.org/downloads/).

### Install Dependencies

Extract the zip file and locate `requirements.txt` file in the folder.

Run the following command in order to install the dependencies:

```bash
pip install -r requirements.txt
```

### Setup Database

Before proceeding forward, MongoDB database access credentials has to be put in .env file as specified in .env-sample file. You can just rename .env-sample to .env and update the information.

### Run the app

After the dependencies are installed in the system and MongoDB database is set up, run `app.py` script as:

```bash
python app.py
```

After successfully running the script, goto `http://127.0.0.1:8050` in your browser to access medical data visualization.
