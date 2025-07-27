# Entegrations

Entegrations is a Python library that provides easy-to-use integrations with various third-party services, including payment processors and large language models (LLMs).

## Features

- **Modular Design**: Install only what you need - full library or individual modules
- **Simplified APIs**: Consistent, well-documented interfaces for each integration
- **Error Handling**: Robust error handling with descriptive error messages
- **Testable**: Designed for easy mocking and testing
- **Detailed Playbooks**: Each integration includes a comprehensive implementation guide

## Available Modules

- **payments**: Integrations with payment processors
  - **stripe**: Stripe payment processing integration
    - Checkout API for creating payment sessions
    - Webhook validation
    - [Detailed Integration Playbook](emergentintegrations/payments/stripe/docs/stripe_integration_playbook.md)
- **llm**: Integrations with large language models
  - **openai**: LLM integration (using LiteLLM)
    - Chat API for generating completions with multiple providers
    - [Detailed Integration Playbook](emergentintegrations/llm/openai/docs/litellm_integration_playbook.md)

## Installation

### Full Package

```bash
pip install -e .
```

### Individual Modules

For just the payments module:
```bash
pip install -e ".[payments]"
```

For just the LLM module:
```bash
pip install -e ".[llm]"
```

Alternatively, you can install directly from the module-specific setup files:

```bash
# For payments module only
pip install -e . -f setup_payments.py

# For LLM module only
pip install -e . -f setup_llm.py
```

## Usage Examples

### Stripe Checkout

```python
from emergentintegrations.payments.stripe import StripeCheckout

# Initialize with your API key
checkout = StripeCheckout(
    api_key="your_stripe_api_key",
    webhook_secret="your_webhook_secret"  # Optional
)

# Create a checkout session
session = checkout.create_checkout_session(
    line_items=[
        {
            "price": "price_12345",
            "quantity": 1
        }
    ],
    success_url="https://example.com/success",
    cancel_url="https://example.com/cancel"
)

# Get the checkout URL
checkout_url = session["url"]

# Retrieve a session
session = checkout.retrieve_session("cs_test_12345")

# Verify a webhook
event = checkout.verify_webhook(
    payload=request.body,  # Raw body bytes
    signature=request.headers["Stripe-Signature"]
)
```

### LiteLLM Integration (via OpenAI module)

```python
from emergentintegrations.llm.openai import OpenAIChat

# Initialize with your API key and provider
chat = OpenAIChat(
    api_key="your_api_key",
    provider="openai"  # Can be "openai", "anthropic", "cohere", etc.
)

# Create a chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a joke about programming."}
]
response = chat.chat_completion(
    messages=messages,
    model="gpt-3.5-turbo",  # Model name specific to the provider
    temperature=0.7,
    max_tokens=150
)

# Extract the response text
text = chat.extract_response_text(response)
print(text)
```

## Documentation

Each integration module includes detailed documentation in its `docs` directory:

- Stripe Integration: [emergentintegrations/payments/stripe/docs/stripe_integration_playbook.md](emergentintegrations/payments/stripe/docs/stripe_integration_playbook.md)
- LiteLLM Integration: [emergentintegrations/llm/openai/docs/litellm_integration_playbook.md](emergentintegrations/llm/openai/docs/litellm_integration_playbook.md)

These playbooks provide comprehensive guides, including:
- Prerequisites and required credentials
- Installation instructions
- Code examples for both backend and frontend
- Advanced configurations
- Testing procedures
- Best practices
- Common issues and solutions

## Integration Testing

To run integration tests with real API keys:

```bash
# Run all integration tests
bash run_integration_tests.sh all

# Run just Stripe integration tests
bash run_integration_tests.sh stripe

# Run just LLM integration tests
bash run_integration_tests.sh llm
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/emergentintegrations.git
cd emergentintegrations

# Install development dependencies
pip install -e ".[all]"
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests for a specific module
pytest tests/payments/
pytest tests/llm/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.