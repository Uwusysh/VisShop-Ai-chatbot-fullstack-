
# 🤖 Chat – Full-Stack AI Chatbot

An end-to-end AI chatbot built with **React**, **Django**, and **MongoDB**, integrating **SentenceTransformers** for semantic search and **Groq’s LLaMA-3.1-8B** for intelligent, context-aware responses. The system uses a hybrid retrieval + generation pipeline and is optimized for accuracy, latency, and scalability.

---

## 🚀 How to Run the Project Locally

### Prerequisites

* Python 3.9+
* Node.js & npm
* Git

---

## 🧠 Backend Setup (Django)

> ⚠️ Backend must be run from the `chatbot_project` directory

```bash
cd Chat2/chatbot_project
```

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Apply Database Migrations

```bash
python manage.py migrate
```

### 3️⃣ Start Django Development Server

```bash
python manage.py runserver
```

📍 Backend URL:

```
http://localhost:8000
```

---

## 🎨 Frontend Setup (React)

> ⚠️ Frontend must be run from the `chatbot-frontend` directory

```bash
cd Chat2/chatbot-frontend
```

### 1️⃣ Install Dependencies

```bash
npm install
```

### 2️⃣ Start React Development Server

```bash
npm start
```

📍 Frontend URL:

```
http://localhost:3000
```

---

## 🔐 Environment Variables Setup

This project uses environment variables to securely manage sensitive credentials.
**Only the Groq API key is required.**

---

### 📁 Backend Environment (`chatbot_project/.env`)

Create a `.env` file inside the `chatbot_project` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

📌 **Important Notes**

* Do NOT commit the `.env` file to GitHub
* Add `.env` to `.gitignore`
* Restart the Django server after updating the `.env` file

---

## ✅ Verification Checklist

* ✅ Django server running on **port 8000**
* ✅ React app running on **port 3000**
* ✅ Chat responses generated using Groq LLaMA model

---

## 🛠 Tech Stack

* **Frontend:** React
* **Backend:** Django
* **Database:** MongoDB
* **Embeddings:** SentenceTransformers
* **LLM:** Groq LLaMA-3.1-8B
* **Deployment:** Render


