# Community Tourist Assistant (MVP)

A crowd-sourced tourist information platform that allows tourists to browse attractions, registered users to submit attractions and reviews, and administrators to moderate content.  
Built with **Flask (Python)**, **MongoDB**, and **server-rendered HTML/CSS**.

---

## Project goal
To propose, design, and develop a crowd-sourced **Minimum Viable Product (MVP)** of the Community Tourist Assistant platform that supports tourism growth while minimising administrative overhead, and present the solution to stakeholders.

---

## Key features (MVP)
### Public / Tourist
- Browse approved attractions
- Search attractions by name (keyword search)
- View attraction details
- View reviews for attractions
- Report inappropriate reviews

### Registered user
- Register and log in
- Submit a new attraction (saved as **pending** until approved)
- Upload an image for an attraction (stored locally in `static/images/`)
- View and manage own pending/rejected attractions
- Edit rejected/pending attractions (resubmits for approval)
- Delete pending attractions
- Submit reviews and ratings (1–5)

### Administrator
- View moderation page
- Approve or reject pending attractions
- Promote users to admin / remove admin role
- Review reported reviews (approve/reject/delete)

---

## Tech stack
- **Backend:** Flask (Python)
- **Database:** MongoDB (local or MongoDB Atlas)
- **Frontend:** HTML templates + CSS
- **Auth:** session-based login
- **File handling:** image uploads saved under `static/images/`
- **Dependencies:** managed via `requirements.txt`

---

## Architecture (summary)
The system uses a **web-based, layered client–server architecture**:
- **Presentation layer:** HTML/CSS pages rendered by Flask templates
- **Application layer:** Flask routes act as controllers and apply business rules (moderation, authentication)
- **Data layer:** MongoDB stores users, admins, attractions, and reviews

The backend follows an **MVC-style structure**:
- **Models:** `User`, `Admin`, `Attractions`, `Reviews`
- **Controllers:** Flask route functions (`@app.route`)
- **Views:** HTML templates rendered

---

## Prerequisites
- requirements.txt
-pip install -r requirements.txt

---

## Setup and run (local development)

### 1) Clone the repository
```bash
git clone <YOUR_REPO_URL>
cd <YOUR_PROJECT_FOLDER>
