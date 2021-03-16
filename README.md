# Instructions for Testing the whole system LOCALHOST

**Make a Virtual Machine with Ubuntu 18.04 or 20.04 OS**

**Update apt repoistories**
 >sudo apt update -y
 
 >sudo apt upgrade -y

**Install RabbitMQ Server**
 >sudo apt install rabbitmq-server -y
 
 >sudo service rabbitmq-server start
 
 >sudo rabbitmq-plugins enable rabbitmq_management\

**Install Python and Pip**
 >python3 --version
 
 >sudo apt install python3-pip -y

**Install Git and clone the repo**
 >sudo apt install gitk -y
 
 >mkdir git
 
 >cd git/
 
 >git clone --branch local https://github.com/nickFugaro/slackers490.git

**Install MYSQL**
 >sudo apt install mysql-server -y
 
 >sudo mysql_secure_installation
 
 Press N then Enter\
 Set your password\
 Press N then Enter\
 Press Y then Enter\
 Press Y then Enter\
 Press Y then Enter
 
 >sudo mysql
 
 **In MYSQL Shell**
 >CREATE DATABASE IT490;
 
 >CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminIT490Ubuntu!';
 
 >GRANT ALL PRIVILEGES ON * . * TO 'admin'@'localhost';
 
 >exit
 
 **In Terminal**
 >cd git/slackers490/StarWarsSite/DBServer
 
 >mysql -u admin -p IT490 < DBdump.sql
 
 password:
 >adminIT490Ubuntu!
 
**Install Pip Packages**

 >pip3 install tweepy
 
 >pip3 install pika
 
 >pip3 install cryptohash
 
 >pip3 install mysql-connector
 
 >pip3 install PyJWT
 
 >pip3 install simplejson
 
 >pip3 install Flask
 
**Configure RabbitMQ Server**
 
 Open Firefox\
 Navigate to 
 >localhost:15672
 
 Username is
 >guest
 
 Password is
 >guest
 
 Navigate to Admin tab\
 Click Users tab in Admin tab\
 Add a User\
 Username:
 >test
 
 Password:
 >test
 
 Navigate to Virtual Hosts tab in Admin tab\
 Add a new virtual host\
 name:
 >vhost
 
 Click on vhost in the list of virtual hosts\
 Go to the permissions tab\
 Choose guest and give * on all permissions\
 CLick Set Permission\
 Do the same with test account\
 Scroll up and select the dropdown in the top right(it should currently be a /)\
 Change it to vhost\
 Navigate to the Exchanges tab\
 Scroll down to Add new exchange\
 Name:
 >beExchange
 
 Type: Direct\
 Durable\
 No\
 No\
 Repeat this process but just change the name to the following 3:
 >dbExchange
 
 >apiExchange
 
 >logExchange
 
**Create API Source File**

 In terminal
 >cd git/slackers490/StarwarsSite/APIServer
 
 >nano custom.env
 
 Copy and paste this configuration and enter your keys:
 >#Twitter
 >export API_KEY="your key"
 >export API_KEY_SECRET="your key"
 >export BEARER_TOKEN="your key"
 >export ACCESS_TOKEN="your key"
 >export ACCESS_TOKEN_SECRET="your key"
 
 >ctrl+o
 
 >ctrl+x
 
**Start the various servers**

 >cd git/slackers490/StarWarsSite
 
 Open **5** terminal tabs in that directory\
 Tab One:
 >cd BackEnd
 
 >./pyLogServer.py
 
 Tab Two:
 >cd APIServer
 
 >source custom.env
 
 >./pyServerAPI.py
 
 Tab Three:
 >cd DBServer
 
 >./pyServerDB.py
 
 Tab Four:
 >cd BackEnd
 
 >./pyServer.py
 
 Tab Five:
 >cd FrontEnd
 
 >python3 main.py
 
 CTRL+Click the Link
 
