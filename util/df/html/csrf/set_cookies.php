<?php
// csrf.bank.local/set_cookies.php

// Normal cookie (default Lax in modern browsers)
setcookie("Ck_bank_normal", "Normal Cookie", [
    "path" => "/",
    "samesite" => "",
]);

// Lax cookie
setcookie("Ck_bank_Lax", "Lax Cookie", [
    "path" => "/",
    "samesite" => "Lax",
]);

// Strict cookie
setcookie("Ck_bank_Strict", "Strict Cookie", [
    "path" => "/",
    "samesite" => "Strict",
]);

// None cookie (requires Secure)
setcookie("Ck_bank_none", "None Cookie", [
    "path" => "/",
    "domain" => "csrf.bank.local",
    "samesite" => "None",
    "HttpOnly" => true,
    "secure" => true
]);

echo "Following Cookies set!<p>";
echo "Ck_bank_normal = Normal Cookie<p>";
echo "Ck_bank_Lax = Lax Cookie!<p>";
echo "Ck_bank_Strict = Strict Cookie!<p>";
echo "Ck_bank_None = None Cookie!<p>";
?>
