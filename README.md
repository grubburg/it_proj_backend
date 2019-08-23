# it_proj_backend
object storage platform API

## Proposed Technologies
- Flask
- Firebase (firestore)

## Setting up the app
- Make sure you can python venv installed : `pip install virtualenv`
- create your virtual environment. I created one called `objectify` but you can use any name, just make sure that if you create the environment within the git repo, to add it to the .gitignore.
- run the venv with `source <venv name>/bin/activate`
- run `pip install -r requirements.txt` to install flask and other dependencies
- Now you can run the app with `gunicorn app:app`
