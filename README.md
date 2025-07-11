# AgriTrack

AgriTrack is a simple, elegant, and responsive farm management web application built with **Flask**, **SQLite**, and **HTML/CSS**. It allows smallholder farmers or agricultural project teams to:

- Track expenses and sales
- Manage key farm activities (tasks)
- Register and log in users securely

## Features

- Add and view farm expenses and sales
- Manage farm tasks (e.g., planting, feeding, harvesting)
- User authentication (Sign up / Log in)
- Clean, farm-themed user interface
- Mobile-responsive design

---

## Technologies Used

- **Python 3** (Flask framework)
- **SQLite** for data storage
- **HTML5 / CSS3** for frontend
- **Jinja2** templating engine
- **Render.com** for deployment

---

## Getting Started (Local Development)

1. Clone the Repository
```bash
git clone https://github.com/teddjames/Agritrack.git
cd Agritrack
```

2. Create & Activate a Virtual Environment (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
5. Run the App
```bash
python app.py
Visit http://localhost:5000 in your browser.
```

6.Deployment
The app is deployed using Render.com.

Live Demo: [Insert your live Render link here once deployed]
(e.g. https://agritrack.onrender.com)

To update:

```bash
git add .
git commit -m "Update"
git push
```
-Your Render service will automatically redeploy after each push to the main/master branch.

## Project Structure
```bash
Agritrack/
│
├── app.py                # Main Flask app
├── users.db              # SQLite database
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   └── signup.html
├── static/
│   └── style.css         # Custom CSS
└── README.md
```

## Author
- Tedd James
