docker build -t xss .
docker tag xss:latest gregxsunday/xssserver
docker push gregxsunday/xssserver