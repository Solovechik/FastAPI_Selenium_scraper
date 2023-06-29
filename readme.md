Launch with Docker-compose.
Access settings in .env file.

manager - port 8001
postgres - port 5433

Endpoints and examples:

curl --location 'http://127.0.0.1:8001/good/add/' \
--header 'Content-Type: application/json' \
--data '{
    "link": "https://www.mvideo.ru/products/split-sistema-haier-hsu-07hrm103-r3-20085322"
}

curl --location --request DELETE 'http://127.0.0.1:8001/good/delete/' \
--header 'Content-Type: application/json' \
--data '{
    "id": 4
}'

curl --location 'http://127.0.0.1:8001/good/list/'

curl --location --request GET 'http://127.0.0.1:8001/good/prices/' \
--header 'Content-Type: application/json' \
--data '{
    "id": 1
}'
