# Core Data Service

## Requirements
- Python 3.13


## Running the application
### Local
To run the application locally you will have to install ffmpeg and libmagic on your local machine plus the requirements.txt

install ffmpeg and libmagic (on mac):
`brew install ffmpeg`
`brew install libmagic`

install requirements:  
`pip install -r requirements.txt`

### From container
from the root directory run the following command:

build and run the image:
`docker compose up`


## Linting

The project uses pre-commit. Make sure you have `pre-commit` installed in your local venv (can be installed from the requirements.txt) then run:

    pre-commit install


### Running tests
You can run local tests by doing `pytest .` from the project root.

