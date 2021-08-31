# What is this
The first implementation, out of 3 (1/3), of the portable dashboard I had been working on, which was asked of me during a research project I had been working on. This was the first project I had ever coded, start to finish, and also created a website from. Originally, this website had used gspread and Oauth2Lib to interface with google sheets. So anytime the sheets file was updated, it updated the graphs. This was convenient and cool, but had to be reworked to use a local excel file instead due to using up the free period offered on google cloud platform. Still works, just mentioning because it used to be even cooler.

# Installation
If interested in running a local version, clone this repo and make sure to have pip installed.

Then, make a separate virtualenv like so (this example makes a virtual environment named myvenv at the given path): python -m venv c:\path\to\myenv

copy the contents of the cloned repo into this new venv folder. Activate the venv like so: cd venv\path\to\myenv\Scripts then type "activate" and hit enter

The name of your venv should appear next to the command prompt. Now type: cd ..

And finally: pip install requirements.txt. If this does not work, packages need to be installed manually.

Then, running the app/app.py file in your editor of choice will boot up a local Flask server, which you can then do as you please with.
