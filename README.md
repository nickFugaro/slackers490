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
 
 
