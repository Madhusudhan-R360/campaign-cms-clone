# Campaign CMS Clone

A production-style Campaign CMS built using **FastAPI**, **MongoDB**, **JWT Authentication**, **Docker**, and **Pytest**.

The project simulates a complete rewards and redemption platform used by enterprises to manage campaigns, claim codes, wallets, orders, transactions, and refunds.

---

# Project Objective

Build a backend system capable of managing:

- Clients
- Accounts
- Products
- Campaigns
- Claim Codes
- Wallets
- Orders
- Wallet Transactions
- Refunds
- JWT Authentication
- Dockerized Deployment
- Automated Testing

---

# Technology Stack

## Backend

- FastAPI
- Uvicorn
- Pydantic

## Database

- MongoDB
- Motor

## Authentication

- JWT
- python-jose
- passlib
- bcrypt

## Data Processing

- Pandas

## DevOps

- Docker
- Docker Compose

## Testing

- Pytest
- FastAPI TestClient

---

# System Architecture

```text
User
   |
   v
JWT Authentication
   |
   v
Client
   |
   v
Account
   |
   v
Product
   |
   v
Campaign
   |
   v
Claim Codes
   |
   v
Wallets
   |
   v
Orders
   |
   v
Wallet Transactions
   |
   v
Refund Workflow
```

---

# Project Structure

```text
campaign-cms-clone/

├── api/
│   ├── auth/
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
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_clients.py
│   └── test_health.py
│
├── uploads/
│
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .env
└── README.md
```

---

# Database Collections

```text
clients
accounts
products
campaigns
campaign_products_link
claim_codes
wallets
orders
order_items
wallet_transactions
users
```

---

# Environment Variables

Create a `.env` file:

```env
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=campaign_cms
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd campaign-cms-clone
```

## Create Virtual Environment

```bash
python3 -m venv venv
```

## Activate Virtual Environment

Linux / Mac

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

```bash
uvicorn main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

OpenAPI Schema:

```text
http://localhost:8000/openapi.json
```

---

# Docker Setup

The FastAPI application runs inside Docker and connects to the existing MongoDB instance.

## Docker Compose

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

## Build

```bash
docker compose build
```

## Start

```bash
docker compose up
```

## Stop

```bash
docker compose down
```

---

# Authentication

## Register User

### Endpoint

```http
POST /auth/register
```

### Request

```json
{
  "username": "admin",
  "password": "admin123"
}
```

### Response

```json
{
  "success": true,
  "message": "User registered"
}
```

---

## Login

### Endpoint

```http
POST /auth/login
```

### Request

```json
{
  "username": "admin",
  "password": "admin123"
}
```

### Response

```json
{
  "success": true,
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

---

## Authorization Header

```http
Authorization: Bearer <token>
```

---

# Client Module

Represents organizations using the platform.

Examples:

```text
Samsung India
Citibank
HSBC
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

# Account Module

Each Client can have multiple Accounts.

Example:

```text
Samsung India
   |
   +-- Samsung eStore
   |
   +-- Samsung Rewards
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

# Product Module

Represents redeemable rewards.

Examples:

```text
Amazon Gift Card

Flipkart Voucher

Myntra Coupon

Croma Gift Card
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

# Campaign Module

Campaigns contain products and claim codes.

Examples:

```text
Samsung Welcome Rewards

Samsung Festive Rewards

Referral Rewards Campaign
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

### APIs

```http
POST /campaigns/{campaign_id}/products

GET /campaigns/{campaign_id}/products
```

---

# Claim Code Module

Claim codes represent user reward allocations.

## Upload API

```http
POST /claim-codes/upload/{campaign_id}
```

## APIs

```http
GET /claim-codes

GET /claim-codes/{claim_code_id}

GET /claim-codes/campaign/{campaign_id}
```

---

## CSV Format

```csv
claim_code,amount,email

SAM1001,5000,john@gmail.com
SAM1002,2500,mary@gmail.com
SAM1003,10000,david@gmail.com
```

---

# Wallet Module

Wallets are generated from claim codes.

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

# Order Module

Orders represent reward redemptions.

## APIs

```http
POST /orders

GET /orders

GET /orders/{order_id}

GET /orders/claim-code/{claim_code}
```

---

## Order Flow

```text
Wallet
  |
  v
Order Created
  |
  v
Balance Deducted
  |
  v
Transaction Created
```

---

# Order Status Workflow

Supported statuses:

```text
pending
processing
completed
cancelled
failed
```

Workflow:

```text
pending
  |
  +--> processing
  |
  +--> cancelled
  |
  +--> failed

processing
  |
  +--> completed
  |
  +--> failed
```

---

## APIs

```http
PATCH /orders/{order_id}/status

GET /orders/status/{status}
```

---

# Wallet Transaction Module

Provides complete audit history.

Transaction Types:

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

# Refund Workflow

Allows cancelled orders to be refunded.

## API

```http
POST /orders/{order_id}/cancel
```

---

## Refund Flow

```text
Order Created
      |
      v
Balance Deduction
      |
      v
Debit Transaction
      |
      v
Order Cancelled
      |
      v
Wallet Refunded
      |
      v
Credit Transaction
```

---

# Security Features

✅ Password Hashing

✅ JWT Token Generation

✅ JWT Verification

✅ Protected Endpoints

✅ Unauthorized Access Prevention

---

# Testing

Implemented using:

```text
Pytest
FastAPI TestClient
```

## Current Tests

```text
test_auth.py

  ✓ Register User
  ✓ Login User

test_clients.py

  ✓ Create Client
  ✓ Authentication Protection

test_health.py

  ✓ OpenAPI Endpoint
```

---

## Run Tests

```bash
python -m pytest
```

Example:

```text
=====================
5 passed
=====================
```

---

# Completed Phases

```text
✅ Phase 1  - Project Foundation

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

✅ Phase 14 - Pytest Testing Suite
```

---

# Key Features

```text
✅ Client Management

✅ Account Management

✅ Product Management

✅ Campaign Management

✅ Campaign Product Mapping

✅ Claim Code Upload

✅ Wallet Creation

✅ Wallet Accounting

✅ Order Management

✅ Order Status Tracking

✅ Transaction Auditing

✅ Refund Processing

✅ JWT Authentication

✅ Docker Deployment

✅ Automated Testing
```

---

# Final Outcome

The Campaign CMS provides a complete reward management lifecycle:

```text
Authentication
     |
     v
Campaign Setup
     |
     v
Claim Code Upload
     |
     v
Wallet Generation
     |
     v
Reward Redemption
     |
     v
Wallet Transactions
     |
     v
Order Management
     |
     v
Refund Processing
     |
     v
Audit Tracking
     |
     v
Dockerized Deployment
     |
     v