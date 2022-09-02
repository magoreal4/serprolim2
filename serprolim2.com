# /etc/nginx/sites-available/serprolim2

server {
    server_name test.limpiezapozossepticos.com www.test.limpiezapozossepticos.com;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
        }

    location /static/ {
        autoindex on;
        alias /root/serprolim2/staticfiles/;
        }
    
    location /media/ {
        autoindex on;
        alias /root/serprolim2/media/;
        }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/serprolim2.sock;
    }
}
