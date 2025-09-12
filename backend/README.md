# Requirements
* Python 3.12 

# How to run 
* Create a virtual environment by running `python -m venv .venv`
* Activate the virtual environment with `source .venv/bin/activate`
* Install requirements by running `pip install -r requirements.txt`
* Run the API by running `fastapi dev api/main.py --port <API-PORT>` (with a suitable port of your choosing). The API will be available at `localhost:<API-PORT>`
* Access the Swagger at `localhost:<API-PORT>/docs`