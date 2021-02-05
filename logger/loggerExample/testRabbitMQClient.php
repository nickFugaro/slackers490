#!/usr/bin/php
<?php
require_once('path.inc');
require_once('get_host_info.inc');
require_once('rabbitMQLib.inc');

$client = new rabbitMQClient("testRabbitMQ.ini","testServer");
if (isset($argv[1]))
{
  $msg = $argv[1];
}
else
{
  $msg = "test message";
  $log = "Message sent successfully";
}

$request = array();
$request['type'] = "Login";
$request['username'] = "bob";
$request['password'] = "pass";
$request['message'] = $msg;
$response = $client->send_request($request);
//$response = $client->publish($request);

$logger = new rabbitMQClient("logger.ini","logServer");
$requestLog = array();
$requestLog['type'] = "recieve_log";
$requestLog['log'] = $log;
$responseLog = $logger->send_request($requestLog);

echo "client received response: ".PHP_EOL;
print_r($response);
print_r($responseLog);
echo "\n\n";

echo $argv[0]." END".PHP_EOL;

