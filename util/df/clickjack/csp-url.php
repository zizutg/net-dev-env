<?php
  $csp = "Content-Security-Policy: frame-ancestors cj.attacker.internal";;
  header("$csp");
  echo "<h1>".$csp."</h1>";
?>
