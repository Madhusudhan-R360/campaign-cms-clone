# Campaign CMS Clone

An intermediate-level Campaign CMS built using FastAPI and MongoDB.

This project is inspired by the Reward360 Campaign CMS and is being rebuilt from scratch to understand the architecture, business workflows, and system design behind a reward campaign management platform.

---

# Project Goal

Build a Campaign Management System that allows administrators to:

- Manage Clients
- Manage Accounts
- Manage Products
- Manage Campaigns
- Upload Claim Codes
- Generate Wallets
- Create Orders

The platform acts as the administrative side of a rewards ecosystem.

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
│   └── claim_codes/
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

Create `.env`

```env
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=campaign_cms
```

---

# Running Application

```bash
uvicorn main:app --reload
```

Swagger:

```text
http://localhost:8000/docs
```

---

# Current Business Hierarchy

```text
MoneyMax
   ↓
Singapore Account
   ↓
Amazon Voucher
   ↓
MoneyMax Welcome Campaign
   ↓
ABC123 Claim Code
```

---

# Phase 1 - Foundation

Completed:

- FastAPI Setup
- MongoDB Connection
- Environment Configuration
- Health Endpoint
- Collection Definitions

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

## Sample Payload

```json
{
  "account_name": "Singapore",
  "description": "Singapore Rewards Program",
  "client_id": "<client_id>",
  "active_status": true
}
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

Example:

```text
MoneyMax
   ↓
Singapore
   ↓
Amazon Voucher
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

The campaign module is the heart of the CMS.

Relationship:

```text
Campaign
        ↓
Campaign Product Link
        ↓
Product
```

---

## Campaign APIs

### Create Campaign

```http
POST /campaigns
```

### Get Campaigns

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

Response:

```json
[
  {
    "sku": "AMZ10",
    "name": "Amazon Voucher $10",
    "price": 10,
    "min_qty": 1,
    "max_qty": 5
  }
]
```

---

# Phase 6 - Claim Codes Module

This phase introduces reward entitlements.

Relationship:

```text
Campaign
    ↓
Claim Codes
```

Example:

```text
MoneyMax Welcome Campaign
      ↓
ABC123 ($100)

XYZ456 ($200)

PQR789 ($300)
```

---

# CSV Upload Format

Create a CSV file:

```csv
claim_code,amount,email
ABC123,100,test1@test.com
XYZ456,200,test2@test.com
PQR789,300,test3@test.com
```

---

# Claim Code Document

```json
{
  "_id": "...",
  "campaign_id": "...",
  "claim_code": "ABC123",
  "amount": 100,
  "email": "test1@test.com",
  "active_status": true,
  "created_at": "..."
}
```

---

# Claim Code APIs

### Upload Claim Codes

```http
POST /claim-codes/upload/{campaign_id}
```

Upload:

```text
sample_claim_codes.csv
```

Response:

```json
{
  "success": true,
  "message": "3 claim codes uploaded"
}
```

---

### Get All Claim Codes

```http
GET /claim-codes
```

---

### Get Claim Code By ID

```http
GET /claim-codes/{claim_code_id}
```

---

### Get Claim Codes By Campaign

```http
GET /claim-codes/campaign/{campaign_id}
```

---

# Claim Code Validations

Implemented:

### Campaign Validation

```text
Campaign must exist
```

---

### CSV Header Validation

Required headers:

```text
claim_code
amount
email
```

---

### Duplicate Claim Codes In File

Reject:

```text
ABC123
ABC123
```

---

### Existing Claim Code Validation

Prevents uploading a claim code already present in MongoDB.

---

### Amount Validation

Reject:

```text
0
-100
```

Accept:

```text
100
200
300
```

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
```

---

# Upcoming Phases

## Phase 7 - Wallet Module

```text
Claim Code
    ↓
Wallet
```

Features:

- Wallet Creation
- Balance Storage
- Wallet Lookup
- Wallet Validation

---

## Phase 8 - Order Module

```text
Wallet
   ↓
Orders
```

Features:

- Order Creation
- Product Redemption
- Balance Deduction
- Order History

---

# End Goal

Build an intermediate-level Campaign CMS that can:

```text
Manage Clients
Manage Accounts
Manage Products
Manage Campaigns
Upload Claim Codes
Generate Wallets
Create Reward Orders
```

while following clean backend architecture using FastAPI and MongoDB.