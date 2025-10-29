Запуск локально (с Docker):
  docker-compose up --build

Сервис поднимется на http://localhost:8000
OpenAPI: http://localhost:8000/docs

Примеры:
Добавить товар в заказ (POST):
  curl -X POST "http://localhost:8000/orders/1/items" -H "Content-Type: application/json" -d '{"product_id":1,"quantity":2}'

Примечание: при запуске впервые можно выполнить python -m app.seed для заполнения тестовых данных.