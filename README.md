# Campaign CMS Clone

An intermediate-level Campaign CMS built using **FastAPI** and **MongoDB**.

This project is inspired by enterprise reward management systems and recreates the complete reward lifecycle from campaign creation to wallet redemption, order processing, and transaction tracking.

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
- Managing Order Status Workflows
- Tracking Wallet Transactions
- Supporting Future Refund & Reversal Flows

---

# Complete System Architecture

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
Claim Codes
   ↓
Wallets
   ↓
Wallet Transactions
   ↓
Orders
   ↓
Order Status Workflow
```

---

# Technology Stack

- FastAPI
- MongoDB
- Motor
- Pydantic
- Pandas
- Uvicorn

---

# Project Structure

```text
campaign-cms-clone/

├── api/
│
│   ├── clients/
│   ├── accounts/
│   ├── products/
│   ├── campaigns/
│   ├── claim_codes/
│   ├── wallets/
│   ├── orders/
│   └── wallet_transactions/
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
order_items
```

---

# Environment Setup

## Create Virtual Environment

```bash
python3 -m venv venv
```

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

## Configure Environment

Create `.env`

```env
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=campaign_cms
```

---

## Run Application

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
Claim Code
      ↓
Wallet
      ↓
Wallet Transaction
      ↓
Order
```

---

# Phase 1 - Foundation

Completed:

- FastAPI Setup
- MongoDB Connection
- Environment Configuration
- Collection Configuration
- Health Endpoint

## Health Check

```http
GET /health
```

---

# Phase 2 - Client Module

Represents organizations using the platform.

Examples:

```text
Samsung India
MoneyMax
HSBC
Citibank
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

Represents business units under a client.

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

Represents redeemable rewards.

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

Represents reward programs.

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

### Link Product To Campaign

```http
POST /campaigns/{campaign_id}/products
```

### Get Campaign Products

```http
GET /campaigns/{campaign_id}/products
```

Relationship:

```text
Campaign
      ↓
Campaign Product Link
      ↓
Product
```

---

# Phase 6 - Claim Code Module

Claim Codes represent reward entitlements.

Example:

```text
SAM1001 = ₹5000

SAM1002 = ₹3000

SAM1003 = ₹10000
```

---

## CSV Upload Format

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

- Campaign Exists Validation
- CSV Header Validation
- Duplicate Claim Codes Validation
- Existing Claim Code Validation
- Positive Amount Validation

---

# Phase 7 - Wallet Module

Wallets store redeemable balances.

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

## Features

- Campaign Validation
- Claim Code Validation
- Duplicate Wallet Prevention
- Automatic Wallet Creation
- Automatic Balance Initialization

---

# Phase 8 - Order Module

Orders represent product redemptions.

Relationship:

```text
Wallet
    ↓
Order
```

---

## Order Flow

```text
Wallet
   ↓
Balance Validation
   ↓
Order Creation
   ↓
Wallet Deduction
```

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

- Wallet Validation
- Product Validation
- Insufficient Balance Validation
- Automatic Balance Deduction

---

# Phase 9 - Order Status Workflow

Introduced enterprise-style order lifecycle management.

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

## Status Lifecycle

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

### Update Status

```http
PATCH /orders/{order_id}/status
```

### Get Orders By Status

```http
GET /orders/status/{status}
```

Examples:

```http
GET /orders/status/pending

GET /orders/status/processing

GET /orders/status/completed

GET /orders/status/cancelled

GET /orders/status/failed
```

---

## Features

- Status Transition Validation
- Terminal State Protection
- Workflow Management
- Order Lifecycle Tracking

---

# Phase 10 - Wallet Transaction History

Introduced wallet audit tracking.

Relationship:

```text
Wallet
     ↓
Wallet Transactions
```

Purpose:

```text
Track every balance movement
inside a wallet.
```

---

# Transaction Types

```text
debit
credit
```

---

## Example Debit Transaction

```json
{
  "claim_code": "SAM1001",
  "transaction_type": "debit",
  "amount": 1000,
  "reference": "ORDER_123",
  "description": "Order redemption for Amazon Gift Card ₹500"
}
```

---

## Future Credit Transaction

```json
{
  "claim_code": "SAM1001",
  "transaction_type": "credit",
  "amount": 1000,
  "reference": "REFUND_123",
  "description": "Order Refund"
}
```

---

# Wallet Transaction APIs

## Get All Transactions

```http
GET /wallet-transactions
```

---

## Get Transaction By ID

```http
GET /wallet-transactions/{transaction_id}
```

---

## Get Transactions By Claim Code

```http
GET /wallet-transactions/claim-code/{claim_code}
```

Example:

```http
GET /wallet-transactions/claim-code/SAM1001
```

---

# Automatic Transaction Logging

Whenever an order is created:

```text
Order Created
      ↓
Wallet Deducted
      ↓
Debit Transaction Recorded
```

Example:

```text
Wallet = ₹5000

Redeem Amazon ₹500
      ↓
Wallet = ₹4500
      ↓
Transaction Added
```

---

# Wallet Audit Trail Example

```text
Claim Code:
SAM1001

Transactions:

Debit   ₹1000
Debit   ₹500
Debit   ₹750
```

This allows administrators to understand exactly how wallet balances changed over time.

---

# Current System Flow

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
Claim Codes
   ↓
Wallets
   ↓
Wallet Transactions
   ↓
Orders
   ↓
Order Status Workflow
```

---

# Completed Phases

```text
✅ Phase 1 - Foundation

✅ Phase 2 - Client Module

✅ Phase 3 - Account Module

✅ Phase 4 - Product Module

✅ Phase 5 - Campaign Module

✅ Phase 6 - Claim Codes Module

✅ Phase 7 - Wallet Module

✅ Phase 8 - Order Module

✅ Phase 9 - Order Status Workflow

✅ Phase 10 - Wallet Transaction History
```

---

# Recommended Next Phase

## Phase 11 - Order Cancellation & Wallet Refund

Workflow:

```text
Order Cancelled
      ↓
Wallet Refunded
      ↓
Credit Transaction Added
      ↓
Balance Restored
```

Example:

```text
Order Value = ₹1000

Available Balance = ₹4000

Cancel Order
      ↓

Available Balance = ₹5000

Transaction:
Credit ₹1000
```

This would bring the CMS even closer to a real enterprise rewards platform.

---

# Final Outcome

The system now supports a complete reward management lifecycle:

```text
Client Creation
      ↓
Account Creation
      ↓
Product Management
      ↓
Campaign Management
      ↓
Campaign Product Mapping
      ↓
Claim Code Upload
      ↓
Wallet Generation
      ↓
Wallet Transaction Tracking
      ↓
Order Creation
      ↓
Balance Deduction
      ↓
Order Status Workflow
```

This represents a solid intermediate-to-advanced Campaign CMS built using FastAPI and MongoDB.