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

(from homework 4)
Generate and set a (32 character) JWT_SECRET to hash your password. Keep this token secret and do not share it If you lose it, users will not be able to log in.

python -c "import secrets; print(secrets.token_hex(32))"
$env:JWT_SECRET = "paste-your-generated-value-here"