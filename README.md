Flask OAuth Authentication

Click here to view my project:  
[My Project](https://flask-oauth-authentication.onrender.com)
---

This project is a simple authentication system I built using Flask where users can log in using Google, Facebook, or X (Twitter).

The main goal was to understand how OAuth works in real-world applications and how different providers handle authentication.

---

What I Built

- Login system using:
  - Google OAuth  
  - Facebook OAuth  
  - X (Twitter) OAuth  
- User data is stored in a database (SQLite)  
- After login, users are redirected to a dashboard showing their details  
- Deployed the full app on Render  

---

How It Works

1. The user clicks on a login button  
2. The app redirects the user to the provider (Google/Facebook/X)  
3. The user logs in and gives permission  
4. The provider sends back a callback request to my app  
5. The app fetches user information using the provider’s API  
6. If the user does not exist in the database, a new record is created  
7. The user is stored in session and redirected to the dashboard  

Each provider behaves slightly differently:

- Google provides full profile information and email  
- Facebook provides email (if permission is granted)  
- X (Twitter) does not provide email, so a fallback using user ID is used  

---

Tech Used

- Python (Flask)  
- Authlib (OAuth integration)  
- SQLAlchemy  
- SQLite  
- HTML/CSS  
- Render (Deployment)  
