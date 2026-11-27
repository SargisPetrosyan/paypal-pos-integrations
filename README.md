# PayPal POS Integrations

Python components for receiving PayPal Point of Sale (formerly iZettle) webhook
events and supporting inventory integrations.

## Components

### `webhook_validator`

An AWS Lambda handler that accepts webhook events:

- **Subscription events:** validates the event as a webhook subscription. Active
  subscriptions have their signing key stored in Aurora DSQL and receive a
  success response. Inactive subscriptions are rejected.
- **Inventory balance events:** validates the event against the shared inventory
  schema, checks its `x-izettle-signature` HMAC-SHA256 signature using stored
  signing keys, then sends the event body as JSON to an SQS queue.

The Lambda entry point is `lambda_function.lambda_handler`.

### `shared`

Shared event schemas, constants, and other Python types used by the integration
components.

### `inventory-manual-changes-worker`

Contains inventory database configuration, models, and repository code. The
worker implementation is not yet complete; some repository methods are
placeholders.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- AWS access and permissions for the AWS resources used by the Lambda

## Local setup

Install the webhook validator dependencies:

```bash
cd webhook_validator
uv sync --locked --all-extras --dev
```

For local execution, provide the following environment variables. You can put
them in a `webhook_validator/.env` file when running commands from that
directory, or configure them in your shell or deployment environment.

| Variable | Purpose |
| --- | --- |
| `DSQL_DB_CLUSTER` | Aurora DSQL cluster identifier used to construct the database host |
| `DSQL_ZONE` | AWS region for the Aurora DSQL cluster |
| `DSQL_USER` | Database user for the webhook validator |
| `INVENTORY_EVENT_QUEUE_URL` | SQS queue URL for validated inventory events |

Do not commit credentials or secrets. Configure AWS credentials and permissions
using your environment's normal AWS credential mechanism.

## Tests and formatting

Run the webhook validator tests from the `webhook_validator` directory:

```bash
uv run pytest
```

Format Python files with Ruff:

```bash
uv run ruff format
```

Check formatting without modifying files:

```bash
uv run ruff format --check
```

The GitHub Actions workflow in `.github/workflows/main.yml` installs the project,
runs Ruff formatting, and runs the tests for pushes and pull requests targeting
`main`.

## Webhook event schemas

The validator accepts either a `WebhookSubscription` or an
`InventoryBalanceUpdateValidator` body. The subscription schema is defined in
`webhook_validator/models.py`; the inventory event schema is defined in
`shared/inventory_models.py`. The shared Pydantic schema configuration accepts
camelCase API fields as well as Python-style field names.
