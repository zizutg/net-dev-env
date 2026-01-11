<?php
$ck1_name = "s_course";
$ck1_value = "Network";
$ck2_name = "__Secure-s_Subject";
$ck2_value = "Comp. Sc";
$ck3_name = "__Secure-s_Instructor";
$ck3_value = "Prof. Ram Rustagi";

$path = "/";
$domain = ".myweb.local";
$secure = true;
$httponly = true;

setcookie($ck1_name, $ck1_value, time() + (300)); 
setcookie($ck2_name, $ck2_value, time() + (300), $path, $domain, $secure);
setcookie($ck3_name, $ck3_value, time() + (86400));
?>

<html>
<body>
<?php
if (count($_COOKIE) > 0) {
  echo "Cookie values are:<br/>";
  foreach ($_COOKIE as $name => $value) {
    echo "<br/>Name= $name, Value= $value\n";
  } 
} else {
    echo "<br/>Cookies are not yet set";
}
?>
</body>
</html>
