## NGINX config

* for hls port redirect

```
server{
      listen 88;
      server_name  localhost;
      
      root /tmp/; 
      index index.html
      autoindex off;
      
      location /hls/live/CH0/livetop.m3u8 {
	    alias /tmp/record/0.m3u8;
	    add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';

            if ($request_method = 'OPTIONS') {
               return 204;
            }
        }
```
