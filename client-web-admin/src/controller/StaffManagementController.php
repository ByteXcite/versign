<?php
require_once(realpath(dirname(__FILE__))."/../dao/StaffDAO.php");

/**
 * Created by PhpStorm.
 * User: saifkhichi96
 * Date: 28/05/2017
 * Time: 3:44 AM
 */
class StaffManagementController
{
    /**
     * @var StaffDAO
     */
    private $staffDao;

    public function __construct()
    {
        $this->staffDao = new StaffDAO();
    }

    public function hire()
    {
        $staff = new Staff();
        $staff->setEmail($_POST["email"]);
        $this->staffDao->save($staff);
    }

    public function fire()
    {
        echo "Employee fired";
    }
}