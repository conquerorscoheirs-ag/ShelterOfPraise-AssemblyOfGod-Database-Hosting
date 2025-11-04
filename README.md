# 🕊️ Shelter Of Praise | Assembly Of God Database-Hosting

> Hosting and managing church website data for **Shelter of Praise | Assembly of God**  
> Powered by **Supabase + Resend**, deployed for CCC Network digital ministry systems.

---

## 📖 Overview

This repository is responsible for handling and storing dynamic data used across the **Shelter of Praise | Assembly of God** website and its connected platforms under the **CCC Network**.

It powers features such as:
- 📬 Newsletter subscription and automated email delivery  
- 📰 News, Devotionals, and Event updates  
- 🙌 Ministry and Congregation member data  
- 💬 Future integration for CCC Network Hub (Thread-type app)

---

## 🧩 Tech Stack

| Technology | Purpose |
|-------------|----------|
| **Supabase** | Database + API Hosting |
| **Resend** | Email automation and notifications |
| **TypeScript + React (Vite)** | Frontend integration |
| **Node.js** | Backend scripts and API functions (optional) |

---

## ⚙️ Features

- Newsletter system with automated email notifications  
- Centralized and secure database for church data  
- Scalable backend powered by Supabase  
- Easy integration with Vite + React frontend  
- Expandable for future CCC Network features  

---

## 🪜 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/CCC-Network/ShelterOfPraise-AssemblyOfGod-Database-Hosting.git
cd ShelterOfPraise-AssemblyOfGod-Database-Hosting
````

### 2️⃣ Set Up Supabase

1. Go to [https://supabase.com](https://supabase.com) and create a project.
2. Copy your **API URL** and **Anon/Public Key**.
3. Create a table named `newsletter_subscribers` with:

   * `id` (UUID) – Primary Key
   * `email` (Text) – Subscriber email
   * `created_at` (Timestamp, default: now())

### 3️⃣ Connect Supabase to Your React App

Add environment variables to your `.env` file:

```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_KEY=your_public_key
```

### 4️⃣ Configure Resend (for email)

1. Go to [https://resend.com](https://resend.com) and create an account.
2. Copy your **API key**.
3. Add it to your backend or serverless function:

```env
RESEND_API_KEY=your_resend_api_key
```

### 5️⃣ Link Newsletter Form

Your newsletter form (`<input id="email-newsletter">` + `<button id="subscribe-button">`) connects through your `news.letter.system.ts` script to insert data into Supabase and trigger an email via Resend.

---

## 🌐 Purpose

This repository is part of the **CCC Network Digital Ecosystem**, a faith-driven initiative of **Shelter of Praise | Assembly of God** to:

> “Build, Connect, and Empower through Technology.”

---

## 🧠 Maintainers

**CCC Network Development Team**
📧 [conquerorscoheirsag@gmail.com](mailto:conquerorscoheirsag@gmail.com)
🏠 Shelter of Praise | Assembly of God, Kalilangan, Bukidnon, Philippines

---

© 2025 Conquerors & Co-Heirs | Shelter of Praise Assembly of God.
*All rights reserved.*