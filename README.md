# Flask Tutorials

1. Flaskr - A basic blog application

#### Usage and testing
* Install and set-up [Python3](https://www.python.org/downloads/)
* Install and set up a [pipenv & virtual environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* Install and set-up [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) Version control
On a web browser 
* [Download](https://github.com/artorious/flask_dojo/archive/master.zip) the repo as a zip folder
* Extract `flask_dojo` directory and navigate into it, 
OR
* Clone `git clone  https://github.com/artorious/flask_dojo.git`
* Navigate to repo's root folder `cd flask_dojo/`
* Checkout the Static files branch `$ git checkout flaskr`
* Install & set-up the project with it's dependencies and requirements 
`$ pipenv install -e .`est
* On a Unix-like command-line, run `$ coverage run -m pytest -v`to test
* Setup Flask server`$ export FLASK_APP=flaskr;  flask run`
* On a web browser navigate to [http://127.0.0.1:5000.](http://127.0.0.1:5000)
Interact with the webApp
* On Postman and run this [collection of requests](https://www.getpostman.com/collections/88efa5feed80f717cab9)



##### Attribution
[Flaskr](http://flask.pocoo.org/docs/1.0/tutorial/#tutorial)
