# Hello world: BESSER + n8n

First step of the seminar stack named in the slides: **BESSER** ([besser-pearl.org](https://besser-pearl.org)) with **n8n** ([github.com/n8n-io/n8n](https://github.com/n8n-io/n8n.git)) as the backend.

This folder is only that hello world. It does not change the Dungeon M-AI-nd app in the rest of this repository.

## What it does

1. `model.py` defines a BESSER B-UML domain model named `Hello` with one class, `Greeting`, and one string attribute, `text`.
2. BESSER's Python generator writes `output/classes.py`.
3. `hello.py` builds `Greeting(text="Hello, world")` and POSTs `{"text": "Hello, world"}` to a webhook.
4. The webhook answers with JSON: `source` and the same `text`.

## Run it

Use Python 3.11 or 3.12 (the versions the BESSER tutorial tests). From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python hello.py
```

You should see the model name `Hello`, the generated file `output/classes.py`, `Greeting.text: Hello, world`, and a JSON reply whose `text` is `Hello, world`. The default `source` is `local-stand-in`.

No account, API key, or running n8n is required for this command.

## What the student adds for real n8n

The default webhook is `stand_in.py`. It speaks the same path and JSON as `n8n/hello-workflow.json`, and it is not n8n.

n8n, from the repository the slides link, asks you to create an owner account in the browser the first time it starts. This hello world does not create that account and does not ship a password or an API key.

1. Install n8n using the quick start on [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n.git) (Docker). Open `http://localhost:5678` and create your own owner account.
2. In the editor, use the workflow menu and choose **Import from File**. Select `n8n/hello-workflow.json`.
3. Publish the workflow. The production webhook is `http://localhost:5678/webhook/hello`. The webhook node uses no authentication.
4. Run:

```bash
N8N_WEBHOOK_URL=http://localhost:5678/webhook/hello python hello.py
```

The reply `source` is then `n8n`. While you are still editing, n8n's test URL is `http://localhost:5678/webhook-test/hello`, and it answers only after you choose **Listen for test event**.
