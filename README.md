# WhatsApp AI Bot with FastAPI, Gemini, and CrewAI

This project implements a WhatsApp bot that uses Google's Gemini AI and CrewAI to process messages and provide intelligent responses. It includes product recommendations and customer support features.

## Features

- WhatsApp message webhook endpoint
- Text and audio message processing (audio TBD)
- Product catalog with search capabilities
- AI-powered responses using Gemini Pro
- Intelligent agent system using CrewAI

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
GOOGLE_API_KEY=your_gemini_api_key
```

3. Run the application:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

- `POST /webhook`: Receives WhatsApp messages
- `GET /products`: Lists all products
- `GET /products/{product_id}`: Get specific product details
- `POST /query-products`: Search products using natural language

## Testing

You can test the API endpoints using curl or any API testing tool like Postman. Example:

```bash
# Get all products
curl http://localhost:8000/products

# Query products
curl -X POST http://localhost:8000/query-products \
  -H "Content-Type: application/json" \
  -d '{"query": "smartphone", "user_id": "123"}'
```

## WhatsApp Integration

Currently, the WhatsApp integration is mocked. To integrate with WhatsApp Business API:

1. Set up a WhatsApp Business account
2. Configure the webhook URL in WhatsApp Business API
3. Update the webhook handler in the code with actual WhatsApp API calls

## Note

This is a development version with mock data. For production use:

- Implement proper database storage
- Add authentication and security measures
- Set up proper error handling and logging
- Configure WhatsApp Business API integration 