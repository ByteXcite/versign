<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Login | VerSign</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
    <link rel="stylesheet" href="styles/custom.css">
</head>

<body>

<div class="login">
    <h1>Login</h1>
    <form method="post" action="../controller/route.php?controller=LoginController&action=login">
        <input type="text" name="username" placeholder="Username" required="required"/>
        <input type="password" name="password" placeholder="Password" required="required"/>
        <button class="btn btn-primary btn-block btn-large" type="submit">Login</button>
    </form>
</div>

</body>
</html>
