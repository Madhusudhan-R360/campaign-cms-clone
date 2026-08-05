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
- Link Products to Campaigns
- Upload Claim Codes
- Generate Wallets
- Create Orders

The platform acts as the administrative side of a rewards ecosystem.

---

# High-Level Architecture

```text
Campaign CMS
      │
      ▼

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

# Business Flow

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
Claim Codes
   ↓
Wallet Balance
   ↓
Redeem Rewards
```

---

# Technology Stack

- FastAPI
- MongoDB
- Motor (Async Mongo Driver)
- Pydantic
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
│   └── campaigns/
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

Currently configured collections:

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

Collections currently in active use:

```text
clients
accounts
products
campaigns
campaign_products_link
```

Remaining collections will be used in upcoming phases.

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

Linux / Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file:

```env
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=campaign_cms
```

---

# Run Application

```bash
uvicorn main:app --reload
```

---

# Swagger Documentation

```text
http://localhost:8000/docs
```

---

# Health Check

## Endpoint

```http
GET /health
```

## Response

```json
{
  "success": true,
  "message": "Campaign CMS Running"
}
```

---

# Phase 1 - Foundation

Completed:

- FastAPI Setup
- MongoDB Connection
- Environment Configuration
- Collection Definitions
- Health Endpoint

---

# Phase 2 - Client Module

## Client Structure

```text
Client
```

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

## Sample Request

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

## Relationship

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

## Sample Request

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

## Relationship

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
Amazon Voucher $10
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
  "image_url": "https://sample.com/image.png",
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

This is the core of the CMS.

---

## Relationship

```text
Client
   ↓
Account
   ↓
Product

Campaign
   ↓
Campaign Product Mapping
   ↓
Product
```

---

## Why Campaign Product Mapping?

Instead of storing products directly inside campaigns:

```text
Campaign A
    ↓
Amazon

Campaign B
    ↓
Amazon
```

a mapping collection allows a product to belong to multiple campaigns.

---

## Campaign Structure

```json
{
  "name": "MoneyMax Welcome Campaign",
  "account_id": "...",
  "start_date": "2026-01-01T00:00:00",
  "end_date": "2026-12-31T23:59:59",
  "active_status": true
}
```

---

## Campaign Product Mapping Structure

```json
{
  "campaign_id": "...",
  "product_id": "...",
  "min_qty": 1,
  "max_qty": 5
}
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

### Attach Product To Campaign

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

# Current Data Hierarchy

```text
MoneyMax (Client)
       │
       ▼

Singapore (Account)
       │
       ▼

Amazon Voucher (Product)
       │
       ▼

MoneyMax Welcome Campaign
       │
       ▼

Campaign Product Link
```

---

# Completed Phases

```text
✅ Phase 1 - Foundation

✅ Phase 2 - Client Module

✅ Phase 3 - Account Module

✅ Phase 4 - Product Module

✅ Phase 5 - Campaign Module
```

---

# Upcoming Phases

## Phase 6

Claim Code Module

```text
CSV Upload
Claim Code Creation
```

---

## Phase 7

Wallet Module

```text
Wallet Creation
Balance Management
```

---

## Phase 8

Order Module

```text
Automatic Order Creation
Order Listing
Order Tracking
```

---

# End Goal

Recreate an intermediate-level version of the Reward Campaign CMS that can:

```text
Manage Clients
Manage Accounts
Manage Products
Manage Campaigns
Upload Claim Codes
Create Wallets
Generate Orders
```

while following real-world backend architecture and best practices using FastAPI and MongoDB.