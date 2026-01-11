# Requirements — To-Do App MVP (v1)

Date: 2026-01-11

## Tech Stack (Decisions)
- **Frontend**: React + TypeScript
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **Deployment**: Render

## Requirements

| ID | Description | Priority | Verification |
|----|-------------|----------|--------------|
| REQ-001 | User registration with username + password (hashed) | P0 | Can create account, password stored securely |
| REQ-002 | User login/logout with JWT token | P0 | Can login, receive token, logout invalidates session |
| REQ-003 | CRUD to-do lists (create, read, update, delete) | P0 | All operations work via API and UI |
| REQ-004 | CRUD to-do items (title, completed status) | P0 | Items belong to lists, all operations work |
| REQ-005 | Backend API using FastAPI + PostgreSQL | P0 | API serves all endpoints, DB persists data |
| REQ-006 | Frontend UI using React + TypeScript | P0 | UI renders, interacts with API |
| REQ-007 | Deploy to Render (backend, frontend, DB) | P1 | App accessible via public URL |

## Assumptions
- Single-user lists (no sharing between users)
- To-do items have minimal fields: title, completed
- JWT for stateless authentication
- No email verification for MVP
