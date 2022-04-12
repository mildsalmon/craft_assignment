# TLS

평문으로 전송되는 HTTP에 암호화를 적용한 방식이 HTTPS이다.

TLS를 위해서는 공개키 암호화 방식과 대칭키 암호화 방식을 모두 사용한다.  
최초에 server와 client가 대칭키를 주고받기 위해서 공개키 암호화 방식을 사용한다.  
그리고 전달받은 대칭키를 통해 서로 통신한다.  

## A. SSL 인증서 전달 방식

1. client가 server에 접속하여 아래 정보를 전달한다.
   - [클라이언트에서 생성한 랜덤 데이터, 클라이언트가 지원하는 암호화 방식, 세션 아이디]
2. server가 client에 아래 내용을 응답한다.
   - [서버 측에서 생성한 랜덤 데이터, 서버가 선택한 클라이언트의 암호화 방식, 인증서]
   - SSL 인증서의 내용으로는 [서비스의 정보 (인증서를 발급한 CA, 서비스의 도메인 등), 서버 측 공개키 (공개키의 내용, 공개키의 암호화 방법)]이 포함되어 있다.
   - SSL 인증서는 CA 개인키로 암호화한다.
3. client는 server의 인증서가 CA에 의해 발급된 것인지 확인한다.
   - CA는 신뢰성이 엄격하게 공인된 기업들만 참여할 수 있다.
   - 브라우저는 내부적으로 CA 리스트를 미리 파악하고 있다.
     - CA의 리스트와 CA의 공개키를 브라우저는 미리 알고 있다.
       - CA의 공개키로 인증서를 복호화하여 서버의 공개키를 얻는다.
4. client는 랜덤 데이터를 조합한다.
   - server가 전송한 랜덤 데이터와 client가 생성한 랜덤 데이터를 조합하여 pre master secret 키를 생성한다.
   - pre master secret 키는 대칭키 암호화 방식에 사용된다.
5. client는 pre master secret 키를 서버의 공개키로 암호화하여 server로 전송한다.
6. server는 client가 전송한 내용을 서버의 개인키로 복호화하여 pre master secret 키를 얻는다.
   - 이 과정에서 pre master secret은 master secret 값이 된다.
   - master secret은 session key를 생성하고 server와 client는 데이터를 대칭키 방식으로 암호화 한 후 주고 받는다.

![](/img/TLS1.png)

# 구현

무료로 SSL 인증서를 발급해주는 Let's Encrypt 서비스를 이용하였다.  
도메인은 freenom을 사용하였다.  (https://mildsalmon.tk/)

## A. Certbot 설치

```
# 레포지토리 추가
sudo add-apt-repository ppa:certbot/certbot

# Certbot Nginx 패키지 설치
sudo apt install python-certbot-nginx
```

## B. SSL 인증서 발급

```
sudo certbot --nginx -d mildsalmon.tk
```

```
# SSL 인증서 자동 갱신
sudo certbot renew --dry-run
```

## C. Nginx 설정 수정

```
server {
        listen 80;
        server_name mildsalmon.tk;
        rewrite         ^ https://$server_name$request_uri? permanent;

}

server {
        listen 443;
        server_name mildsalmon.tk;

        ssl on;
        ssl_certificate /etc/letsencrypt/live/mildsalmon.tk/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/mildsalmon.tk/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static {
                alias /home/ubuntu/craft_assignment/craft/static;
        }

        location / {
                include proxy_params;
                proxy_pass http://unix:/tmp/gunicorn.sock;

                proxy_buffer_size       128k;
                proxy_buffers           4 256k;
                proxy_busy_buffers_size 256k;
        }
}
```

```
# nginx 설정 파일에 오류가 있는지 확인
sudo nginx -t

# nginx 재시작
sudo systemctl restart nginx
```

## D. Django runserver

```
python3 manage.py runserver 0:8000 --certificate /etc/letsencrypt/live/mildsalmon.tk/fullchain.pem --key /etc/letsencrypt/ypt/live/mildsalmon.tk/privkey.pem
```

# 완성

![](/img/6.png)