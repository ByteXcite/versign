<?php

/**
 * Created by PhpStorm.
 * User: saifkhichi96
 * Date: 28/05/2017
 * Time: 1:02 PM
 */
class Parser
{
    public static function parseRequest($request, $object)
    {
        $stdObj = json_decode($request);
        return self::cast($object, $stdObj);
    }

    /**
     * recast stdClass object to an object with type
     *
     * @param string $className
     * @param stdClass $object
     * @throws InvalidArgumentException
     * @return mixed new, typed object
     */
    private static function cast($new, stdClass &$object)
    {
        foreach ($object as $property => &$value) {
            $new->$property = &$value;
            unset($object->$property);
        }
        unset($value);
        $object = (unset)$object;
        return $new;
    }

    public static function echoResponse($object)
    {
        if (method_exists($object, "getJsonData")) {
            header("Content-type: application/json");
            echo json_encode($object->getJsonData());
        }
    }
}

?>