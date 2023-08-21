# Drum sensor solver demo

Try out solving equations!

## how to install

```bash
pip install virtualenv
python -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

## how to run

```bash
source .venv/bin/activate
python predict_point.py
```

## how to run tests

```bash
pytest
```

## how to run with OSC

### start server

Nb. only receives messages & prints results to terminal right now

```bash
source .venv/bin/activate
python osc-server.py
``` 

### send test message

In a separate terminal:

```bash
source .venv/bin/activate
python osc-client.py
``` 
