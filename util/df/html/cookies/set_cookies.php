<?php

// Normal cookie (default Lax in modern browsers)
setcookie("Ck_time", "Expiry Cookie", [
    "expires" => time() + 30
]);

// Lax cookie
setcookie("Ck_path", "Path Cookie", [
    "path" => "/path"
]);

// Strict cookie
setcookie("Ck_domain", "Domain Cookie", [
    "domain" => "xyz.myweb.local"
]);

// None cookie (requires Secure)
setcookie("Ck_secure", "Secure Cookie", [
    "HttpOnly" => true,
    "secure" => true
]);

echo "Following Cookies set!<p>";
echo "Ck_time = Expiry Cookie<p>";
echo "Ck_path = Path Cookie!<p>";
echo "Ck_domain = Domain Cookie!<p>";
echo "Ck_secure = Secure Cookie!<p>";
?>
