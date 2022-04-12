# 순서도

웹 브라우저 -> 웹 서버 (Nginx) -> 동적 요청 ---Yes---> WSGI 서버 (Gunicorn) -> WSGI 어플리케이션 (django)
                                  └---No---> 

# Gunicorn을 이용하여 웹 접속

mildsalmon.tk:8000이 아닌 mildsalmon.tk로 접속할 수 있도록 WSGI(Gunicorn)와 Nginx를 연결해주었다.

웹 서버에 동적 요청이 발생하면 웹 서버가 WSGI 서버를 호출하고 WSGI 서버는 파이썬 프로그램을 호출하여 동적 페이지 요청을 대신 처리한다.

# 구현

/etc/systemd/system/craft.service 파일을 작성하고 데몬을 실행한다.

```
sudo systemctl daemon-reload
sudo systemctl start craft.service
```

AWS 서버가 재시작되더라도 Gunicorn이 자동 실행되도록 설정한다.

```
sudo systemctl enable craft.service
```

# 완성

![](/img/5.png)