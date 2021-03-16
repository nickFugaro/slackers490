# Instructions for Testing the whole system LOCALHOST

Make a Virtual Machine with Ubuntu 18.04 or 20.04 OS\

Update apt repoistories\
 >sudo apt update -y
 
 >sudo apt upgrade -y
Install RabbitMQ Server\
 >sudo apt install rabbitmq-server -y
 
 >sudo service rabbitmq-server start
 
 >sudo rabbitmq-plugins enable rabbitmq_management
Install Python and Pip\
 >python3 --version
 
 >sudo apt install python3-pip -y
Install Git\
 >sudo apt install gitk -y

