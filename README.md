# Campaign CMS Clone

An enterprise-style Campaign CMS built using **FastAPI**, **MongoDB**, **JWT Authentication**, and **Docker**.

This project recreates the complete reward lifecycle used in real-world rewards and loyalty platforms, including campaign management, wallet management, order processing, transaction auditing, refund workflows, authentication, and containerization.

---

# Project Objective

Build a Campaign CMS capable of:

- Managing Clients
- Managing Accounts
- Managing Products
- Managing Campaigns
- Campaign Product Mapping
- Claim Code Upload
- Wallet Generation
- Order Creation
- Order Lifecycle Management
- Wallet Transactions
- Refund Processing
- JWT Authentication
- Dockerized Deployment

---

# Complete System Architecture

```text
User
   ↓
JWT Authentication
   ↓

Client
   ↓
Account
   ↓
Product
   ↓
Campaign
   ↓
Campaign Product Mapping
   ↓
Claim Codes
   ↓
Wallets
   ↓
Wallet Transactions
   ↓
Orders
   ↓
Order Status Workflow
   ↓
Refund Workflow
```

---

# Technology Stack

## Backend

- FastAPI
- Pydantic
- Uvicorn

## Database

- MongoDB
- Motor

## Security

- JWT Authentication
- python-jose
- passlib
- bcrypt

## DevOps

- Docker
- Docker Compose

## Data Processing

- Pandas

---

# Project Structure

```text
campaign-cms-clone/

├── api/
│
│   ├── auth/
│   │   ├── app.py
│   │   ├── schema.py
│   │   └── utility.py
│   │
│   ├── clients/
│   ├── accounts/
│   ├── products/
│   ├── campaigns/
│   ├── claim_codes/
│   ├── wallets/
│   ├── wallet_transactions/
│   └── orders/
│
├── core/
│   └── security.py
│
├── db/
│   ├── config.py
│   └── connection.py
│
├── uploads/
│   └── csv/
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

# MongoDB Collections

```python
clients
accounts
products
campaigns
campaign_products_link
claim_codes
wallets
wallet_transactions
orders
users
```

---

# Environment Variables

Create `.env`

```env
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=campaign_cms
```

---

# Installation

## Create Virtual Environment

```bash
python3 -m venv venv
```

---

## Activate Environment

Linux / Mac

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Locally

```bash
uvicorn main:app --reload
```

Swagger:

```text
http://localhost:8000/docs
```

---

# Docker Support

The application is fully containerized.

## Dockerfile

The application is packaged into a Docker container running FastAPI.

---

## Docker Compose

The FastAPI application runs inside Docker while connecting to the existing MongoDB instance.

### docker-compose.yml

```yaml
services:

  app:
    build: .

    container_name: campaign_cms_app

    ports:
      - "8000:8000"

    extra_hosts:
      - "host.docker.internal:host-gateway"

    environment:
      MONGO_URL: mongodb://host.docker.internal:27017
      DATABASE_NAME: campaign_cms
```

---

## Build Docker Image

```bash
docker compose build
```

---

## Run Container

```bash
docker compose up
```

---

## Stop Container

```bash
docker compose down
```

---

## Swagger

```text
http://localhost:8000/docs
```

---

# Complete Business Flow

```text
Client
   ↓
Account
   ↓
Product
   ↓
Campaign
   ↓
Campaign Product Mapping
   ↓
Claim Code Upload
   ↓
Wallet Generation
   ↓
Order Creation
   ↓
Wallet Deduction
   ↓
Wallet Transaction
   ↓
Order Status Workflow
   ↓
Refund Processing
```

---

# Phase 1 - Foundation

Completed:

- FastAPI Setup
- MongoDB Setup
- Environment Configuration
- Collection Configuration
- Health Endpoint

---

# Phase 2 - Client Module

Represents organizations using the platform.

Examples:

```text
Samsung India
HSBC
Citibank
MoneyMax
```

## APIs

```http
POST /clients

GET /clients

GET /clients/{client_id}

PUT /clients/{client_id}
```

---

# Phase 3 - Account Module

Relationship:

```text
Client
   ↓
Account
```

Example:

```text
Samsung India
      ↓
Samsung eStore
```

## APIs

```http
POST /accounts

GET /accounts

GET /accounts/{account_id}

GET /accounts/client/{client_id}

PUT /accounts/{account_id}
```

---

# Phase 4 - Product Module

Products represent redeemable rewards.

Examples:

```text
Amazon Gift Card ₹500

Flipkart Gift Card ₹1000

Myntra Voucher ₹750
```

## APIs

```http
POST /products

GET /products

GET /products/{product_id}

GET /products/account/{account_id}

PUT /products/{product_id}
```

---

# Phase 5 - Campaign Module

Campaigns represent reward programs.

Examples:

```text
Samsung Welcome Rewards 2026

Samsung Referral Campaign

Samsung Festive Rewards
```

## APIs

```http
POST /campaigns

GET /campaigns

GET /campaigns/{campaign_id}

PUT /campaigns/{campaign_id}
```

---

## Campaign Product Mapping

```http
POST /campaigns/{campaign_id}/products

GET /campaigns/{campaign_id}/products
```

---

# Phase 6 - Claim Code Module

Claim Codes represent reward allocations.

## APIs

```http
POST /claim-codes/upload/{campaign_id}

GET /claim-codes

GET /claim-codes/{claim_code_id}

GET /claim-codes/campaign/{campaign_id}
```

---

## CSV Format

```csv
claim_code,amount,email
SAM1001,5000,arjun@gmail.com
SAM1002,3000,priya@gmail.com
SAM1003,10000,vikram@gmail.com
```

---

## Features

- Campaign Validation
- CSV Validation
- Duplicate Validation
- Existing Claim Code Validation
- Positive Amount Validation

---

# Phase 7 - Wallet Module

Wallets store redeemable balances.

## APIs

```http
POST /wallets/generate/{campaign_id}

GET /wallets

GET /wallets/{wallet_id}

GET /wallets/claim-code/{claim_code}
```

---

## Wallet Example

```json
{
  "claim_code": "SAM1001",
  "total_balance": 5000,
  "available_balance": 5000,
  "consumed_balance": 0
}
```

---

# Phase 8 - Order Module

Orders represent redemptions.

## APIs

```http
POST /orders

GET /orders

GET /orders/{order_id}

GET /orders/claim-code/{claim_code}
```

---

## Features

- Product Validation
- Wallet Validation
- Balance Validation
- Wallet Deduction

---

# Phase 9 - Order Status Workflow

Supported statuses:

```text
pending
processing
completed
cancelled
failed
```

---

## Workflow

```text
pending
   ├── processing
   ├── cancelled
   └── failed

processing
   ├── completed
   └── failed

completed
   └── terminal

cancelled
   └── terminal

failed
   └── terminal
```

---

## APIs

```http
PATCH /orders/{order_id}/status

GET /orders/status/{status}
```

---

# Phase 10 - Wallet Transaction History

Introduced wallet auditing.

## Transaction Types

```text
debit
credit
```

## APIs

```http
GET /wallet-transactions

GET /wallet-transactions/{transaction_id}

GET /wallet-transactions/claim-code/{claim_code}
```

---

## Features

- Automatic Debit Transaction Creation
- Audit Trail
- Transaction History
- Redemption Tracking

---

# Phase 11 - Order Cancellation & Refund

Introduced wallet refund workflow.

## API

```http
POST /orders/{order_id}/cancel
```

---

## Workflow

```text
Order Created
      ↓
Wallet Deduction
      ↓
Debit Transaction

Cancel Order
      ↓
Wallet Refund
      ↓
Credit Transaction
      ↓
Status = Cancelled
```

---

## Features

- Wallet Refund
- Credit Transaction Logging
- Refund Auditing
- Double Refund Prevention

---

# Phase 12 - JWT Authentication

Introduced secure API access.

---

## Register

```http
POST /auth/register
```

Request:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

---

## Login

```http
POST /auth/login
```

Request:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:

```json
{
  "success": true,
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

---

## Security Features

- Password Hashing using bcrypt
- JWT Token Generation
- JWT Token Validation
- Protected Endpoints

---

## Protected APIs

Examples:

```http
POST /clients

POST /accounts

POST /products

POST /campaigns

POST /wallets/generate/{campaign_id}

POST /orders

PATCH /orders/{order_id}/status

POST /orders/{order_id}/cancel
```

Authentication Header:

```http
Authorization: Bearer <token>
```

---

# Phase 13 - Dockerization

Introduced application containerization.

## Features

✅ Dockerized FastAPI Application

✅ Docker Compose Support

✅ Environment Variable Injection

✅ Existing MongoDB Integration

✅ Consistent Run Environment

---

## Workflow

```text
Docker Container
        ↓
FastAPI
        ↓
Existing MongoDB
        ↓
MongoDB Compass
```

This allows newly created records to appear in the same MongoDB instance already used during local development.

---

# Current System Capabilities

```text
✅ JWT Authentication

✅ Client Management

✅ Account Management

✅ Product Management

✅ Campaign Management

✅ Campaign Product Mapping

✅ Claim Code Upload

✅ Wallet Generation

✅ Wallet Accounting

✅ Order Creation

✅ Order Status Workflow

✅ Wallet Transactions

✅ Refund Processing

✅ Dockerized Deployment
```

---

# Completed Phases

```text
✅ Phase 1  - Foundation

✅ Phase 2  - Client Module

✅ Phase 3  - Account Module

✅ Phase 4  - Product Module

✅ Phase 5  - Campaign Module

✅ Phase 6  - Claim Code Module

✅ Phase 7  - Wallet Module

✅ Phase 8  - Order Module

✅ Phase 9  - Order Status Workflow

✅ Phase 10 - Wallet Transaction History

✅ Phase 11 - Order Cancellation & Refund

✅ Phase 12 - JWT Authentication

✅ Phase 13 - Dockerization
```

---

# Next Phase

## Phase 14 - Pytest Testing Suite

Planned:

```text
Unit Tests

Integration Tests

API Tests

Authentication Tests

Order Workflow Tests

Refund Workflow Tests
```

---

# Final Outcome

The Campaign CMS now supports a complete enterprise reward lifecycle:

```text
Authentication
      ↓
Campaign Setup
      ↓
Claim Code Upload
      ↓
Wallet Generation
      ↓
Reward Redemption
      ↓
Wallet Accounting
      ↓
Order Lifecycle
      ↓
Transaction Auditing
      ↓
Refund Processing
      ↓
Dockerized Deployment
```

This project demonstrates backend architecture, authentication, wallet accounting, order management, transaction auditing, refunds, and containerized deployment using FastAPI and MongoDB.