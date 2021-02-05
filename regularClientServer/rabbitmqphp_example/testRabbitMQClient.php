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
    
}

$request = array();
//$request['type'] = "login";
$request['username'] = "steve";
$request['password'] = "password";
$request['message'] = $msg;
$response = $client->send_request($request);
//$response = $client->publish($request);
$log = "ERROR: unsupported message type";
if ($response == $log){



$logger = new rabbitMQClient("logger.ini","logServer");
 $requestLog = array();
$requestLog['type'] = "recieve_log";
$requestLog['log'] = $log;
$responseLog = $logger->send_request($requestLog);
}
if ($response == "Incorrect Credentials"){
	$logger = new rabbitMQClient("logger.ini","logServer");
	$requestLog = array();
	$requestLog['type'] = "recieve_log";
	$requestLog['log'] = "Incorrect Credentials"; 
	$responseLog = $logger->send_request($requestLog);
}

if ($response == "Welcome Steve!"){
	$logger = new rabbitMQClient("logger.ini","logServer");
        $requestLog = array();
        $requestLog['type'] = "recieve_log";
        $requestLog['log'] = "Welcome Steve!"; 
        $responseLog = $logger->send_request($requestLog);
}
echo "client received response: ".PHP_EOL;
print_r($response);
echo "\n\n";

echo $argv[0]." END".PHP_EOL;

