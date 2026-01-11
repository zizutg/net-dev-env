<?php
  $csp = "Content-Security-Policy: frame-ancestors *";
  header("$csp");
  echo "<h1>".$csp."</h1>";
?>
