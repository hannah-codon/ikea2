# Requirements
* Python 3.12 

# How to run 
* Create a virtual environment by running `python -m venv .venv`
* Activate the virtual environment with `source .venv/bin/activate`
* Install requirements by running `pip install -r requirements.txt`
* Create a .env file with the variables:
    * `PORT=<SUITABLE API PORT>`
    * `DB_USER=postgres`
    * `DB_PASSWORD=PASSWORD`
    * `DB_NAME=hackathon_db`
    * `DB_HOST=hackathon-pgvector-db`
    * `DB_PORT=5432`
* Run the API by running `make run`. The API will be available at `localhost:<API-PORT>`
* Access the Swagger at `localhost:<API-PORT>/docs`