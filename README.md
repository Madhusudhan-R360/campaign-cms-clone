# Campaign CMS Clone

A simplified but intermediate-level clone of the Reward Campaign CMS platform built using FastAPI and MongoDB.

This project focuses on understanding and rebuilding the core CMS architecture used to manage:

- Clients
- Accounts
- Products
- Campaigns
- Claim Codes
- Wallets
- Orders

The goal is to recreate the business workflow of a campaign management platform while keeping the implementation practical and easy to extend.

---

# Current Progress

## ✅ Phase 1 - Foundation

Completed:

- FastAPI setup
- MongoDB connection
- Environment configuration
- Collection definitions
- Health check endpoint

## ✅ Phase 2 - Client Module

Completed:

- Create Client
- Get All Clients
- Get Client By ID
- Update Client

## ✅ Phase 3 - Account Module

Completed:

- Create Account
- Get All Accounts
- Get Account By ID
- Get Accounts By Client
- Update Account

---

# Business Hierarchy

The CMS follows the following hierarchy:

```text
Client
   ↓
Account
   ↓
Product
   ↓
Campaign
   ↓
Claim Codes
   ↓
Wallets
   ↓
Orders