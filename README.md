# 🚖 Cab Fare Comparator — Uber vs Ola vs Rapido

> Automated real-time fare comparison dashboard built with Python, Selenium & Streamlit.
> Final-year B.Tech project by **Deepak** | Portfolio-ready | Local-run

---

## 📸 Features

| Feature | Description |
|---|---|
| 🟢 **Live Fare Scraping** | Selenium automates Uber, Ola & Rapido to fetch real fares |
| 💰 **Cheapest Highlight** | Instantly shows you which service saves the most money |
| 🔄 **Auto-Refresh** | Fares auto-update every N minutes (configurable) |
| 🍪 **Cookie Login** | Login once → cookies saved → no login needed next time |
| 🔐 **Env Var Login** | Store credentials in `.env` for fully headless automation |
| 📊 **Fare History** | Session-level fare history stored in CSV |

---

## 🗂️ Project Structure

```
cab_fare_comparator/
│
├── app.py                   # Streamlit dashboard (main entry point)
├── requirements.txt         # All Python dependencies
├── .env.example             # Template for credentials
├── .gitignore
├── README.md
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py      # Base class with shared Selenium logic
│   ├── uber_scraper.py      # Uber fare scraper
│   ├── ola_scraper.py       # Ola fare scraper
│   └── rapido_scraper.py    # Rapido fare scraper
│
├── utils/
│   ├── __init__.py
│   ├── cookie_manager.py    # Save/load browser cookies
│   ├── location_helper.py   # Jaipur location presets
│   └── data_logger.py       # Fare history CSV logger
│
├── data/
│   └── fare_history.csv     # Auto-generated fare log
│
└── cookies/                 # Saved browser session cookies
    ├── uber_cookies.pkl
    ├── ola_cookies.pkl
    └── rapido_cookies.pkl
```

---

## ⚙️ Setup & Run (Step-by-Step)

### 1. Clone / Download the project

```bash
git clone https://github.com/YOUR_USERNAME/cab-fare-comparator.git
cd cab-fare-comparator
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Google Chrome + ChromeDriver

- Download Chrome: https://www.google.com/chrome/
- ChromeDriver is auto-managed by `webdriver-manager` — no manual install needed ✅

### 5. Set up credentials

```bash
cp .env.example .env
# Now edit .env and fill in your Uber/Ola/Rapido phone numbers & passwords
```

### 6. Run the dashboard

```bash
streamlit run app.py
```

> Opens at: **http://localhost:8501**

---

## 🍪 Cookie Login (Recommended)

1. Open the dashboard → go to **"Login Manager"** tab
2. Click **"Login to Uber/Ola/Rapido"** — a browser window opens
3. Log in manually (solve any OTP/captcha)
4. Click **"Save Cookies"** — session is saved for future runs
5. Next time, just click **"Load Cookies"** — instant headless login!

---

## 🔐 Environment Variables

Edit `.env`:

```env
UBER_PHONE=+919876543210
UBER_PASSWORD=your_password

OLA_PHONE=+919876543210
OLA_PASSWORD=your_password

RAPIDO_PHONE=+919876543210
RAPIDO_PASSWORD=your_password

REFRESH_INTERVAL_MINUTES=5
```

---

## ⚠️ Important Notes

- **This is for educational purposes only.** Scraping may violate ToS of these apps.
- Use your **own accounts** only.
- Run locally — do not deploy publicly.
- Fares may differ from app due to dynamic pricing and location accuracy.
- If scrapers break, selectors in `scrapers/` need updating (sites change their HTML).

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Selenium 4 | Browser automation |
| BeautifulSoup4 | HTML parsing |
| Streamlit | Dashboard UI |
| webdriver-manager | Auto ChromeDriver |
| python-dotenv | Env var management |
| pandas | Data handling |
| plotly | Charts |

---

## 👨‍💻 Author

**Deepak** — B.Tech CSE, 3rd Year  
Project: Automated Cab Fare Comparator  
Built for: Semester Exam Project | Portfolio

---
