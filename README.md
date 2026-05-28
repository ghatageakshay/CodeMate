 🚀 CodeMate

CodeMate is a developer collaboration platform built to help students and beginner developers find teammates and build projects together.

The core idea is simple:

> Many developers have ideas but struggle to find the right people to build with.

CodeMate bridges that gap by enabling users to create profiles, discover similar developers, connect with them, and collaborate on projects in structured "Collab Rooms."

---

   ✨ Features (V2)

    🔐 Authentication
 User signup and login with secure password hashing
 Session-based authentication on all protected routes

    👤 User Profiles
 Name, skill level (Beginner/Intermediate/Mentor), and interests
 Interest tags displayed as clean badges
 Edit profile functionality

    🧩 Smart Matching Algorithm
 Users select from 14 CS domains (Frontend, Backend, AI/ML, etc.)
 Matching uses set intersection to find common interests
 Dashboard displays personalized match suggestions with connection status

    🤝 Connection System
 Send connection requests to matched developers
 Accept/reject incoming requests
 View all connections in organized tabs (Incoming, Sent, Connected)
 Real-time status updates across the platform

    🔍 Find Devs Page
 Browse all developers with real-time search
 Filter by name without page reload using REST API
 Smart connect buttons showing current connection status
 Built on `/api/users` REST endpoint

    💬 Direct Messaging
 Send messages only to accepted connections
 WhatsApp-style conversation UI (blue/grey bubbles)
 Inbox showing all active conversations
 Messages stored with timestamps

    📊 Dashboard Stats
 Real-time statistics: Total Connections, Pending Requests, Match Count
 Daily Dev Tip of the Day (curated developer quotes)
 Trending articles from DEV.to API
 Match suggestions with quick connect buttons

    🚀 Collab Rooms
 Create rooms with project name, description, and tech stack
 Define roles needed (Frontend, Backend, Designer, etc.) with skill requirements
 Dynamic role addition - add multiple roles without page reload
 Browse public feed - see all open collab rooms
 Room detail pages - full project info and role listings
 Role applications - apply with GitHub link and message
 Creator dashboard - review applications and accept/reject candidates
 Status tracking - applications show pending/accepted/rejected status

    📰 Developer Content
 Trending articles from DEV.to API
 Keeps dashboard active and informative

---

   🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Database | SQLite |
| Authentication | Werkzeug (password hashing) |
| API | REST API with JSON responses |
| Deployment | Render |
| External APIs | DEV.to Articles API |

---

   📸 Screenshots



---

   🚀 Deployment

Live Demo: https://codemate-rz34.onrender.com

Deployed to Render with auto-deploy on GitHub push.

Note: Optimized for desktop/laptop viewing (1024px+). Mobile UI improvements coming in V3.

---

   📌 Project Status

V2 - Feature Complete

V2 successfully implements the core vision: skill-based matching + project collaboration.

What's working:
 Complete user flows from signup to collab room creation
 Real-time search and filtering
 Messaging system for team communication
 Structured project collaboration with role-based applications
 Production deployment with auto-sync to GitHub

---

   🔮 V3 Roadmap

 Persistent Database: Migrate from SQLite to PostgreSQL
 ML Matching: Replace intersection algorithm with Cosine Similarity
 Room Chat: Real-time messaging inside collab rooms
 Notifications: Real-time alerts for connections, messages, applications
 Project Board: Kanban board inside rooms (To Do → In Progress → Done)
 Mobile Optimization: Full mobile-responsive redesign
 Code Architecture: Refactor into Flask Blueprints for scalability

---

   ⚠️ Known Limitations

 Database: SQLite data resets on server restart. PostgreSQL coming in V3.
 Mobile UI: Not optimized for mobile devices. Best on desktop (1024px+).
 Real-time Features: No WebSocket support yet. V3 will add live notifications.

---

   🧠 What I Built & Learned

Technical Skills:
 Full-stack Flask development (routes, sessions, databases)
 Relational database design (6 interconnected tables)
 REST API design and implementation
 Session-based authentication and authorization
 SQL queries (JOINs, CASE WHEN, aggregation with COUNT)
 JavaScript fetch API and DOM manipulation
 Deployment and production debugging

Product Thinking:
 User flows and UX design
 Matching algorithms (set theory)
 Feature prioritization and MVP planning
 Real-world deployment challenges

---

   📬 Feedback

Feedback and suggestions are welcome. If you're interested in the vision or want to collaborate, feel free to reach out!

---

Built as a solo college project with focus on learning, shipping, and iterating.
