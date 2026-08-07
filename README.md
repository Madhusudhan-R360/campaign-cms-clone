# Campaign CMS Clone

An intermediate-to-advanced Campaign CMS built using **FastAPI**, **MongoDB**, and **JWT Authentication**.

This project recreates a complete enterprise-style reward lifecycle from campaign setup to reward redemption, transaction auditing, refund processing, and secure API access.

---

# Project Objective

Build a Campaign CMS capable of:

- Managing Clients
- Managing Accounts
- Managing Products
- Managing Campaigns
- Mapping Products to Campaigns
- Uploading Claim Codes
- Generating Wallets
- Creating Orders
- Tracking Order Lifecycle
- Tracking Wallet Transactions
- Supporting Refunds
- Securing APIs with JWT Authentication

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
- Passlib
- bcrypt
- python-jose

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

# Environment Configuration

## .env

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

# Requirements

```txt
fastapi
uvicorn
motor
pymongo
pandas
python-jose[cryptography]
passlib[bcrypt]==1.7.4
bcrypt==4.0.1
```

---

# Run Application

```bash
uvicorn main:app --reload
```

Swagger:

```text
http://localhost:8000/docs
```

---

# Business Flow

```text
Samsung India
      ↓
Samsung eStore
      ↓
Amazon Gift Card ₹500
      ↓
Samsung Welcome Rewards 2026
      ↓
SAM1001
      ↓
Wallet
      ↓
Order
      ↓
Transaction
      ↓
Refund
```

---

# Phase 1 - Foundation

Completed:

- FastAPI Setup
- MongoDB Configuration
- Environment Variables
- Collection Setup
- Health Endpoint

---

## Health API

```http
GET /health
```

---

# Phase 2 - Client Module

Represents organizations.

Examples:

```text
Samsung India
HSBC
Citibank
MoneyMax
```

---

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

---

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

---

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

Represents reward programs.

Examples:

```text
Samsung Welcome Rewards 2026

Samsung Referral Campaign

Samsung Festive Rewards
```

---

## APIs

```http
POST /campaigns

GET /campaigns

GET /campaigns/{campaign_id}

PUT /campaigns/{campaign_id}
```

---

## Campaign Product Mapping

### Link Product

```http
POST /campaigns/{campaign_id}/products
```

### Get Campaign Products

```http
GET /campaigns/{campaign_id}/products
```

---

# Phase 6 - Claim Code Module

Claim Codes store reward balance allocations.

---

## CSV Format

```csv
claim_code,amount,email
SAM1001,5000,arjun@gmail.com
SAM1002,3000,priya@gmail.com
SAM1003,10000,vikram@gmail.com
```

---

## APIs

```http
POST /claim-codes/upload/{campaign_id}

GET /claim-codes

GET /claim-codes/{claim_code_id}

GET /claim-codes/campaign/{campaign_id}
```

---

## Validations

- Campaign Validation
- CSV Header Validation
- Duplicate Claim Code Validation
- Existing Claim Code Validation
- Positive Amount Validation

---

# Phase 7 - Wallet Module

Wallets store spendable reward balance.

Relationship:

```text
Claim Code
      ↓
Wallet
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

## APIs

```http
POST /wallets/generate/{campaign_id}

GET /wallets

GET /wallets/{wallet_id}

GET /wallets/claim-code/{claim_code}
```

---

# Phase 8 - Order Module

Orders represent reward redemptions.

---

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

Introduced enterprise order lifecycle.

---

## Supported Statuses

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

Introduced transaction auditing.

Relationship:

```text
Wallet
      ↓
Wallet Transaction
```

---

## Transaction Types

```text
debit
credit
```

---

## Debit Example

```json
{
  "claim_code": "SAM1001",
  "transaction_type": "debit",
  "amount": 1000,
  "reference": "ORDER_123"
}
```

---

## APIs

```http
GET /wallet-transactions

GET /wallet-transactions/{transaction_id}

GET /wallet-transactions/claim-code/{claim_code}
```

---

## Features

- Automatic Debit Transaction Creation
- Wallet Audit Trail
- Transaction History
- Claim Code Lookup

---

# Phase 11 - Order Cancellation & Wallet Refund

Introduced wallet refund workflow.

Relationship:

```text
Order
   ↓
Cancel
   ↓
Refund
   ↓
Credit Transaction
```

---

## API

```http
POST /orders/{order_id}/cancel
```

---

## Workflow

```text
Order Creation
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
Status Updated
```

---

## Features

- Wallet Refund
- Credit Transaction Creation
- Refund Auditing
- Double Refund Prevention

---

# Phase 12 - JWT Authentication

Introduced secure API access using JWT.

Relationship:

```text
User
   ↓
Register
   ↓
Login
   ↓
JWT Token
   ↓
Protected APIs
```

---

# User Collection

```json
{
  "username": "admin",
  "password": "$2b$12$hashed_password"
}
```

---

# Authentication APIs

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

# JWT Security

Passwords are:

```text
Hashed using bcrypt
```

Tokens are:

```text
Signed using HS256
```

Authentication is implemented using:

```python
python-jose

passlib

bcrypt
```

---

# Protected Endpoints

Examples:

```http
POST /clients

POST /accounts

POST /products

POST /campaigns

POST /claim-codes/upload/{campaign_id}

POST /wallets/generate/{campaign_id}

POST /orders

PATCH /orders/{order_id}/status

POST /orders/{order_id}/cancel
```

All require:

```http
Authorization: Bearer <jwt_token>
```

---

# Complete Capabilities

```text
✅ Authentication

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

✅ JWT Security
```

---

# Completed Phases

```text
✅ Phase 1 - Foundation

✅ Phase 2 - Client Module

✅ Phase 3 - Account Module

✅ Phase 4 - Product Module

✅ Phase 5 - Campaign Module

✅ Phase 6 - Claim Code Module

✅ Phase 7 - Wallet Module

✅ Phase 8 - Order Module

✅ Phase 9 - Order Status Workflow

✅ Phase 10 - Wallet Transaction History

✅ Phase 11 - Order Cancellation & Refund

✅ Phase 12 - JWT Authentication
```

---

# Upcoming Enhancements

## Phase 13

Dockerization

```text
Dockerfile

docker-compose.yml

Mongo Container

Application Container
```

## Phase 14

Pytest

```text
Unit Tests

Integration Tests

API Tests
```

---

# Final Outcome

The Campaign CMS now supports a complete enterprise-style reward lifecycle:

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
Transaction Tracking
      ↓
Order Lifecycle
      ↓
Refund Processing
      ↓
Secure Access Control
```

This project demonstrates backend architecture, authentication, financial workflows, transaction tracking, and reward management using FastAPI and MongoDB.