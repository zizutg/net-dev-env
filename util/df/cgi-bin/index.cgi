#!/bin/bash 

echo 'Content-type: text/html' 
echo 
echo '<html> <body>' 
echo '<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">'  
echo 'CGI Bash Script Test Page'  
echo '</div>'  
echo '<p>'
echo 'This response is from web server: '
echo `hostname -I`
echo '</body> </html>'  


