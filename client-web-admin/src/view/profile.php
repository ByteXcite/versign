<?php
/**
 * Created by PhpStorm.
 * User: saifkhichi96
 * Date: 27/05/2017
 * Time: 10:00 PM
 */
ob_start();
session_start();

require_once(realpath(dirname(__FILE__))."/../bo/SessionManager.php");
if (!SessionManager::getInstance()->isSessionStarted()) {
    header("Location: ../login.php");
    die();
}

$user = unserialize($_SESSION["user"]);
?>
<!DOCTYPE html>
<html>
<head>
    <link href="/vendor/fontawhttps://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles/custom.css">
    <link rel="stylesheet" href="styles/profile.css"/>
    <link rel="stylesheet" href="/vendor/twbs/bootstrap/dist/css/bootstrap.min.css"/>
    <title>Profile | VerSign</title>
</head>
<body>
<!-- Navbar -->
<nav class="navbar navbar-inverse">
    <div class="container-fluid">
        <div class="navbar-header">
            <a class="navbar-brand" href="index.php">VerSign</a>
        </div>
        <ul class="nav navbar-nav">
            <li><a href="index.php">Home</a></li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
            <li><a href="profile.php"><? echo "Welcome, ".$user->getFirstName(); ?>
            <li class="active"><a href="profile.php"><span class="glyphicon glyphicon-user"></span> Profile</a></li>
            <li><a href="../controller/route.php?controller=LoginController&action=logout">
                    <span class="glyphicon glyphicon-log-out"></span> Logout</a></li>
        </ul>
    </div>
</nav>
<br>
<!-- /Navbar -->

<!-- page content -->
<div class="container">
    <div class="row">

        <!-- Sidebar -->
        <div class="col-sm-3">
            <a href="#" class="btn btn-danger btn-block btn-compose-email">Compose Email</a>
            <ul class="nav nav-pills nav-stacked nav-email shadow mb-20">
                <li class="active">
                    <a href="#">
                        <i class="fa fa-inbox"></i> Inbox <span class="label pull-right">7</span>
                    </a>
                </li>
                <li>
                    <a href="#"><i class="fa fa-envelope-o"></i> Send Mail</a>
                </li>
                <li>
                    <a href="#"><i class="fa fa-certificate"></i> Important</a>
                </li>
                <li>
                    <a href="#">
                        <i class="fa fa-file-text-o"></i> Drafts <span
                            class="label label-info pull-right inbox-notification">35</span>
                    </a>
                </li>
                <li><a href="#"> <i class="fa fa-trash-o"></i> Trash</a></li>
            </ul><!-- /.nav -->

            <h5 class="nav-email-subtitle">More</h5>
            <ul class="nav nav-pills nav-stacked nav-email mb-20 rounded shadow">
                <li>
                    <a href="#">
                        <i class="fa fa-folder-open"></i> Promotions <span
                            class="label label-danger pull-right">3</span>
                    </a>
                </li>
                <li>
                    <a href="#">
                        <i class="fa fa-folder-open"></i> Job list
                    </a>
                </li>
                <li>
                    <a href="#">
                        <i class="fa fa-folder-open"></i> Backup
                    </a>
                </li>
            </ul>
        </div>
        <!-- /Sidebar -->

        <!-- Profile Content -->
        <div class="col-sm-9">
            <div class="panel panel-default">
                <div class="panel-heading resume-heading">
                    <div class="row">
                        <div class="col-lg-12">
                            <div class="col-xs-12 col-sm-4">
                                <figure>
                                    <img class="img-circle img-responsive" alt="" src="http://placehold.it/300x300">
                                </figure>
                            </div>
                            <div class="col-xs-12 col-sm-8">
                                <ul class="list-group">
                                    <li class="list-group-item"><? echo strtoupper($user->getFirstName()); ?></li>
                                    <li class="list-group-item"><? echo strtoupper($user->getLastName()); ?></li>
                                    <li class="list-group-item"><? echo "@".$user->getUsername(); ?></li>
                                    <li class="list-group-item"><i class="fa fa-phone"></i><? echo $user->getNIC(); ?></li>
                                    <li class="list-group-item"><i class="fa fa-envelope"></i> <? echo $user->getEmail(); ?></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bs-callout bs-callout-danger">
                    <h4>Bank Information</h4>
                    <ul class="list-group">
                        <li class="list-group-item row">
                            <em class="col-sm-3 col-xs-3">ACCOUNT #</em>
                            <strong class="col-sm-9 col-xs-3">
                                123456789
                            </strong>
                        </li>
                        <li class="list-group-item row">
                            <em class="col-sm-3 col-xs-3">ACCOUNT TITLE</em>
                            <strong class="col-sm-9 col-xs-3">
                                ABRACADABRA
                            </strong>
                        </li>
                        <li class="list-group-item row">
                            <em class="col-sm-3 col-xs-3">BRANCH NAME</em>
                            <strong class="col-sm-9 col-xs-3">
                                DISNEYLAND
                            </strong>
                        </li>
                        <li class="list-group-item row">
                            <em class="col-sm-3 col-xs-3">DATE OPENED ON</em>
                            <strong class="col-sm-9 col-xs-3">
                                9/11
                            </strong>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <!-- /Profile Content -->
    </div>
</div>

<script src="/vendor/components/jquery/jquery.min.js"></script>
<script src="/vendor/twbs/bootstrap/dist/js/bootstrap.min.js"></script>
</body>
</html>