<?php

/**
 * Database is a Singleton class which provides interface to the application
 * with a MySQL database.
 *
 * @author saifkhichi96
 */
class Database
{
    private static $ourInstance = NULL;
    private $db_name = "versign";
    private $db_host = "localhost";
    private $db_user = "root";
    private $db_pwd = "root";

    /**
     * Database constructor. Private so that class cannot be instantiated externally.
     */
    private function __construct()
    {

    }

    /**
     * @return bool|mysqli
     */
    public static function getConnection()
    {
        if (self::$ourInstance == NULL) {
            self::$ourInstance = new Database();
        }

        return self::$ourInstance->connect();
    }

    /**
     * Opens a connection with MySQL database.
     *
     * @return bool|mysqli connection object or False on connection failure
     */
    private function connect()
    {
        $db_conn = mysqli_connect(
            $this->db_host,
            $this->db_user,
            $this->db_pwd,
            $this->db_name);

        return mysqli_connect_errno() != 0 ? False : $db_conn;
    }
}

?>