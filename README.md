# Campaign CMS Clone

An intermediate-level Campaign CMS built using **FastAPI** and **MongoDB**.

This project is inspired by enterprise reward management systems and recreates the complete reward lifecycle from campaign setup to order redemption.

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
- Managing Order Status Workflow
- Tracking Reward Redemption Lifecycle

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
orders
order_items
```

---

# Setup

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

## Environment Variables

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

# Business Hierarchy

```text
Samsung India
      ↓
Samsung eStore
      ↓
Amazon Gift Card ₹500
Flipkart Gift Card ₹1000
Myntra Voucher ₹750
      ↓
Samsung Welcome Rewards 2026
      ↓
Claim Codes
      ↓
Wallets
      ↓
Orders
```

---

# Phase 1 - Foundation

Completed:

- FastAPI Setup
- MongoDB Connection
- Environment Configuration
- Collection Definitions
- Health Check Endpoint

## Health API

```http
GET /health
```

Response:

```json
{
  "success": true,
  "message": "Campaign CMS Running"
}
```

---

# Phase 2 - Client Module

Represents the top-level business entity.

Examples:

```text
Samsung India
HSBC
MoneyMax
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

Relationship:

```text
Account
   ↓
Products
```

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

Samsung Referral Rewards

Samsung Festive Campaign
```

---

## Campaign APIs

```http
POST /campaigns

GET /campaigns

GET /campaigns/{campaign_id}

PUT /campaigns/{campaign_id}
```

---

## Campaign Product Mapping APIs

### Link Product To Campaign

```http
POST /campaigns/{campaign_id}/products
```

Payload:

```json
{
  "product_id": "<product_id>",
  "min_qty": 1,
  "max_qty": 5
}
```

---

### Get Campaign Products

```http
GET /campaigns/{campaign_id}/products
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
SAM1004,7500,neha@gmail.com
SAM1005,2000,rahul@gmail.com
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
- Duplicate Claim Code Validation
- Existing Claim Code Validation
- Amount Validation

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

## Wallet APIs

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
- Automatic Balance Initialization

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

## Order Creation Flow

```text
Wallet
    ↓
Balance Validation
    ↓
Product Validation
    ↓
Order Creation
    ↓
Wallet Deduction
```

---

## Order Example

```json
{
  "claim_code": "SAM1001",
  "product_name": "Amazon Gift Card ₹500",
  "quantity": 2,
  "amount": 1000
}
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
- Balance Validation
- Automatic Wallet Deduction

---

# Phase 9 - Order Status Workflow

This phase introduces enterprise-style order lifecycle management.

Previously:

```text
Order
   ↓
completed
```

Now:

```text
pending
   ↓
processing
   ↓
completed
```

or

```text
pending
   ↓
cancelled
```

or

```text
pending
   ↓
failed
```

---

# Order Status Lifecycle

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

# Order Status APIs

## Update Order Status

```http
PATCH /orders/{order_id}/status
```

Example:

```json
{
  "status": "processing"
}
```

---

## Get Orders By Status

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

# Supported Status Values

```text
pending
processing
completed
cancelled
failed
```

---

# Status Transition Rules

## Allowed

```text
pending → processing

pending → cancelled

pending → failed

processing → completed

processing → failed
```

---

## Not Allowed

```text
completed → processing

completed → pending

cancelled → completed

failed → processing
```

Terminal statuses cannot be modified.

---

# Example Workflow

## Step 1

Create Order

```text
Status = pending
```

---

## Step 2

Operations Team Starts Processing

```text
pending
   ↓
processing
```

---

## Step 3

Voucher Delivered

```text
processing
   ↓
completed
```

---

## Step 4

Failure Scenario

```text
pending
   ↓
failed
```

---

# Example End-to-End Flow

```text
Samsung India
        ↓
Samsung eStore
        ↓
Amazon Gift Card ₹500
        ↓
Samsung Welcome Rewards 2026
        ↓
Claim Code:
SAM1001
        ↓
Wallet:
₹5000
        ↓
Order:
₹1000
        ↓
Status:
Pending
        ↓
Processing
        ↓
Completed
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
```

---

# Recommended Next Phases

## Phase 10

Wallet Transaction History

```text
Wallet
   ↓
Credit / Debit Logs
```

---

## Phase 11

Order Cancellation + Wallet Refund

```text
Cancel Order
      ↓
Refund Wallet
```

---

## Phase 12

Campaign Analytics Dashboard

```text
Campaign Summary
Redemption Statistics
Wallet Utilization
Order Metrics
```

---

# Final Outcome

The Campaign CMS now supports the complete reward redemption lifecycle:

```text
Client Creation
       ↓
Account Creation
       ↓
Product Creation
       ↓
Campaign Creation
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
Order Status Workflow
```

This results in a functional, intermediate-level Campaign CMS closely resembling the workflow of a real reward management platform.