#!/usr/bin/php
<?php
require_once('path.inc');
require_once('get_host_info.inc');
require_once('rabbitMQLib.inc');

function makeLog($logs)
{
$file = basename(__FILE__);
$date = date('m/d/Y == H:i:s'); //found on stack overflow
$logger = new rabbitMQClient("logger.ini","logServer");
$requestLog = array();
$requestLog['type'] = "send_log";
$requestLog['log'] = $logs;
$requestLog['file'] = $file;
$requestLog['date'] = $date;
$responseLog = $logger->send_request($requestLog);

}


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
$request['type'] = "login";
$request['username'] = "steve";
$request['password'] = "password";
$request['message'] = $msg;
$response = $client->send_request($request);
//$response = $client->publish($request);

if ($response == "ERROR: unsupported message type"){

	$logs = "ERROR: unsupported message type"; 
	makeLog($logs);
}

if ($response == "Incorrect Credentials"){
	
	$logs = "Incorrect Credentials"; 
	makeLog($logs);
}

if ($response == "Welcome Steve!"){
	
	$logs = "User: steve logged in"; 
        makeLog($logs);
}


echo "client received response: ".PHP_EOL;
print_r($response);
echo "\n\n";

echo $argv[0]." END".PHP_EOL;

