# Campaign CMS Clone

An intermediate-level Campaign CMS built using **FastAPI** and **MongoDB**.

This project is inspired by the Reward360 Campaign CMS and has been rebuilt from scratch to understand the complete reward campaign lifecycle, including campaign administration, claim code management, wallet generation, and reward redemption.

---

# Project Objective

Build a Campaign CMS that can:

- Manage Clients
- Manage Accounts
- Manage Products
- Manage Campaigns
- Map Products to Campaigns
- Upload Claim Codes
- Generate Wallets
- Process Reward Redemptions
- Track Orders

The project mirrors the workflow of a real-world rewards platform.

---

# End-to-End Architecture

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
│   ├── wallets/
│   │   ├── app.py
│   │   ├── schema.py
│   │   └── utility.py
│   │
│   └── orders/
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

# Environment Variables

Create `.env`:

```env
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=campaign_cms
```

---

# Run Application

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
- Health Endpoint

## Health Check

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

Represents the top-level organization.

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

### Sample Request

```json
{
  "client_name": "Samsung India",
  "time_zone": "Asia/Kolkata",
  "primary_contact": "rewards@samsung.com",
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

### Product Example

```json
{
  "account_id": "...",
  "sku": "AMZ500",
  "name": "Amazon Gift Card ₹500",
  "brand": "Amazon",
  "category": "Gift Card",
  "price": 500,
  "stock_count": 1000,
  "image_url": "https://amazon.com/logo.png",
  "active_status": true
}
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

### Link Product

```http
POST /campaigns/{campaign_id}/products
```

Request:

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

## Claim Code APIs

```http
POST /claim-codes/upload/{campaign_id}

GET /claim-codes

GET /claim-codes/{claim_code_id}

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

Wallets hold redeemable balances.

Relationship:

```text
Claim Code
     ↓
Wallet
```

Example:

```text
Claim Code:
SAM1001

Amount:
₹5000

↓

Wallet:
₹5000
```

---

## Wallet Structure

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

### Generate Wallets

```http
POST /wallets/generate/{campaign_id}
```

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

---

## Features

- Campaign Validation
- Claim Code Validation
- Duplicate Wallet Prevention
- Automatic Balance Initialization

---

# Phase 8 - Order Module

This is where redemption occurs.

Relationship:

```text
Wallet
    ↓
Order
```

---

# Redemption Flow

```text
Wallet Balance
      ↓
Product Selected
      ↓
Balance Validation
      ↓
Order Creation
      ↓
Wallet Deduction
```

---

## Example

Initial Wallet:

```text
Claim Code:
SAM1001

Available Balance:
₹5000
```

Redeem:

```text
Amazon Gift Card ₹500

Quantity = 2
```

Cost:

```text
₹1000
```

Updated Wallet:

```text
Available Balance = ₹4000

Consumed Balance = ₹1000
```

---

## Order Structure

```json
{
  "claim_code": "SAM1001",
  "product_name": "Amazon Gift Card ₹500",
  "quantity": 2,
  "amount": 1000,
  "status": "completed"
}
```

---

## Order APIs

### Create Order

```http
POST /orders
```

Request:

```json
{
  "claim_code": "SAM1001",
  "product_id": "<product_id>",
  "quantity": 2
}
```

---

### Get All Orders

```http
GET /orders
```

---

### Get Order By ID

```http
GET /orders/{order_id}
```

---

### Get Orders By Claim Code

```http
GET /orders/claim-code/{claim_code}
```

---

## Features

Implemented:

### Wallet Validation

```text
Wallet must exist
```

### Product Validation

```text
Product must exist
```

### Balance Validation

```text
Wallet Balance >= Order Value
```

### Automatic Wallet Deduction

```text
Available Balance ↓

Consumed Balance ↑
```

---

# End-to-End Test Scenario

## Client

```text
Samsung India
```

## Account

```text
Samsung eStore
```

## Products

```text
Amazon Gift Card ₹500

Flipkart Gift Card ₹1000

Myntra Voucher ₹750
```

## Campaign

```text
Samsung Welcome Rewards 2026
```

## Claim Codes

```text
SAM1001 = ₹5000

SAM1002 = ₹3000

SAM1003 = ₹10000
```

## Wallets

```text
SAM1001 → ₹5000

SAM1002 → ₹3000

SAM1003 → ₹10000
```

## Orders

```text
SAM1001

Amazon ₹500 × 2

Total = ₹1000
```

Wallet Balance:

```text
₹5000 → ₹4000
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
```

---

# Final Outcome

The system now supports the complete reward lifecycle:

```text
Client Creation
       ↓
Account Creation
       ↓
Product Creation
       ↓
Campaign Creation
       