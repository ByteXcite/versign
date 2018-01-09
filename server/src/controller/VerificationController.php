<?php
require_once(realpath(dirname(__FILE__)) . "/Parser.php");
require_once(realpath(dirname(__FILE__)) . "/../entity/VerificationRequest.php");
require_once(realpath(dirname(__FILE__)) . "/../entity/VerificationResponse.php");

if (isset($_POST["payload"])) {
    $payload = $_POST["payload"];
    try {
        $request = Parser::getTypedObject($payload, new VerificationRequest());
        $userExists = is_dir(realpath(dirname(__FILE__)) . "/../../db/users/" . $request->customerId);
        
        $response = new VerificationResponse();
        if (!$userExists) {
            $response->belongsTo = null;
        } else {
            // TODO: Fetch user details from database
            $response->belongsTo = new Customer();
            $response->belongsTo->id = $request->customerId;
            $response->belongsTo->firstName = "####";
            $response->belongsTo->lastName = "####";

            $filename = "requests/verify/request.json";
            $file = fopen($filename, "w");
            if($file) {
                fwrite($file, $payload);
                fclose($file);
        
                $python = "/anaconda2/bin/python";
                $action = "requests/verify/process.py";
                $logfile = "requests/verify/log";
                $cmd = $python.' '.$action.' >& '.$logfile;
                system($cmd);

                $action = "../../lib/src/verify.py";
                $f_user = "--user " . $response->customerId;
                $f_sign = "--sign requests/verify/" . $response->customerId . ".png";
                $cmd = $python.' '.$action.' '.$f_user.' '.$f_sign;
                system($cmd);
            }
        }

        // TODO: Read verification status from file (written by Python)
        $status = false;
        $response->genuine = $status;

        Parser::echoJsonData($response);
    }
    catch (ClassCastException $ex) {

    }
}
?>