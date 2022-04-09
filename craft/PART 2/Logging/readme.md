# Logging

코드에 로깅 호출을 추가하여 소프트웨어가 실행될 때 발생하는 이벤트를 추적하는 수단이다.

# Log Level

- DEBUG
  - 상세한 정보
  - 보통 문제를 진단할 때만 필요함.
- INFO
  - 작업이 정상적으로 작동하고 있다는 확인 메시지
- WARNING
  - 예상하지 못한 문제나 발생 가능한 문제점을 명시
- ERROR
  - 프로그램이 함수를 실행하지 못할 정도의 심각한 문제
- CRITICAL
  - 프로그램이 동작할 수 없을 정도의 심각한 문제


# 구현

파이썬에서 기본으로 제공되는 logging 라이브러리르 사용하였다.

## formatters

formatter를 통해 출력할 log의 format을 지정한다.

'%(asctime)s [%(levelname)s] %(name)s: %(message)s'를 적용하여 시간과 log level, 이름, 메시지를 출력하였다.

## handlers

로그의 출력 방법을 정의한다.
 
쿼리를 통해 생긴 로그를 별도의 파일에 저장할 예정이다.  
파일 경로와 인코딩 방식, 최대 크기 등을 지정하였다.

## loggers

query logger를 만들어서 query를 수행하는 중 Exception이 발생하는 지점에 적용하였다.