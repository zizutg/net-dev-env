<?php
  $csp = "Content-Security-Policy: frame-ancestors 'self'";
  header("$csp");
  echo "<h1>".$csp."</h1>";
?>
