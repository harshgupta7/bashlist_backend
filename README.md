# Bashlist Backend

Backend Server for Bashlist.


# Setup

* `pip install -r requirements.txt` -- install all the requirements for the project.


# Testing (TODO)

* `pytest`

# Running

* `python app.py` -- Starts the server in debug mode.


## Supported endpoints:
* GET `/account` -- Returns unique URL for user to access acount
* GET `/getallfiles` -- Returns a JSON representation of all files currently in users storage
* GET `/filedown/<string:name>` -- Returns the file for the user
* GET `'/filedownloader/<string:one>/<string:realval>/<string:three>'` -- Downloads file as an attachment.
* POST `/register` -- New account registration
* POST `/sendmail` -- sends mail with the downloadable link to the file
* DELETE `/filedown/<string:name>` -- Deletes a file from user's storage
