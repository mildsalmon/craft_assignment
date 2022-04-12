# Health Check

장비에 장애가 발생하였을 때 신속하게 교체하기 위해서 빠른 장애 탐지가 필요하다.

Health Check는 서버에 일정한 간격으로 신호를 보내고 응답이 오는지 체크하여 정상 가동 중인지를 판단한다.

# Health Check 종류

## 1. Layer 3 (ICMP)

ping 등으로 응답 확인

ICMP Echo Request 메시지를 전송한 후 ICMP Echo Reply 메시지 수신 여부에 따라서 서비스 서버의 서비스 가능 유무를 판단한다.

## 2. Layer 4 (Port)

웹 서비스인 경우, 80번 포트로 응답 확인

TCP 3 way handshake를 이용하여 서버의 서비스 포트로 SYN를 전송하고 SYN-ACK로 응답 유무에 따라서 서비스 서버의 서비스 가능 유무를 판단한다.

## 3. Layer 7 (HTTP)

HTTP 통신을 확인하는 경우, 특정 페이지가 제대로 표시되는지 확인

서버와 TCP 세션을 맺고 Request 메시지 전송을 통해 응답 코드를 확인한다.

# 구현

[django-health-check](https://github.com/KristianOellegaard/django-health-check) 라이브러리를 사용하였다. 

기존에 사용하던 django==2.0.2 버전과는 dependency 오류가 발생해서 django==2.2로 버전업을 시켜주었다.

이 라이브러리는 서버가 실행될 때 plugin_dir(HealthCheckPluginDirectory)의 self._registry에 각 app (cache, dp, storage, migration)에 작성된 CacheBackend, DatabaseBackend, StorageHealthCheck, MigrationsHealthCheck와 option이 append된다.

그리고 views.py의 MainView 클래스는 mixins.py의 CheckMixin 클래스를 상속하고 template의 {% for plugin in plugins %}로 plugins를 호출한다.

각 plugin은 BaseHealthCheckBackend를 상속하고 있어서 identifier와 status는 별도로 구현하지 않고 사용한다.  
check_status만 별도로 overriding한다.

## 각 app별 동작 방식

cache는 django.core.cache의 caches를 통해 특정 키워드('djangohealtcheck_test', 'itworks')를 set하고 get을 통해 일치하는지 확인한다.

db는 간단한 create와 delete를 통해 오류가 발생하는지 확인한다.

storage는 파일 하나를 만들고 문장을 입력하여 여분의 공간이 있는지 확인하고 파일을 삭제한다.

migration은 미해결된 migrations이 있는지를 확인한다.


# 완성

![](/img/7.png)