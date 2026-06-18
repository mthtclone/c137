Workspace setup:

```
python -m venv venv
source venv/Script/activate
pip install -r requirements.txt
pre-commit install
```

---

Run this every time before you commit your codes:

`ruff check .` 

and

`black .`

---

The workspace has makefile and you need to make sure you have installed `make` on your system.

Install via one of these on Window:

Chocolatey - `choco install make`
Scoop - `scoop install make`

Install via one of these on MacOS:

`xcode-select --install` 

or 

Homebrew - `brew install make`

These are the available Make commands:

```
make run      # start the game (not applicable yet)
make lint     # run ruff checks
make format   # run black formatter
make hooks    # run pre-commit on all files
```

---



