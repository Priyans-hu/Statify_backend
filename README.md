# 🔧 Statify Status Dashboard

A multi-tenant real-time status page system for organizations to monitor/track services, log incidents, and show live status to end users.. Built with scalability and RBAC in mind.

## 🧩 Features

- User authentication (JWT)
- Organization & Admin access
- CRUD for services
- Role-based access control
- Modular routes-controller-service backend

## 🧠 Architecture

### Folder Structure

```shell
backend/
├── app/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   └── utils/
├── main.py
└── requirements.txt
```

### Why this structure?

Used a routes-controller-service architecture to decouple routing, business logic, and data access. This ensures better testability and easier maintenance as features scale.

### Design Decisions

- Decoupled layers (routes/controller/service) to isolate responsibilities
- Pydantic schemas for validation and documentation
- UUIDs for all primary keys for easier multi-tenant separation
- Org-based service filtering at DB + controller layer

## ⚙️ Running Locally

### Backend

```bash
cd backend
cp .env.example .env
docker-compose up --build
```

### Frontend

Checkout: [GitHub Repository](https://github.com/Priyans-hu/Statify_frontend)

Build with next.js (tailwindcss, shadcdn, typescript)

## 📜 API Reference

Auto-generated at: `http://localhost:8000/docs`
