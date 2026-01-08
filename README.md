# SellAndBuyCo

SellAndBuyCo is a referral-driven crypto trading platform MVP.

## Overview
This project focuses on a fee-based referral system designed for scalable growth.
Users are incentivized to invite others, earning commissions from trading fees.

## Core Features (MVP)
- User registration & login
- Referral system (2-level: L1 / L2)
- Trade-fee-based referral pool
- Commission ledger (payout history)
- Admin-configurable fees and referral rules

## Fee & Referral Logic
- Trade fee: **0.2%**
- Referral pool: **20% of trade fee**
- Referral split:
  - Level 1 (direct): **70%**
  - Level 2 (indirect): **30%**

### Example Calculation
Trade amount: `1,000,000`  
Trade fee (0.2%): `2,000`  
Referral pool (20%): `400`

- L1 commission: `280`
- L2 commission: `120`

## API Endpoints

### Health
- `GET /health`

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Trade
- `POST /trade/simulate`
- `GET /trade/commissions/{email}`

### Admin
- `GET /admin/fee`
- `POST /admin/fee`
- `GET /admin/referral-rules`
- `POST /admin/referral-rules`

## Tech Stack
- FastAPI
- SQLAlchemy
- Pydantic v2
- SQLite (MVP)
- Uvicorn

## Run Locally
```bash
cd backend
python -m uvicorn app.main:app --reload
