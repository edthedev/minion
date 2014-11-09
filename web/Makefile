
env:
	virtualenv --no-site-packages ENV; chmod +x ENV/bin/activate

requirements:
	ENV/bin/activate; ENV/bin/pip install -r requirements.txt

runserver: 
	ENV/bin/activate; ENV/bin/python web.py
