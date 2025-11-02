## Development

### Backend - To do list

- [x] Build a mock agent making proper tool call and respecting the tool_call_id policy of OpenAI.
- [x] Build a lifespan with a checkpointer (SQLite based)
- [x] Add route `/agent/chat/{thread_id}` to chat with one agent
    - [x] Add the agent id as optional param (enables later the capability the agent selection by the user)
    - [x] Implement pytest for the route
- [x] Add route `/agent/thread/{thread_id}` to pull the entire thread (representing the conversation) from the sqlite db.
    - [x] Implement pytest for the route.
- [x] Implement the `/agent/list_agents/`.
- [ ] Implement a `test_db` when mock/test variables are set to `True`.
- [ ] Implement an authentication for the user (https://medium.com/@wangarraakoth/user-authentication-in-fastapi-using-python-3b51af11b38d)
  - [ ] User registration. Endpoint: `POST /auth/register`.
  - [ ] User Login & Token Authentication. Endpoint: `POST /auth/login`.
  - [ ] Database to store users data.
- [ ] Implement an access to local model through Docker.
  - [ ] 
- [ ] Implement the logic to maintain a `profile` of the user based on previous conversation.
    - [ ] Save all questions-answers for a given user id.

### Backend - Authentication
# 🛡️ Authentication & Security Plan (FastAPI Backend)

## Overview
This plan outlines the steps to implement a **secure authentication system** and **data encryption** layer for a FastAPI backend.
Frontend integration (login/register UI) and email-based password setup are deferred to a later phase.

---

## ⚙️ Phase 1 — Core Authentication

### DONE **1. Project Setup**
- Initialize a FastAPI project with:
  - **SQLAlchemy** (or **Tortoise ORM**) for database
  - **Alembic** for migrations
  - **passlib[bcrypt]** for password hashing
  - **python-jose** or **PyJWT** for JWT tokens
  - **pydantic-settings** or **python-dotenv** for environment variables
- Create a `.env` file for:
  ```
  SECRET_KEY=
  ACCESS_TOKEN_EXPIRE_MINUTES=
  ALGORITHM=HS256
  DATABASE_URL=
  ```
- Reference:
  - [FastAPI Security (OAuth2 + JWT)](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
  - [Better Stack: Authentication with FastAPI](https://betterstack.com/community/guides/scaling-python/authentication-fastapi/)

---

### DONE **2. User Model & Database Schema**
- Define a `User` table with:
  - `id`
  - `email`
  - `hashed_password`
  - `is_active`
  - `created_at`
- Enforce email uniqueness.
- Use Alembic for migrations.
- Reference: [FastAPI + SQLAlchemy Docs](https://fastapi.tiangolo.com/tutorial/sql-databases/)

---

### **3. User Registration**
- Endpoint: `POST /auth/register`
- Validate email uniqueness.
- Hash passwords using:
  ```python
  from passlib.context import CryptContext
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  ```
- Store only the **hashed password** in the database.
- Reference: [Password Hashing in FastAPI](https://www.fastapitutorial.com/blog/password-hashing-fastapi/)

---

### **4. User Login & Token Authentication**
- Endpoint: `POST /auth/login`
- Verify credentials → generate JWT token.
- Include claims like `sub`, `exp`, and `iat`.
- Return token to client:
  ```json
  { "access_token": "<JWT>", "token_type": "bearer" }
  ```
- Add `/auth/me` endpoint using `get_current_user()` dependency.
- References:
  - [FastAPI OAuth2 Password Flow](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
  - [TestDriven.io: FastAPI JWT Auth](https://testdriven.io/blog/fastapi-jwt-auth/)

---

### DONE **5. Protect Routes**
- Secure routes using dependency injection:
  ```python
  @app.get("/protected")
  def protected(current_user: User = Depends(get_current_user)):
      return {"email": current_user.email}
  ```
- Implement role or permission checks if needed.
- Reference: [FastAPI Security Dependencies](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/)

---

### **6. Use Databases through SQLAlchemy
- Reference: [FastAPI auth with db](https://betterstack.com/community/guides/scaling-python/authentication-fastapi/)
---

## 🔒 Phase 2 — Data Encryption & Security

### **6. Encrypt Sensitive Data**
- Decide on encryption scope:
  - Full-disk (DB-level) encryption
  - Field-level encryption (recommended)
- Use AES symmetric encryption via `cryptography` library.
- Store the encryption key in environment variables.
- Reference:
  - [Python Cryptography Docs](https://cryptography.io/en/latest/)
  - [Handling Secrets Securely in FastAPI](https://www.getorchestra.io/guides/fastapi-secrets-management-handling-sensitive-data-with-secretstr-and-secretbytes)

---

### **7. Secure Application Configuration**
- Enforce HTTPS in production.
- Use strong JWT secret keys and short token lifetimes.
- Enable CORS if frontend is on a separate domain.
- Never log sensitive data.
- Consider:
  - Rate limiting login attempts
  - Centralized secret management
  - Regular token rotation
- References:
  - [8 Best Practices to Secure FastAPI](https://medium.com/@zaman.rahimi.rz/8-best-practices-to-make-python-fastapi-secure-785d75368a6e)
  - [Escape Tech: Secure FastAPI APIs](https://escape.tech/blog/how-to-secure-fastapi-api/)

---

## 📧 Phase 3 — Password Setup via Email (Optional / Future Work)

### **8. Email-based Password Setup**
- Later, implement:
  - `POST /auth/send-password-setup` → sends email with token
  - `POST /auth/set-password` → verifies token & sets password
- Use `fastapi-mail` or an external SMTP provider (e.g., SendGrid).
- References:
  - [FastAPI-Mail Library](https://sabuhish.github.io/fastapi-mail/)
  - [Password Reset with FastAPI JWT](https://testdriven.io/blog/fastapi-jwt-auth/#password-reset)


### Frontend - To do list

- [ ] Follow React typescript tutorial [here](https://handsonreact.com/docs/labs/react-tutorial-typescript#fundamentals)