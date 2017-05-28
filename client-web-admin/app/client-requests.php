<?php

/**
 * Created by PhpStorm.
 * User: saifkhichi96
 * Date: 28/05/2017
 * Time: 1:02 PM
 */
class Greeting
{
    public $sender;
    public $message;

    function __construct($sender = "", $message = "")
    {
        $this->sender = $sender;
        $this->message = $message;
    }

    function getJsonData()
    {
        $var = get_object_vars($this);
        foreach ($var as &$value) {
            if (is_object($value) && method_exists($value, 'getJsonData')) {
                $value = $value->getJsonData();
            }
        }
        return $var;
    }
}

/**
 * recast stdClass object to an object with type
 *
 * @param string $className
 * @param stdClass $object
 * @throws InvalidArgumentException
 * @return mixed new, typed object
 */
function recast($new, stdClass &$object)
{
    foreach ($object as $property => &$value) {
        $new->$property = &$value;
        unset($object->$property);
    }
    unset($value);
    $object = (unset)$object;
    return $new;
}

header("Content-type: application/json");
if (isset($_GET["payload"])) {
    $stdObj = json_decode($_GET["payload"]);
    $greeting = recast(new Greeting(), $stdObj);
    $greeting->sender = "Server";
    $greeting->message = "Hi, Client! You said \"" . $greeting->message . "\"";
} else {
    $greeting = new Greeting("Server", "Hi, Client! You did not say anything.");
}
echo json_encode($greeting->getJsonData());
?>