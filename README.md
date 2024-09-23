# mnist

## Docker

### Docker Image Build

```
docker build --platform <플랫폼 지정> --tag <도커 아이디>/<이미지 이름>:<버전> .
```

### Docker Run 방법

```
docker run -d --name mnist \
-e LINE_TOKEN=<라인에서 발급한 토큰> \
-e DB_IP=<데이터베이스 아이피> \
-e DB_PORT=<데이터베이스 포트> \
-p <fastapi 연결 할 포트>:8080 \
<도커 아이디>/<이미지 이름>:<버전>
```

### Docker Push

```
docker push <도커아이디>/<이미지명>:<버전>
```