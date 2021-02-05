#!/usr/bin/php
<?php
require_once('path.inc');
require_once('get_host_info.inc');
require_once('rabbitMQLib.inc');

$login = "false";
function doLogin($username,$password)
{
    // lookup username in databas
   global $login;
    $user1 = "bob";
    $user2= "steve";
    $user1pass = "pass";
    $user2pass = "password";
    
	if ($username == $user1){
	   if ($password == $user1pass){
		
		$login = "Welcome Bob!"; 

	   }
	} elseif ($username == $user2){
	   if ($password == $user2pass){
		
		$login = "Welcome Steve!";
		
	   }	
	}else {
		$login = "Incorrect Credentials";
	} 
	
	return $login;
    //return false if not valid
}

function requestProcessor($request)
{
	global $login;
  echo "received request".PHP_EOL;
  var_dump($request);
  if(!isset($request['type']))
  {
    $error = "ERROR: unsupported message type";
	return $error;  
  }
  switch ($request['type'])
  {
    case "login":
      return doLogin($request['username'],$request['password']);
    case "validate_session":
      return doValidate($request['sessionId']);
  }
  return array("returnCode" => '0', 'message'=>"Server received request and processed");
}

$server = new rabbitMQServer("testRabbitMQ.ini","testServer");

echo "testRabbitMQServer BEGIN".PHP_EOL;
$server->process_requests('requestProcessor');
echo "testRabbitMQServer END".PHP_EOL;
exit();
?>

