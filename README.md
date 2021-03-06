# craft_assignment

## Demo URL

[Craft assignment - mildsalmon.tk](https://mildsalmon.tk/)

시연 서버라서 DEBUG=True 상태를 수정하지 않았습니다.

서버는 AWS의 EC2에서 동작하고 있습니다.

## PART 1. SIMPLE BACKEND AUTH SERVER

> REST가 아닌 GraphQL을 사용하여야 함.

![](/img/1.png)

> e-mail과 password를 인자로 회원가입할 수 있음.
> 회원정보는 DB에 저장되며, password는 암호화 되어 저장 됨

![](/img/2.png)

> e-mail과 password를 인자로 로그인 할 수 있으며, 이는 json webtoken을 반환 함.

![](/img/3.png)

> 로그인 시, authorization header에 json webtoken이 이미 포함되어 있는 경우 주어진 json webtoken에 해당하는 email 값을 찾아 "이미 {email}로 로그인 하였습니다."라는 텍스트를 반환.

![](/img/4.png)


## PART2. AUGMENTED BACKEND AUTH SERVER

### a. Logging

[PART2. Logging](https://github.com/mildsalmon/craft_assignment/blob/main/craft/PART%202/Logging/readme.md)

### b. Health Checks

[PART2. Health Checks](https://github.com/mildsalmon/craft_assignment/blob/main/craft/PART%202/Health%20Checks/readme.md)

### c. TLS

[PART2. Logging TLS](https://github.com/mildsalmon/craft_assignment/blob/main/craft/PART%202/TLS/readme.md)

# python version

python 3.8

# library

django==2.2  
graphene==2.0.1  
graphene-django==2.0.0  
django-filter==1.1.0  
django-graphql-jwt==0.2.1  
PyJWT==1.7.0   
django-health-check==3.16.5  
django-sslserver==0.22  
gunicorn==20.1.0  
