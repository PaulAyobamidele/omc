Absolutely — here is a **clean, fully engineered, sequential end-to-end testing plan** for **EVERYTHING** we have built so far in your school system API.
This simulates a real QA test plan and ensures **roles, permissions, JWT, data flow, grades, and relationships** all work correctly.

Use this in **Thunder Client**, **Postman**, or **cURL**.

---

Absolutely — here is the **updated full end-to-end testing plan** with the **NEW parent-only signup flow for children**, meaning:

### ✅ **Parents now create student accounts themselves**

We no longer rely on:
❌ students signing themselves up
❌ Django admin linking parent → child manually

Instead, we now have:

### 🔹 **Parent Signup**

### 🔹 **Parent Login**

### 🔹 **Parent Creates Child Accounts via `/api/users/create-child/`**

### 🔹 **Child automatically assigned to that parent**

Everything below reflects that new architecture.

---

# 🚀 **UPDATED END-TO-END TEST PLAN (Parent-Only Child Signup)**

This new plan verifies:

### 🔐 Authentication

### 👨‍👩‍👧 Parent creates children

### 📝 Teacher grade creation

### 👀 Parent + student grade visibility

### 🔐 Permission enforcement

---

# ✅ **PHASE 1 — Signup (Only Parent & Teacher)**

We will now create:

* **1 Parent**
* **1 Teacher**
* **Children will be created by parent later**

---

## **TEST 1 — Signup Parent**

POST `/api/users/signup/`

```json
{
  "username": "dozie",
  "email": "dozie@example.com",
  "password": "test1234",
  "role": "parent"
}
```

Expected: parent created.

---

## **TEST 2 — Signup Teacher**

POST `/api/users/signup/`

```json
{
  "username": "mark",
  "email": "mark@example.com",
  "password": "test1234",
  "role": "teacher"
}
```

Expected: teacher created.

---

# 🚀 **PHASE 2 — Parent Logs In (JWT)**

## **TEST 3 — Parent Login**

POST `/api/token/`

```json
{
  "username": "dozie",
  "password": "test1234"
}
```

Store `access` token → parent_token.

---

# 🚀 **PHASE 3 — Parent Creates Children (NEW FLOW)**

Parents now use:

### **POST** `/api/users/create-child/`

This endpoint:
✔ creates a student
✔ assigns them automatically to the authenticated parent
✔ prevents student self-signup

---

## **TEST 4 — Parent Creates Child #1**

Headers:

```
Authorization: Bearer <parent_token>
```

Body:

```json
{
  "first_name": "Joy",
  "last_name": "Adubi",
  "date_of_birth": "2015-06-12",
  "grade_level": "Primary 5"
}

```

Expected:

```json
{
  "message": "Child account created successfully",
  "child": {
    "username": "joy",
    "role": "student",
    "parent": "dozie"
  }
}
```



## **TEST 5 — Parent Creates Child #2**

Same endpoint, new child:

```json
{
  "username": "ken",
  "email": "ken@example.com",
  "password": "childpass2"
}
```

Expected: second child created.

---

# 🚀 **PHASE 4 — Teacher Login**

## **TEST 6 — Login Teacher**

POST `/api/token/`

```json
{
  "username": "teacher1",
  "password": "test1234"
}
```

Store token → teacher_token.

---

# 🚀 **PHASE 5 — Children Login**

(This confirms children were created properly.)

---

## **TEST 7 — Login Child #1 (joy)**

```json
{
  "username": "joy",
  "password": "childpass1"
}
```

Store `joy_token`.

---

## **TEST 8 — Login Child #2 (ken)**

```json
{
  "username": "ken",
  "password": "childpass2"
}
```

Store `ken_token`.

---

# 🚀 **PHASE 6 — Verify Relationships**

## **TEST 9 — Parent ME Endpoint**

`GET /api/users/me/`
Headers: parent_token

Expected:

```json
{
  "username": "dozie",
  "role": "parent",
  "children": ["joy", "ken"]
}
```

---

## **TEST 10 — Child ME (joy)**

Headers: `joy_token`

Expected:

```json
{
  "username": "joy",
  "role": "student",
  "parent": "dozie"
}
```

---

# 🚀 **PHASE 7 — Teacher Creates Grades**

## **TEST 11 — Teacher Creates Grade for Joy**

POST `/api/grades/`
Headers: teacher_token

```json
{
  "student": "joy",
  "subject": "Math",
  "score": 88,
  "comments": "Good progress."
}
```

---

## **TEST 12 — Teacher Creates Grade for Ken**

```json
{
  "student": "ken",
  "subject": "English",
  "score": 92,
  "comments": "Excellent writing skills."
}
```

---

# 🚀 **PHASE 8 — Student Views Their Own Grades**

## **TEST 13 — Joy checks grades**

GET `/api/grades/student/`
Headers: `joy_token`

Expected: only Joy’s grades.

---

## **TEST 14 — Ken checks grades**

GET `/api/grades/student/`

Expected: only Ken’s grades.

---

# 🚀 **PHASE 9 — Parent Views All Children’s Grades**

## **TEST 15 — Parent views grade dashboard**

GET `/api/grades/parent/`
Headers: `parent_token`

Expected:

```json
[
  {
    "student": "joy",
    "subject": "Math",
    "score": 88
  },
  {
    "student": "ken",
    "subject": "English",
    "score": 92
  }
]
```

---

# 🚀 **PHASE 10 — Permission Checks**

## **TEST 16 — Parent tries to create a grade (should fail)**

Expected:

```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## **TEST 17 — Student tries parent endpoint (should fail or be empty)**

---

## **TEST 18 — Teacher tries student endpoint (should return empty list)**

---

## **TEST 19 — Unauthenticated user tries any grade endpoint**

Expected:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

# 🎉 **UPDATED PLAN COMPLETE (Parent-Only Child Signup Included)**

This version now correctly matches your updated system:

### ✔ Parent-only child creation

### ✔ Automatic parent-student linking

### ✔ Teacher-only grade entry

### ✔ Student/parent grade access

### ✔ Full RBAC + JWT verification

---

If you want…

### 👉 I can generate a **PDF version**

### 👉 A **Postman collection**

### 👉 Or an **automated pytest suite** for the entire plan

Which one do you want next?


# 🎉 **You have now fully tested your MVP backend.**

This plan validates:

* ✔ Multiple roles
* ✔ JWT Token issuing
* ✔ Token-based role enforcement
* ✔ Parent ↔ Student relationships
* ✔ Teacher-only grade entry
* ✔ Student grade visibility
* ✔ Parent multi-child grade aggregation
* ✔ Unauthorized access blocking

---

If you want, next we can test:

### 📄 PDF report generation

### 🛡 RBAC middleware

### 📂 Create a `reports` app

### 🧪 Automated pytest suite

### 🚀 Frontend (React) API integration plan

Just tell me:

👉 **Do you want the PDF Report testing plan next?**




