## API Documentation

StockPilot provides RESTful endpoints for inventory management.

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /products | Retrieve all products |
| POST | /products | Add a product |
| GET | /products/{id} | Retrieve product details |
| GET | /inventory/low-stock | View low-stock products |
| PATCH | /inventory/{id}/restock | Restock a product |
| GET | /stats | View inventory statistics |
| GET | /health | Check application health |

Interactive API documentation is available through FastAPI Swagger UI at:

http://localhost:8000/docs