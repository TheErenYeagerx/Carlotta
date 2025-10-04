<h1 align="center">✨ Carlotta ✨</h1>

<p align="center">
  <img src="https://files.catbox.moe/kdpomb.jpg" alt="Carlotta Bot" width="450">
</p>

<p align="center">
  <b>👾 Automatically Accept Telegram Group & Channel Join Requests</b><br>
  Built with <a href="https://docs.pyrogram.org">Pyrogram</a>, <a href="https://www.mongodb.com">MongoDB</a> & <a href="https://flask.palletsprojects.com/">Flask</a>.  
  <br>Simple • Fast • Professional — Inspired by <b>Carlotta</b>.
</p>

---

<p align="center">
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  </a>
  <a href="https://docs.pyrogram.org/">
    <img src="https://img.shields.io/badge/Pyrogram-2.x-FF6F00?style=for-the-badge&logo=telegram" />
  </a>
  <a href="https://www.mongodb.com/">
    <img src="https://img.shields.io/badge/MongoDB-Database-green?style=for-the-badge&logo=mongodb" />
  </a>
  <a href="https://flask.palletsprojects.com/">
    <img src="https://img.shields.io/badge/Flask-Webserver-black?style=for-the-badge&logo=flask" />
  </a>
</p>

---

## 📖 About
Carlotta Auto Approve Bot helps you manage Telegram groups and channels by **auto-accepting join requests**.  
No manual approvals needed — just deploy, add the bot, and relax.  

- 🔹 Supports Groups & Channels  
- 🔹 Force Subscribe System  
- 🔹 MongoDB Database Support  
- 🔹 Flask Web Support  
- 🔹 Multi-Owner (SUDO users)  
- 🔹 Broadcast & Stats Commands  

---

## ⚙️ Environment Variables

| Variable      | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `API_ID`      | Telegram API ID → [my.telegram.org](https://my.telegram.org)                 |
| `API_HASH`    | Telegram API Hash → [my.telegram.org](https://my.telegram.org)               |
| `BOT_TOKEN`   | Bot Token from [@BotFather](https://t.me/BotFather)                         |
| `CHID`        | Force-subscribe channel ID (make bot admin in that channel)                 |
| `SUDO`        | Bot owner IDs (for broadcast/stats). Multiple IDs separated by space        |
| `MONGO_URI`   | MongoDB connection URI → [Setup Guide](https://telegra.ph/How-To-get-Mongodb-URI-04-06) |

---

## 🛠 Commands

| Command        | Description                                 | Access      |
|----------------|---------------------------------------------|-------------|
| `/start`       | Check if bot is alive                       | Everyone    |
| `/users`       | Show bot statistics                         | Owner/SUDO  |                  | Owner/SUDO  |
| `/broadcast`   | Broadcast a message to all users            | Owner/SUDO  |

---

## 🚀 Deployment

You can deploy Carlotta Auto Approve Bot on **Heroku, Railway, Render, VPS** or any cloud hosting service.  

```bash
git clone https://github.com/TheErenYeagerx/Carlotta.git
cd Carlotta
pip install -r requirements.txt
python3 bot.py