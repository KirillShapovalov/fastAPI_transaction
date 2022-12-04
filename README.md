docker-compose up --build

http://0.0.0.0:8008/docs

POST /transaction

test data:

[
  {
    "user_id": 1,
    "balance_dif": 200
  },
{
    "user_id": 2,
    "balance_dif": -510
  },
{
    "user_id": 3,
    "balance_dif": -1200.5
  }
]