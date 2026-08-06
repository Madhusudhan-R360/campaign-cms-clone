# Campaign CMS Clone

An intermediate-level Campaign CMS built using FastAPI and MongoDB.

This project is inspired by the Reward360 Campaign CMS and is being rebuilt from scratch to understand the architecture, workflows, data relationships, and backend design behind a reward campaign management platform.

---

# Project Goal

Build a Campaign Management System that allows administrators to:

- Manage Clients
- Manage Accounts
- Manage Products
- Manage Campaigns
- Map Products to Campaigns
- Upload Claim Codes
- Generate Wallets
- Manage Reward Lifecycle
- Prepare for Product Redemption and Orders

---

# High-Level Architecture

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
│   │   ├── app.py
│   │   ├── schema.py
│   │   └── utility.py
│   │
│   ├── accounts/
│   │   ├── app.py
│   │   ├── schema.py
│   │   └── utility.py
│   │
│   ├── products/
│   │   ├── app.py
│   │   ├── schema.py
│   │   └── utility.py
│   │
│   ├── campaigns/
│   │   ├── app.py
│   │   ├── schema.py
│   │   └── utility.py
│   │
│   ├── claim_codes/
│   │   ├── app.py
│   │   ├── schema.py
│   │   └── utility.py
│   │
│   └── wallets/
│       ├── app.py
│       ├── schema.py
│       └── utility.py
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
orders
order_items
```

---

# Installation

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

# Environment Variables

Create a `.env` file.

```env
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=campaign_cms
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

# Current Business Flow

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
Claim Code
   ↓
Wallet
```

Example:

```text
MoneyMax
   ↓
Singapore Account
   ↓
Amazon Voucher
   ↓
Welcome Campaign
   ↓
ABC123
   ↓
Wallet Balance = $100
```

---

# Phase 1 - Foundation

Completed:

- FastAPI Setup
- MongoDB Connection
- Environment Configuration
- Collection Definitions
- Health Check Endpoint

---

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

Client represents the top-level organization.

Examples:

```text
MoneyMax
HSBC
Citibank
SingSaver
```

---

## APIs

### Create Client

```http
POST /clients
```

### Get All Clients

```http
GET /clients
```

### Get Client By ID

```http
GET /clients/{client_id}
```

### Update Client

```http
PUT /clients/{client_id}
```

---

## Sample Payload

```json
{
  "client_name": "MoneyMax",
  "time_zone": "Asia/Singapore",
  "primary_contact": "admin@moneymax.com",
  "active_status": true
}
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
MoneyMax
   ↓
Singapore
```

---

## APIs

### Create Account

```http
POST /accounts
```

### Get All Accounts

```http
GET /accounts
```

### Get Account By ID

```http
GET /accounts/{account_id}
```

### Get Accounts By Client

```http
GET /accounts/client/{client_id}
```

### Update Account

```http
PUT /accounts/{account_id}
```

---

# Phase 4 - Product Module

Relationship:

```text
Client
   ↓
Account
   ↓
Product
```

---

## Product Structure

```json
{
  "account_id": "...",
  "sku": "AMZ10",
  "name": "Amazon Voucher $10",
  "brand": "Amazon",
  "category": "Gift Card",
  "price": 10,
  "stock_count": 1000,
  "image_url": "https://example.com/image.png",
  "active_status": true
}
```

---

## APIs

### Create Product

```http
POST /products
```

### Get All Products

```http
GET /products
```

### Get Product By ID

```http
GET /products/{product_id}
```

### Get Products By Account

```http
GET /products/account/{account_id}
```

### Update Product

```http
PUT /products/{product_id}
```

---

# Phase 5 - Campaign Module

Campaigns represent reward programs.

Example:

```text
MoneyMax Welcome Campaign
MoneyMax Referral Campaign
HSBC Rewards Campaign
```

---

# Campaign Product Mapping

Products are linked to campaigns through a mapping collection.

Relationship:

```text
Campaign
      ↓
Campaign Product Link
      ↓
Product
```

This allows:

```text
Amazon Voucher
      ↓
Campaign A

Amazon Voucher
      ↓
Campaign B
```

---

## Campaign APIs

### Create Campaign

```http
POST /campaigns
```

### Get All Campaigns

```http
GET /campaigns
```

### Get Campaign By ID

```http
GET /campaigns/{campaign_id}
```

### Update Campaign

```http
PUT /campaigns/{campaign_id}
```

---

## Campaign Product APIs

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

# Phase 6 - Claim Codes Module

Claim Codes represent reward entitlements.

Example:

```text
ABC123 = $100

XYZ456 = $200

PQR789 = $300
```

---

# CSV Upload Format

```csv
claim_code,amount,email
ABC123,100,test1@test.com
XYZ456,200,test2@test.com
PQR789,300,test3@test.com
```

---

## Claim Code Document

```json
{
  "_id": "...",
  "campaign_id": "...",
  "claim_code": "ABC123",
  "amount": 100,
  "email": "test1@test.com",
  "active_status": true
}
```

---

## APIs

### Upload Claim Codes

```http
POST /claim-codes/upload/{campaign_id}
```

### Get All Claim Codes

```http
GET /claim-codes
```

### Get Claim Code By ID

```http
GET /claim-codes/{claim_code_id}
```

### Get Claim Codes By Campaign

```http
GET /claim-codes/campaign/{campaign_id}
```

---

## Validations

Implemented:

- Campaign Validation
- CSV Header Validation
- Duplicate Claim Codes Validation
- Existing Claim Code Validation
- Amount Validation

---

# Phase 7 - Wallet Module

Wallets provide balance management for claim codes.

Relationship:

```text
Claim Code
      ↓
Wallet
```

---

## Wallet Structure

```json
{
  "_id": "...",
  "campaign_id": "...",
  "claim_code": "ABC123",
  "total_balance": 100,
  "available_balance": 100,
  "consumed_balance": 0,
  "active_status": true
}
```

---

## Wallet Generation Flow

```text
Campaign
     ↓
Claim Codes
     ↓
Generate Wallets
     ↓
Wallet Balance Created
```

Example:

```text
Claim Code:
ABC123

Amount:
100

↓

Wallet

Total Balance      : 100
Available Balance  : 100
Consumed Balance   : 0
```

---

## Wallet APIs

### Generate Wallets

```http
POST /wallets/generate/{campaign_id}
```

Creates wallets from all claim codes belonging to the campaign.

---

### Get All Wallets

```http
GET /wallets
```

---

### Get Wallet By ID

```http
GET /wallets/{wallet_id}
```

---

### Get Wallet By Claim Code

```http
GET /wallets/claim-code/{claim_code}
```

Example:

```http
GET /wallets/claim-code/ABC123
```

---

## Wallet Features

Implemented:

### Campaign Validation

Ensure campaign exists.

### Claim Code Validation

Wallets are only generated from existing claim codes.

### Duplicate Wallet Prevention

A claim code can only have one wallet.

### Automatic Balance Initialization

```text
Claim Code Amount
      ↓
Wallet Total Balance

Claim Code Amount
      ↓
Wallet Available Balance
```

---

# Current Project Status

```text
✅ Phase 1 - Foundation

✅ Phase 2 - Client Module

✅ Phase 3 - Account Module

✅ Phase 4 - Product Module

✅ Phase 5 - Campaign Module

✅ Phase 6 - Claim Codes Module

✅ Phase 7 - Wallet Module
```

---

# Upcoming Phases

## Phase 8 - Order Module

Relationship:

```text
Wallet
    ↓
Order
```

Features:

- Redeem Product
- Balance Validation
- Balance Deduction
- Order Creation
- Order History

---

# Final Goal

Build a fully functional Campaign CMS capable of:

```text
Managing Clients
Managing Accounts
Managing Products
Managing Campaigns
Uploading Claim Codes
Generating Wallets
Creating Orders
Managing Reward Redemptions
```

using FastAPI, MongoDB, and real-world backend architecture patterns.