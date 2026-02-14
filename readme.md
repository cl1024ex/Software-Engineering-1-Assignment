# Community Tourist Assistant (MVP)

A crowd-sourced tourist information platform that allows tourists to browse attractions, registered users to submit attractions and reviews, and administrators to moderate content.  
Built with **Flask (Python)**, **MongoDB**, and **server-rendered HTML/CSS**.

---

## Key features (MVP)
### Non-registered user
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

## Prerequisites
- requirements.txt
-pip install -r requirements.txt

---

## Setup and run (local development)

### 1) Clone the repository
git clone <YOUR_REPO_URL>
cd <YOUR_PROJECT_FOLDER>

### 2) Create a virtual environment

### 3) Install the requirements.txt

### 4) Run application using Flask Run
