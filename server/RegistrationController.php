<?php
class RegistrationResponse {
    public $successful;

    function RegistrationResponse($successful=true){
        $this->successful = $successful;
    }

    function getJsonData(){
        $var = get_object_vars($this);
        foreach ($var as &$value) {
            if (is_object($value) && method_exists($value,'getJsonData')) {
                $value = $value->getJsonData();
            }
        }
        return $var;
    }
}

class SignatureImage {
    public $width;
    public $height;
    public $pixelData;

    function getJsonData(){
        $var = get_object_vars($this);
        foreach ($var as &$value) {
            if (is_object($value) && method_exists($value,'getJsonData')) {
                $value = $value->getJsonData();
            }
        }
        return $var;
    }
}

class RegistrationRequest {
    public $customerId;

    /**
     * SignatureImage
     */
    public $refSignA;

    /**
     * SignatureImage
     */
    public $refSignB;
    
    /**
     * SignatureImage
     */
    public $refSignC;
    
    /**
     * SignatureImage
     */
    public $refSignD;

    function getJsonData(){
        $var = get_object_vars($this);
        foreach ($var as &$value) {
            if (is_object($value) && method_exists($value,'getJsonData')) {
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
    foreach($object as $property => &$value)
    {
        $new->$property = &$value;
        unset($object->$property);
    }
    unset($value);
    $object = (unset) $object;
    return $new;
}

if (isset($_POST["payload"])) {
    $filename = "register/request.json";
    $file = fopen( $filename, "w" );

    if( $file ) {
        fwrite( $file,  $_POST["payload"]);
        fclose( $file );

        // system("/Library/Frameworks/Python.framework/Versions/2.7/bin/python register/process.py >& register/log");
    }
    
    $response = new RegistrationResponse(true);
    header("Content-type", "text/json");
    echo json_encode($response->getJsonData());
}
?>