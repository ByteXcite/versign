<?php
/**
 * Created by PhpStorm.
 * User: saifkhichi96
 * Date: 27/05/2017
 * Time: 9:53 PM
 */
require_once(realpath(dirname(__FILE__))."/../bo/SessionManager.php");


class LoginController
{
    function login()
    {
        echo "\n\tLoginController::login() ... ";
        $username = $_POST["username"];
        $password = $_POST["password"];

        $auth = SessionManager::getInstance();
        $auth->startSession($username, $password);
        if ($auth->isSessionStarted()) {
            echo "SUCCESS.\n\tRedirecting now ...\n";
            header("Location: ../view/index.php");
        } else {
            echo "FAILURE.\n\tRedirecting now ...\n";
            header("Location: ../view/login.php");
        }
    }

    function logout()
    {
        echo "\n\tLoginController::logout() ... ";
        SessionManager::getInstance()->endSession();
        echo "DONE.\n\tRedirecting now...\n";
        header("Location: ../view/login.php");
    }
}