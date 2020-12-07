/* /etc/ssh/ssh_config */

1. change port number  

```
#L13 uncomment
#Port 22
```

2. enable passwd/root login  

```
#L27 uncomment and change to yes
#PermitRootlogin yes
#PasswordAuthentication yes
```

3. Change date to avoid password expire  

```
$ date '2020-12-07'

$ vi /etc/login.defs
PASS_MAX_DAYS 99999
PASS_MIN_DAYS 0
```

4. Change root passward & add user  

```
$ passwd root
new passwd: <>
re type passwd: <>

$ usradd <user>
```  




