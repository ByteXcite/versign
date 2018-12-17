<?php
require_once(realpath(dirname(__FILE__)) . "/Parser.php");
require_once(realpath(dirname(__FILE__)) . "/../entity/VerificationRequest.php");
require_once(realpath(dirname(__FILE__)) . "/../entity/VerificationResponse.php");

if (isset($_POST["payload"])) {
    $payload = $_POST["payload"];
    try {
        $request = Parser::getTypedObject($payload, new VerificationRequest());
        $userExists = is_dir(realpath(dirname(__FILE__)) . "/verisign-core/db/users/" . $request->customerId);
        
        $response = new VerificationResponse();
        if (!$userExists) {
            $response->belongsTo = null;
        } else {
            // TODO: Fetch user details from database
            $response->belongsTo = new Customer();
            $response->belongsTo->id = $request->customerId;
            $response->belongsTo->firstName = "####";
            $response->belongsTo->lastName = "####";

            $filename = "verisign-core/bin/verify/request.json";
            $file = fopen($filename, "w");
            if($file) {
                fwrite($file, $payload);
                fclose($file);
        
                $python = "/anaconda2/bin/python";
                $action = "verisign-core/verify.py";
                $logfile = "verisign-core/bin/verify/log";
                $cmd = $python.' '.$action.' >& '.$logfile;
                system($cmd);

                $action = "verisign-core/src/verify.py";
                $f_user = "--user '" . $request->customerId . "'";
                $f_sign = "--sign verisign-core/bin/verify/" . $request->customerId . ".png";
                $cmd = $python.' '.$action.' '.$f_user.' '.$f_sign.' >& '.$logfile;
                system($cmd);
            }
        }

        // TODO: Read verification status from file (written by Python)
        $status = true;
        $response->genuine = $status;

        Parser::echoJsonData($response);
    }
    catch (ClassCastException $ex) {

    }
}
?>