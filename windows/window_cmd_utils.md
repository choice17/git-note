## window_cmd_utils  

* [netsh](#netsh)  
* [netstat](#netstat)  
* [route](#route)  


### netsh  

[referece](https://networking.ringofsaturn.com/PC/netsh.php)

1. netsh tool able to allow ip and port forward to another accessible network  

```bash
> netsh interface portproxy add v4tov4 listenport=40047 listenaddress=192.168.0.100 connectport=40047 connectaddress=192.168.5.100
```

2. setup static ip addr  

```
netsh interface ip set address name="Local Area Connection" static 192.168.0.100 255.255.255.0 192.168.0.1 1
```

3. setup dhcp 

```
netsh interface ip set address "Local Area Connection" dhcp
```


### netstat  

netstat is to check ip and port connection for tcp udp

```
> netstat -a
> netstat -b
```

## route  

route is to check router connection  

```
> route -n
```
