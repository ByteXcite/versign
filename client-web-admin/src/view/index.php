<?php
/**
 * Created by PhpStorm.
 * User: saifkhichi96
 * Date: 28/05/2017
 * Time: 12:32 AM
 */
ob_start();
session_start();

require_once(realpath(dirname(__FILE__)) . "/../bo/SessionManager.php");
if (!SessionManager::getInstance()->isSessionStarted()) {
    header("Location: ../login.php");
    die();
}

$user = unserialize($_SESSION["user"]);
?>
<!DOCTYPE html>
<html>
<head>
    <!-- Bootstrap -->
    <link href="/vendor/twbs/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet"/>

    <!-- Font Awesome -->
    <link href="/vendor/fortawesome/font-awesome/css/font-awesome.min.css" rel="stylesheet">

    <!-- Datatables -->
    <link href="/vendor/datatables.net-bs/css/dataTables.bootstrap.min.css" rel="stylesheet">
    <link href="/vendor/datatables.net-buttons-bs/css/buttons.bootstrap.min.css" rel="stylesheet">
    <link href="/vendor/datatables.net-fixedheader-bs/css/fixedHeader.bootstrap.min.css" rel="stylesheet">
    <link href="/vendor/datatables.net-responsive-bs/css/responsive.bootstrap.min.css" rel="stylesheet">
    <link href="/vendor/datatables.net-scroller-bs/css/scroller.bootstrap.min.css" rel="stylesheet">

    <!-- Custom Styles -->
    <link rel="stylesheet" href="styles/custom.css"/>

    <title>Employees | VerSign</title>
</head>
<body>
<!-- Navbar -->
<nav class="navbar navbar-inverse">
    <div class="container-fluid">
        <div class="navbar-header">
            <a class="navbar-brand" href="index.php">VerSign</a>
        </div>
        <ul class="nav navbar-nav">
            <li class="active"><a href="index.php">Home</a></li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
            <li><a href="profile.php"><? echo "Welcome, " . $user->getFirstName(); ?>
            <li><a href="profile.php"><span class="glyphicon glyphicon-user"></span> Profile</a></li>
            <li><a href="../controller/route.php?controller=LoginController&action=logout">
                    <span class="glyphicon glyphicon-log-out"></span> Logout</a></li>
        </ul>
    </div>
</nav>
<br>
<!-- /Navbar -->

<!-- page content -->
<div class="scroll">
    <div class="container">
        <div class='x_panel col-sm-12 col-md-9 col-xs-12'>
            <div class='x_title'>
                <h3>Customers<br>
                    <small>Lists of bank accounts</small>
                </h3>
                <div class='clearfix'></div>
            </div>
            <div class='x_content'>
                <table id='datatable' class='table table-striped table-bordered'>
                    <thead>
                    <tr>
                        <th>Account #</th>
                        <th>Account Title</th>
                        <th>Branch</th>
                        <th>Customer Name</th>
                        <th>Customer Email</th>
                        <th>Opened On</th>
                    </tr>
                    </thead>
                    <tbody>
                    <?php
                    $dao = new StaffDAO();
                    $employees = $dao->getAll();
                    foreach ($employees as $emp) {
                        echo "
                        <tr>
                            <td>" . $emp->getNic() . "</td>
                            <td>" . $emp->getFirstName() . "</td>
                            <td>" . $emp->getLastName() . "</td>
                            <td>" . $emp->isAdmin() . "</td>
                            <td>" . $emp->getUsername() . "</td>
                            <td>" . $emp->getEmail() . "</td>
                        </tr>";
                    }
                    ?>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="x_panel col-sm-12 col-md-3 col-xs-12">
            <br><br><br>
            <div class='x_title'>
                <h3>Account Management</h3>
                <div class='clearfix'></div>
            </div>
            <div class="btn-group">
                <a href="customer_add.php">
                    <button class="btn-primary">Add Account</button>
                </a>
                <a href="?edit_customer">
                    <button class="btn-primary">Edit Account</button>
                </a>
                <a href="?remove_customer">
                    <button class="btn-primary">Remove Account</button>
                </a>
            </div>
        </div>
    </div>
    <br><br>
    <div class="container">
        <div class='x_panel col-sm-12 col-md-9 col-xs-12'>
            <div class='x_title'>
                <h3>Employees<br>
                    <small>Lists of employees of the bank</small>
                </h3>
                <div class='clearfix'></div>
            </div>
            <div class='x_content'>
                <table id='datatable' class='table table-striped table-bordered'>
                    <thead>
                    <tr>
                        <th>NIC</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Position</th>
                        <th>Username</th>
                        <th>Email</th>
                    </tr>
                    </thead>
                    <tbody>
                    <?php
                    $dao = new StaffDAO();
                    $employees = $dao->getAll();
                    foreach ($employees as $emp) {
                        echo "
                        <tr>
                            <td>" . $emp->getNic() . "</td>
                            <td>" . $emp->getFirstName() . "</td>
                            <td>" . $emp->getLastName() . "</td>
                            <td>" . $emp->isAdmin() . "</td>
                            <td>" . $emp->getUsername() . "</td>
                            <td>" . $emp->getEmail() . "</td>
                        </tr>";
                    }
                    ?>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="x_panel col-sm-12 col-md-3 col-xs-12">
            <br><br><br>
            <div class='x_title'>
                <h3>Employee Management</h3>
                <div class='clearfix'></div>
            </div>
            <div class="btn-group">
                <a href="employee_add.php">
                    <button class="btn-primary">Hire Employee</button>
                </a>
                <a href="?edit_employee">
                    <button class="btn-primary">Edit Employee</button>
                </a>
                <a href="?remove_employee">
                    <button class="btn-primary">Fire Employee</button>
                </a>
            </div>
        </div>
    </div>
</div>

<script src="/vendor/components/jquery/jquery.min.js"></script>
<script src="/vendor/twbs/bootstrap/dist/js/bootstrap.min.js"></script>

<!-- Datatables -->
<script src="/vendor/datatables.net/js/jquery.dataTables.min.js"></script>
<script src="/vendor/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>
<script src="/vendor/datatables.net-buttons/js/dataTables.buttons.min.js"></script>
<script src="/vendor/datatables.net-buttons-bs/js/buttons.bootstrap.min.js"></script>
<script src="/vendor/datatables.net-buttons/js/buttons.flash.min.js"></script>
<script src="/vendor/datatables.net-buttons/js/buttons.html5.min.js"></script>
<script src="/vendor/datatables.net-buttons/js/buttons.print.min.js"></script>
<script src="/vendor/datatables.net-fixedheader/js/dataTables.fixedHeader.min.js"></script>
<script src="/vendor/datatables.net-keytable/js/dataTables.keyTable.min.js"></script>
<script src="/vendor/datatables.net-responsive/js/dataTables.responsive.min.js"></script>
<script src="/vendor/datatables.net-responsive-bs/js/responsive.bootstrap.js"></script>
<script src="/vendor/datatables.net-scroller/js/dataTables.scroller.min.js"></script>
<script src="/vendor/jszip/dist/jszip.min.js"></script>
<script src="/vendor/pdfmake/build/pdfmake.min.js"></script>
<script src="/vendor/pdfmake/build/vfs_fonts.js"></script>

<!-- Custom Theme Scripts -->
<script src="scripts/custom.min.js"></script>
</body>
</html>
