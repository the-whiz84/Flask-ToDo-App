# OrganizeIt

A modern, beautifully designed productivity application built with Python and Flask. OrganizeIt lets you create, manage, and track tasks across multiple custom lists with a seamless dark/light mode experience.

## Features

- **Multiple Task Lists** — Create custom lists and navigate between them using the responsive sidebar
- **Task Management** — Add, edit, complete, and delete tasks with due dates
- **Dynamic Due Badges** — Automatic status indicators: *Due today*, *On time*, *Past due*
- **Glassmorphism UI** — Premium design with frosted-glass panels and smooth micro-animations
- **Persistent Theming** — Dark/Light mode toggle saved to `localStorage`
- **CSRF Protection** — All forms secured with Flask-WTF CSRF tokens
- **App Factory Pattern** — Clean architecture using Flask Blueprints

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.14+, Flask, SQLAlchemy ORM |
| Auth | Flask-Login, Werkzeug password hashing |
| Forms | Flask-WTF / WTForms with validation |
| Frontend | HTML5, Vanilla JS, Bootstrap 5.3 |
| Icons | FontAwesome 6 (CSS Web Fonts) |
| Styling | Custom CSS with glassmorphism utilities |

## Project Structure

```
Flask-ToDo-App/
├── api/
│   ├── __init__.py        # App factory & extension init
│   ├── config.py          # Environment-driven configuration
│   ├── forms.py           # WTForms definitions
│   ├── main.py            # Application entrypoint
│   ├── models.py          # SQLAlchemy models (User, TaskList, Task)
│   ├── routes.py          # Blueprint routes
│   ├── static/
│   │   ├── assets/        # Favicon & background images (WebP)
│   │   ├── css/styles.css # Design system
│   │   └── js/scripts.js  # Theme toggler
│   └── templates/         # Jinja2 templates
├── .env                   # Environment variables (not tracked)
├── requirements.txt
└── vercel.json            # Vercel deployment config
```

## Running Locally

1. **Clone & enter the project:**
   ```bash
   git clone https://github.com/the-whiz84/Flask-ToDo-App.git
   cd Flask-ToDo-App
   ```

2. **Set up the environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env   # or create manually
   ```
   ```env
   SECRET_KEY=your_secure_secret_here
   DATABASE_URI=sqlite:///todo.db
   ```

4. **Run the app:**
   ```bash
   python3 api/main.py
   ```

5. **Open** `http://127.0.0.1:5000` in your browser.

## License

[MIT](LICENSE)