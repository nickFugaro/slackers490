#! /bin/bash

cd /usr/local/bin

./rabbitmqadmin --host=localhost --port=15672 --vhost=vhost --username=guest --password=guest purge queue name=db_queue
./rabbitmqadmin --host=localhost --port=15672 --vhost=vhost --username=guest --password=guest purge queue name=be_queue
./rabbitmqadmin --host=localhost --port=15672 --vhost=vhost --username=guest --password=guest purge queue name=log_queue
