# Lab 10 - HTTP Status Codes, Headers and Caches

This exercise provides basic overview of HTTP Headers and local caching of contents by a web browser.

## Learning Objectives

- Understand HTTP Status Codes.
- Understand use of HTTP Status codes and Headers in rendering of a web page.
- Understand use of Cache by a web browser.
- Understand use of HTTP Status codes associated with Cacheing.

## Environment 

Docker Desktop, which is an application environment for your laptop environment that enables running of containerized applications. The Docker Desktop integrates and provides access to a vast ecosystem of docker images via Docker Hub. To access web content, use of Firefox browser is recommended as it provides easier support to dissect and analyse web request and response

Currently, most computers use either ARM based CPU (such as Apple Macbook using Sillicon chip M1/M2/M3/M4) or Windows based laptop using Intel x86 based CPU. An image created for arm architecture is unlikely to run on x86 based systems and vice versa. Nevertheless, the image for this exercise is designed to work in both. 

***For all of the exercise we will do based on a docker environment we will use pre-built images. When the image does not work. Build the image using the docker file in util folder. as follows:***

- docker build -f `<file-path>/<file-name>.df` -t `<image name>` .
  - E.g. `docker build -f ./util/df/net-ub22-host.df -t net-ub22-host .`
  
## Description

> Creating, running and verifying the web server
- Creating a Local Web server Instance
- We will customized docker images to create a web server instance.
  - `$ docker run -it -d --name web -p 80:80 --rm zizutg/net-ub22-host`
- Note: if this doesn't work we build the image 


- Start the web server in the docker instance of web server.
  - In the terminal window of your laptop, enter the following command
  - `$ docker exec -it web apache2ctl start`

Verify that web server is up and running and serving web pages. 
- Run the following command on host (laptop) terminal.
  - `$ curl http://localhost/welcome.html`

```html
<html>
    <head>
        <title>Welcome Page<title>
    <head>
    <body>
        <h1>Welcome to HTTP Learning<h1>
        Welcome to experiential learning of HTTP protocol.
    <body>
<html>
```

## Status Codes

In the firefox/Chrome browser, open the "Web Developer Tools" window.

Enter any URL, e.g., <http://localhost/welcome.html> in the window, click on the URL in developer tools under the Network tab, and analyze the status codes in the HTTP response.

> Status code 200
- Access any web page successfully, analyze the status code, and It should be 200.

> Status code 301/302

- In the command terminal (laptop/host), use the following command
  - `$ curl -I http://google.com`
- Analyze the response header and status codes to be either 301 (or 302). The new URL is provided in the Response Header "Location:". A browser automatically makes a new request with the new URL to fetch the content. 
- Use the option "-L" in curl to see automatically fetching the new URL with the status code of 200.
  - `$ curl -I -L http://google.com`

> Status code 304

- Enter the URL <http://localhost/img/img-01.jpg> in the firefox browser. 
  - It should display a simple image box containing letters "Image 01". 
  - Refresh the web page few times, and analyze the status code in Web Developer Tools.
  - It will display the status code 304.

- This happens as the image is cached by the browser. 
  - Remove the Firefox Cache by clearing its history, i.e.,
    -  `Menu > History > Clear Recent History` 
    -  Select/check "`Temporary Cache Files and Pages`"  and refresh the web page. 
  - The status code will show 200. 
    - Refresh again and status code will be 304 as the image is already cached.

> Status code 400

- Access web 
- Make any HTTP request with incorrect formatting.
- `curl -I -H 'Host: a\ncom' http://localhost/welcome.html`

> Status code 401
- Access the web server via bash
  - `docker exec -it web bash`
- Specify a directory in webserver root e.g. /var/www/html/private to be protected by password.
  - Create a password directory, file and the actual password
    - `sudo mkdir -p /var/www/passwords`
    - `sudo htpasswd -c /var/www/passwords/password.file student`
    - When prompted for password type `dps_repo` 
    - ***You may not need sudo as you are root***
- Specify this directory in Apache configuration /etc/apache2/apache2.conf as follows
    ```
    <Directory /var/www/html/private>
        AllowOverride all
    </Directory>
    ```

- In this directory create a file .htaccess with following contents
    ```
    AuthType Basic
    AuthName "Password Required"
    AuthUserFile "/var/www/passwords/password.file"
    Require valid-user
    ```

- Restart the Apache web server (your laptop terminal window)
  - `$ docker exec -it web apache2ctl restart.`
  - Or just `apache2ctl restart` if you are inside the host

- Now access any web resource (HTML file) in this /private directory and web server will response with status code 401. 
  - For example, user the URL <http://localhost/private/personal.html> and browser will pop up the authorization windows. 
  - Access this url using curl and it will give respond with status code 401.
  - `$ curl -I http://localhost/private/personal.html`

> Status code 403
- Enter the URL http://websitea.local/noperm.html in the browser and its status code should be 403.

> Status code 404
- Enter the URL http://websitea.local/xyz.html and its status code should be 404.

> Status code 500

- Enter the following URLs <http://localhost/cgi-bin/goodcgi.py>. 
  - This should display the web page properly.

- Enter the following URLs <http://localhost/cgi-bin/badcgi.py>. 
  - This URL should give status code 500 and its content should display Internal Server Error. 
  - Analyze the good and bad behaviour by studying and analyzing these programs in the directory /usr/lib/cgi-bin in the docker instance.

## HTTP Cache

#### Enable headers in Apache Config

Configure Apache webserver to serve specific headers via apache directives. 
- Access the docker instance and run the following command
    - $ docker exec -it web bash
- Inside the web host write the following commands

    - `$ a2enmod headers`
    - `$ apache2ctl restart`
    - You can leave it for other tasks or `$ exit`

#### Configuring Apache with Cache-Control directives

Update Apache configuration file `/etc/apache2/apache2.conf` with directives to set cache-control headers for 3 or more files e.g., image files (`img/img-<n>.jpg`). 
- Set the cache-control headers separately for each of these 3+ files/directories.

    - File *img-06.jpg*; Max-age=60.
    - File *img-07.jpg*; No-store.
    - File *img-08.jpg*; No-cache.

- For example, add the following lines at the end of `/etc/apache2/apache2.conf` file.
    ```
    <Directory /var/www/html/img>
        <Files "img-06.jpg">
            Header set Cache-Control "public, max-age=30"
        </Files>
        <Files "img-07.jpg">
            Header set Cache-Control "public, no-store"
        </Files>
        <Files "img-08.jpg">
            Header set Cache-Control "public, no-cache"
        </Files>
    </Directory>
    ```
- Restart Apache web server so that these directive take effect.
  - `$ apache2ctl restart`

#### Accessing Images with Cache-Control headers

Study and analyze the role of Response Header Cache-Control (Web Developer Tools window) by accessing these image URLs as below

- Access this URL <http://localhost/img/img-06.jpg> in your browser (Firefox). 
  - File should be served with status code 200 (check HTTP headers in web develop console of browser). 
  - Access this web again within less than 60 seconds, then it should make use of appropriate headers and status code should be 304.

- Access this URL <http://localhost/img/img-07.jpg> in your browser (Firefox). 
  - This should be returned with status code 200. 
  - Refresh few times and each time web server should respond with status code 200 since this web page will not be cached.

- Access this URL <http://localhost/img/img-08.jpg> in your browser (Firefox). 
  - Then access it again. 
  - Explore the HTTP request header especially `If-Modified-Since` and study its roles in serving web pages.

#### HTTP Cache Request Headers

Study the vulnerability of `If-Modified-Since` request header and why `Etag` is a better choice. 
- Consider a file `img-<n>.jpg` with modified date as $DATE1. 
  - Copy image 8 as image 88, access the web host via docker exec
    - `$ cd /var/www/html/img`
    - `$ cp img-08.jpg img-88.jpg`
  - Access image 88 in using curl from local terminal. 
    - `$curl -I http://localhost/img/img-88.jpg`
    ```
    HTTP/1.1 200 OK
    Date: Wed, 14 Jan 2026 21:07:31 GMT
    Server: Apache/2.4.58 (Ubuntu)
    Last-Modified: Wed, 14 Jan 2026 21:06:44 GMT
    ETag: "44ae-6485f7c4a2296"
    Accept-Ranges: bytes
    Content-Length: 17582
    Content-Type: image/jpeg
    ```
  - Save the date and Etag
    - `DATE1:  Wed, 14 Jan 2026 21:06:44 GMT`
    - `ETag: "44ae-6485f7c4a2296"`
  - Now copy another file with preserved time stamp onto image 88
    - `cp -p img-09.jpg img-88.jpg `
  - When accessing this file with header `If-Modified-Since`, show that server will return status code 304 even though file content has changed. 
    - The `date` should be the date we saved a moment ago
    - `curl -I -H "If-Modified-Since: Wed, 14 Jan 2026 21:06:44 GMT" http://localhost/img/img-88.jpg`
    ```
    HTTP/1.1 304 Not Modified
    Date: Wed, 14 Jan 2026 21:15:53 GMT
    Server: Apache/2.4.58 (Ubuntu)
    Last-Modified: Fri, 21 Nov 2025 16:47:19 GMT
    ETag: "3fae-6441d9113d3c0"
    Accept-Ranges: bytes
    ```
- Now demonstrate using the header `Etag` and `If-None-Match` and show that when file is changed, web server will respond with full file content using status code as 200 and not 304. 
- Use the curl command with -H option to specify appropriate headers.
  -  - The `Etag` should be the Etag we saved a moment ago
  - `curl -I -H 'If-None-Match: "44ae-6485f7c4a2296"' http://localhost/img/img-88.jpg`
    ```
    HTTP/1.1 200 OK
    Date: Wed, 14 Jan 2026 21:19:59 GMT
    Server: Apache/2.4.58 (Ubuntu)
    Last-Modified: Fri, 21 Nov 2025 16:47:19 GMT
    ETag: "3fae-6441d9113d3c0"
    Accept-Ranges: bytes
    Content-Length: 16302
    Content-Type: image/jpeg
    ```
 ***`curl is better for this demo. If you use a browser, it may not be able to capture it correctly`***



## Summary

In this exercise, we have learnt the following

- Use of HTTP status codes
- Browser behaviour in rendering the contents as per Status codes.
- Use of HTTP of status code 304
- Use of Headers HTTP headers used for caching by the browser.

## Learning Resources

### HTTP RFCs

-   RFC 7231 (obsoletes 2616) : HTTP 1/1
-   RFC 9110: HTTP Semantics

### Command line tools

-   curl: <https://curl.se/>
-   wget: <https://www.gnu.org/software/wget/manual/wget.html>

### Web Developer Tools in Briowser

-   Firefox: <https://firefox-source-docs.mozilla.org/devtools-user/>
-   Chrome: <https://developer.chrome.com/docs/devtools/open/>
