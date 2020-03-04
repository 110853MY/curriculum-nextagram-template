import os
import config
from authlib.flask.client import OAuth


oauth = OAuth()

flask_env = os.environ.get('FLASK_ENV')

if flask_env == 'production':
    config = eval("config.ProductionConfig")
else:
    config = eval("config.DevelopmentConfig")

# There was a problem with the client id and secret being returned from the config file
# I dont usually user the config file very often as it can give issues like this, I still prefer to just directly call the os.getenv value from the .env file where I need it
# If you saw just no the value I am getting looks like it is a tuple and not just the value itself
# Use breakpoint all the time everywhere, I think you understand the flow of how things work well so just go through and keep adding different breakpoints at different parts along the way and check the values as you go, it will usually become very apparent what the problem is when something where you expect a value only returns None
# You don't have to use 1 breakpoint and then try again and add another breakpoint, what you can actually do is add 4 or 5 breakpoints, once you have checked everything at 1 breakpoint you can type 'c' and press enter then it will move to the next breakpoint it hits, does that make sense? You can put anywhere, doesnt have to just be at return statements, like here i put one before the oauth register so i could check the value of the config variables
oauth.register('google',
               client_id=os.getenv('CLIENT_ID'),
               client_secret=os.getenv('CLIENT_SECRET'),
               access_token_url='https://accounts.google.com/o/oauth2/token',
               access_token_params=None,
               refresh_token_url=None,
               authorize_url='https://accounts.google.com/o/oauth2/auth',
               api_base_url='https://www.googleapis.com/oauth2/v1/',
               client_kwargs={
                   'scope': 'https://www.googleapis.com/auth/userinfo.email',
                   'token_endpoint_auth_method': 'client_secret_basic',
                   'token_placement': 'header',
                   'prompt': 'consent'
               }
               )
