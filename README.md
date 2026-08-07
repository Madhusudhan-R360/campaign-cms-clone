# Campaign CMS Clone

An intermediate-to-advanced Campaign CMS built using **FastAPI** and **MongoDB**.

This project recreates the complete reward lifecycle used in enterprise reward and loyalty platforms, from campaign creation to reward redemption, transaction tracking, and refund processing.

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
- Managing Order Statuses
- Tracking Wallet Transactions
- Supporting Order Cancellation & Refunds

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
   ↓
Refund Workflow
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
│   ├── wallet_transactions/
│   └── orders/
│
├── db/
│   ├── config.py
│   └── connection.py
│
├── uploads/
│   └── csv/
│
├── main.py
├── .env
├── requirements.txt
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

# Setup

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

Swagger UI:

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
Refund Workflow
```

---

# Phase 1 - Foundation

Completed:

- FastAPI Setup
- MongoDB Setup
- Environment Configuration
- Collection Definitions
- Health Endpoint

## API

```http
GET /health
```

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

Products represent rewards available for redemption.

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

Samsung Festive rewards

Samsung Referral Campaign
```

## APIs

```http
POST /campaigns

GET /campaigns

GET /campaigns/{campaign_id}

PUT /campaigns/{campaign_id}
```

---

## Campaign Product Mapping APIs

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

Claim codes represent reward balances.

Example:

```text
SAM1001 = ₹5000

SAM1002 = ₹3000

SAM1003 = ₹10000
```

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

## Validations

- Campaign validation
- CSV structure validation
- Duplicate claim code validation
- Existing claim code validation
- Positive amount validation

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

- Automatic wallet generation
- Claim code validation
- Duplicate wallet prevention
- Balance initialization

---

# Phase 8 - Order Module

Orders represent reward redemptions.

Relationship:

```text
Wallet
      ↓
Order
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

- Wallet validation
- Product validation
- Balance validation
- Wallet deduction

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

### Update Status

```http
PATCH /orders/{order_id}/status
```

### Get Orders By Status

```http
GET /orders/status/{status}
```

---

## Features

- Status transition validation
- Terminal state protection
- Workflow tracking

---

# Phase 10 - Wallet Transaction History

Introduced full wallet audit trail.

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

## Example Debit Transaction

```json
{
  "claim_code": "SAM1001",
  "transaction_type": "debit",
  "amount": 1000,
  "reference": "ORDER_123",
  "description": "Order redemption"
}
```

---

## APIs

### Get All Transactions

```http
GET /wallet-transactions
```

### Get Transaction By Id

```http
GET /wallet-transactions/{transaction_id}
```

### Get Transactions By Claim Code

```http
GET /wallet-transactions/claim-code/{claim_code}
```

---

## Features

- Automatic debit transaction creation
- Wallet audit tracking
- Transaction lookup
- Claim code transaction history

---

# Phase 11 - Order Cancellation & Wallet Refund

Introduced refund and balance restoration workflow.

Relationship:

```text
Order
   ↓
Cancellation
   ↓
Wallet Refund
   ↓
Credit Transaction
```

---

# Cancellation Workflow

```text
Create Order
      ↓
Wallet Debit
      ↓
Debit Transaction

Cancel Order
      ↓
Wallet Refund
      ↓
Credit Transaction
      ↓
Order Status = Cancelled
```

---

## Business Rules

### Allowed

```text
pending → cancelled

processing → cancelled
```

### Not Allowed

```text
completed → cancelled

failed → cancelled

cancelled → cancelled
```

---

## API

### Cancel Order

```http
POST /orders/{order_id}/cancel
```

---

## Refund Flow Example

### Initial Wallet

```json
{
  "available_balance": 5000,
  "consumed_balance": 0
}
```

### Create Order

```text
Order Amount = 1000
```

Wallet becomes:

```json
{
  "available_balance": 4000,
  "consumed_balance": 1000
}
```

### Cancel Order

```http
POST /orders/{order_id}/cancel
```

Wallet becomes:

```json
{
  "available_balance": 5000,
  "consumed_balance": 0
}
```

---

## Credit Transaction

Created automatically:

```json
{
  "claim_code": "SAM1001",
  "transaction_type": "credit",
  "amount": 1000,
  "reference": "ORDER_ID",
  "description": "Refund for order"
}
```

---

## Features

- Order cancellation
- Wallet refund
- Automatic credit transaction logging
- Refund audit trail
- Status update to cancelled
- Double refund prevention

---

# Complete Example Scenario

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
Wallet ₹5000
      ↓
Order ₹1000
      ↓
Wallet ₹4000
      ↓
Cancel Order
      ↓
Wallet ₹5000
      ↓
Credit Transaction ₹1000
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

✅ Phase 11 - Order Cancellation & Wallet Refund
```

---

# Current System Capabilities

```text
Client Management

Account Management

Product Management

Campaign Management

Campaign Product Mapping

Claim Code Upload

Wallet Generation

Order Creation

Wallet Deduction

Order Status Lifecycle

Wallet Transaction Tracking

Order Cancellation

Wallet Refund Processing

Transaction Audit Trail
```

---

# Recommended Future Enhancements

```text
Campaign Analytics Dashboard

Inventory Management

RBAC (Role Based Access Control)

Approval Workflow

Campaign Clone

Claim Code Expiry

Scheduled Campaign Activation
```

---

# Final Outcome

The Campaign CMS now supports a complete reward management lifecycle with:

```text
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
Order Workflow
      ↓
Transaction Tracking
      ↓
Refund Processing
```

This closely resembles a real-world enterprise rewards and campaign management platform built using FastAPI and MongoDB.