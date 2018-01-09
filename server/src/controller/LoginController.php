<?php
require_once(realpath(dirname(__FILE__)) . "/Parser.php");
require_once(realpath(dirname(__FILE__)) . "/../src/entity/Credentials.php");
require_once(realpath(dirname(__FILE__)) . "/../src/dao/StaffDAO.php");

if (isset($_GET["payload"])) {
    $credentials = Parser::parseRequest($_GET["payload"], new Credentials());   // Read credentials passed in payload

    if (($staff = (new StaffDAO())->get($credentials->getUsername())) != null   // If employee exists
        && strcmp($staff->getPassword(), $credentials->getPassword()) == 0      // and passwords match
    ) {
        Parser::echoResponse($staff);
    }
}