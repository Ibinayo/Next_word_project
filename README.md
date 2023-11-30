# Next Word Predictor
### What is the next word predictor
The next word predictor is an ML project which makes use of sequence generation packages (i.e, texnsorflow) to predict five possible net words.

### How to start the application

- Open the project folder in an editor(VS code, etc) or the command-line/terminal

-If you don't have a python enviroment, we create one. If you don't use 'python3', you can use 'python'. If you have, skip this step.

> `frankiw:¬/Next_Word_Project$ python3 -m venv env`

-This will create an *env* folder in your directory. 

> `frankiw:¬/Next_Word_Project$ source env/bin/activate`

This will activate the python environment

`(env) frankiw:¬/Next_Word_Project$ `

- Install the packages in the requirements.txt fie
>`(env) frankiw:~/Next_Word_Project$ pip install -r requirements.txt `<br>

- The above code installs the packages in the requirements file necessary to run the project.

- Confirm the project's content

> `(env) frankiw:~/Next_Word_Project$ ls`<br>
>*app*<br>
*config.py*<br>
*nwp.py*<br>
*requirements.txt*<br>
*migrations*<br>
*instance* <br>


- If *instance* and *migrationsis not present in the project's file, we'll need to run some commands to initialise the database. 
- If they are, please skip the next three steps
> `(env) frankiw:~/Next_Word_Project$ flask db init`<br>

This command will output some information that will have a similar format to this:

 >*Creating directory '~/Next_word_project/migrations' ...  done*<br>
  Creating directory '~/Next_word_project/migrations/versions' ...  done<br>
  Generating ~/Next_word_project/migrations/script.py.mako ...  done<br>
  Generating ~/Next_word_project/migrations/env.py ...  done<br>
  Generating ~/Next_word_project/migrations/alembic.ini ...  done<br>
  Generating ~/Next_word_project/migrations/README ...  done<br>
  Please edit configuration/connection/logging settings in '~/Next_word_prj/migrations/alembic.ini' before proceeding. *<br>

Then we run:

> `(env) frankiw:~/Next_Word_Project$ flask db migrate`<br>

This command will output some information that will have a similar format to this:

>*INFO  [alembic.runtime.migration] Context impl SQLiteImpl.<br>
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.<br>
INFO  [alembic.autogenerate.compare] Detected added table 'user'<br>
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'<br>
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_username' on '['username']'<br>
  Generating ~/Next_word_project/migrations/versions/5da739186931_.py ...  done*<br>

  Then: 

> `(env) frankiw:~/Next_Word_Project$ flask db upgrade`<br>

This command will output some information that will have a similar format to this:

>*INFO  [alembic.runtime.migration] Context impl SQLiteImpl.<br>
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.<br>
INFO  [alembic.runtime.migration] Running upgrade  -> 5da739186931, empty message*<br>

- Now *instance* and *migrations* folders will be in the project folder. The instance folder contains the sqlite database

- Then we run our application.

> `(env) frankiw:~/Next_Word_Project$ python3 -m nwp`<br>
 > some text.....
 > *Serving Flask app 'app'*<br>
 *Debug mode: on*<br>
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.*<br>
 *Running on http://127.0.0.1:5050*<br>
Press CTRL+C to quit
 *Restarting with stat*<br>
 *Debugger is active!*<br>
 *Debugger PIN: 971-672-220*<br>

 - Then 'ctrl+click' on the http link. This will open a browser tap that will run the appication.

- You can also go the browser and input in the http link if preferred.

- Note: Internet connection is needed for the proper functioning of the application

## Please read

`It should be noted that this model is made to function on user previous input, but predictions will still be made.`
`To save your user input, click the 'Clear the textarea' button.`
`If any error is given, please, retake the steps`
