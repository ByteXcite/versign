<?php
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