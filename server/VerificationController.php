<?php
class Customer {
    public $nic;
    public $firstName;
    public $lastName;

    function Customer($nic="", $firstName="", $lastName=""){
        $this->nic = $nic;
        $this->firstName = $firstName;
        $this->lastName = $lastName;
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

class VerificationResponse {
    public $genuine;
    public $belongsTo;

    function VerificationResponse($genuine=true, $NIC="", $firstName="", $lastName=""){
        $this->genuine = $genuine;
        $this->belongsTo = new Customer($NIC, $firstName, $lastName);
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

class VerificationRequest {
    public $customerId;

    /**
     * SignatureImage
     */
    public $questionedSignature;

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
    $filename = "log.json";
    $file = fopen( $filename, "w" );

    if( $file ) {
        fwrite( $file,  $_POST["payload"]);
        fclose( $file );
        
        shell_exec("./verify.py");
    }
    
    $response = new VerificationResponse(false, "7860123456789", "Test", "User");
    header("Content-type", "text/json");
    echo json_encode($response->getJsonData());
}
?>