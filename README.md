# Instructions for Testing the whole system

  To run an API server you need Twitter API keys\
  To run a DB server you need a copy of the database\
  All IPs in all the server and client files need to be set to rabbitMQ server IP (localhost if its all on one VM)\
  To run rabbitMQ Server make sure you have it installed, then do systemctl start rabbitmq-server(It'll open if you go to localhost:15672)\
  Log into rabbitMQ management with guest guest\
  Go to Admin > add new user > name user test and password is test\
  In Admin add new vhost name it vhost, then make sure to switch to it in the top right dropdown(would currently be a /)\
  Give guest and test all priviledges on vhost\
  Go to exchanges and make sure you are in vhost in top right corner\
  Add 4 new exchanges with default settings:\
  beExchange\
  dbExchange\
  apiExchange\
  logExchange\
  Run Log Server, API Server, DB Server, BE Server, main.py\
  Click link in main.py console to see site\
