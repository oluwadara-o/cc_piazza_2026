This is the backend for Piazza a social media application to 
allow user to make and read posts via the API

Set Up Instructions
```shell
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Running the Server
```shell
uvicorn main:app --reload
```

Testing:
```shell
python -m pytest
```