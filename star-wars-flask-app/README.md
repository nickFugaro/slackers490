  
1. Install all packages  
    `npm install`  
    `pip install flask-socketio`  
    `pip install eventlet`  
    `pip install --upgrade google-auth`
    `npm install -g webpack`  
    `npm install --save-dev webpack`  
    `npm install socket.io-client --save` 
    `pip install requests`
    `npm install @material-ui/core`
    `npm install react-scroll-to-bottom`
    `npm install react-google-login`

2. Setup PSQL
    * Update yum: `sudo yum update` (answer yes to all prompts)   
    * Upgrade pip: `sudo /usr/local/bin/pip install --upgrade pip`  
    * Get psycopg2: `sudo /usr/local/bin/pip install psycopg2-binary`    
    * Get SQLAlchemy: `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`    
  
3. Setting up PSQL  
    * Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`(Enter yes to all prompts.)
    * Initialize PSQL database: `sudo service postgresql initdb`    
    * Start PSQL: `sudo service postgresql start`    
    * Make a new superuser: `sudo -u postgres createuser --superuser $USER` (Ignore errors)
    * Make a new database: `sudo -u postgres createdb $USER` (Ignore errors)   
    * Look for the user using:    
        a) `psql`    
        b) `\du` look for ec2-user as a user    
        c) `\l` look for ec2-user as a database    
    * Make a new user:    
        a) `psql` (if you already quit out of psql)    
        b) `create user [some_username_here] superuser password '[some_unique_new_password_here]';` (Replace all values in square brackets)
        c) `\q` to quit out of sql    
    * `cd` into the Assignment 2 folder and make a new file called `sql.env` and add `SQL_USER=` and `SQL_PASSWORD=` in it  
    * Fill in those values with the values you put in 7. b)  
  
  
4. Enabling read/write from SQLAlchemy  
  
    * Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
    * Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
    * After changing those lines, run `sudo service postgresql restart`  
    * Ensure that `sql.env` has the username/password of the superuser you created!  
    * You have to source by doing: `source sql.env`
    * Run your code!    
          a) `npm run watch`. If prompted to install webpack-cli, type "yes"    
          b) In a new terminal, `python app.py`    
          c) Preview Running Application (might have to clear your cache by doing a hard refresh)   

5. Google OAuth

    * You will have to set up a under the Google API Console here: `https://console.developers.google.com/`
    * From there you will have to create a project and retrive its Client ID from the credentials page to utilize for Google Authentication.
    * You will also need to take the link of your heroku app after its deployed and add it to the 'Authorized JavaScript Origins' section under the credentials page.

6. Deploy to Heroku

    * To set up with Heroku you will have to start by signing up at heroku.com
    * Install Heroku with `npm install -g heroku`
    * Login with Heroku with `heroku login -i`
    * Do a Heroku Creat `heroku create`
    * Install postgres on Heroku with `heroku addons:create heroku-postgresql:hobby-dev`
    * Set heroku as a git remote with `heroku git:remote -a [yourappname]` (Replace what it is in brackets with your app's name)
    * Push to heroku master `git push heroku master`

## 3 Issues I Had With The Project

1. I initally could not get the message and user chip to line up when I had set the dangerouslySetInnerHTML tag in place. I was able to solve this by finding that using the style in CSS called display: 'inline block' I was able to rectify the positioning.
2. I also could not get the profile picture formatted properly to be in line with the user name and message, but the adjusting with the posiitoning using 'top' needed to make the position: 'relative' in CSS.
3. Initially I also had issues with deployment to Heroku, but I realized that I had to do another pip freeze > requirements.txt to account for the newly used google auth libraries.

## 2 Ways I Could Have Improved This With More Time

1. For some reason now that I have the message, profile picture, and username in line, which looks aesthetically better than my last approach with the message under the username, has made the username within the chip go up a little and makes it look a little off, will need to fix that somehow. 
2. I also want to get the user side messages on to one side for the active user on the screen as well going forward.  

## Yoda Bot Commands!!!

I can help you with the following commands: 
-!!about: A little bit about me this will tell! Hrmmm. 
-!!help: I will return a list of all the things I can help you with. Hrmmm. 
-!!funtranslate - Return a message, I can, in a fun language! 
-!!quote - Returns a a famous quote from our beloved franchise! 
-!!force - You if you are one with the force I will tell. Yes, hrrmmm.! 
-If you throw in an image link, Yoda force push you back the real thing!



