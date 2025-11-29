(Pipeline failing due to VM not being up.)

If using nix, you can use my premade local environment with :

`nix-shell -v`

If you do not use nix, you will need python 3.11 installed globally and numpy added to the requirements.txt.

Create a python env with : 

`python -m venv .venv`

Activate it :

`source .venv/bin/activate`

And install the packages (don't forget to add numpy if not using nix) :

`pip install -r requirements.txt`
