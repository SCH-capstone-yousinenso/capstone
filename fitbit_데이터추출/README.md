# FITBIT 데이터 추출 방법

## 1. Fitbit 계정 만들기 : https://www.fitbit.com/

## 2. https://dev.fitbit.com/ 들어간 후 상단 Manage -> Register An app 클릭

## 3. 빨간 표시 똑같이 할 것
> Oauth 2.0 Application Type은 personal 체크
> Callback URL:http://127.0.0.1:8080/
> 작성 후 submit

![image](https://user-images.githubusercontent.com/70958560/161204798-3c0e489b-61c0-4f95-9c4f-809e16f0af45.png)

## 4. 클라이언트 키와 시크릿 넘버 기억

![image](https://user-images.githubusercontent.com/70958560/161204878-38a7a585-ea49-4505-81a3-4c3be06c52a4.png)

## 5. `python-fitbit-master` 폴더 전부 다운로드

## 6. cmd or 아나콘다 명령 프롬프트 관리자 권한 실행 후 코드 실행
```
pip install –r requirements/base.txt 
```
