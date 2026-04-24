# Trust Labs Analytics — Setup Guide
## v4.0 · Authentication + Mobile + Keep-Alive

---

## What changed from v3.0

| Problem | Fix |
|---|---|
| No login — anyone with the URL could see everything | `streamlit-authenticator` — username + password required |
| SQL injection vulnerability in search queries | Parameterised queries with `?` placeholders throughout |
| App sleeps on Streamlit Cloud after inactivity | `streamlit-autorefresh` pings every 10 minutes silently |
| Broken on mobile — text too large, cards overflow | `@media` CSS breakpoints for 768px and 480px screens |
| `predict_visits()` recalculated on every tab switch | `@st.cache_data` added — cached for 1 hour |
| All tables loaded at startup even on unused pages | Lazy loading — each page loads only what it needs |
| SQLite default journal mode — unsafe for concurrent reads | WAL mode enabled on connection |

---

## Step 1 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 2 — Set your passwords

Run this once to generate hashed passwords:

```bash
python generate_passwords.py
```

Edit `generate_passwords.py` first — replace the placeholder strings with
your actual passwords, then run it. Copy the two hashed outputs into
`config.yaml` under each user's `password` field.

Example `config.yaml` after update:
```yaml
credentials:
  usernames:
    admin:
      email: ahmedsm2727@gmail.com
      name: Ahmed Mustafa
      password: $2b$12$abc123...  ← paste hashed password here
    branch_manager:
      email: manager@trustlabs.com
      name: Branch Manager
      password: $2b$12$xyz789...  ← paste hashed password here
```

---

## Step 3 — Change the cookie secret key

In `config.yaml`, replace:
```yaml
key: trust_labs_ultra_secret_key_change_this
```
with any long random string, e.g.:
```yaml
key: tl_k8$mNq2#vP9xR5@wL3jY7uE1cA6
```

---

## Step 4 — Run locally

```bash
streamlit run app.py
```

---

## Step 5 — Deploy to Streamlit Cloud (keep-alive included)

1. Push all files to a GitHub repo:
   ```
   app.py
   config.yaml
   requirements.txt
   generate_passwords.py   (optional — can exclude)
   .streamlit/config.toml
   trust_labs.db
   ```

2. Go to share.streamlit.io → New app → connect your repo

3. The `st_autorefresh` call in the app pings every 10 minutes —
   Streamlit Cloud won't put it to sleep as long as someone has
   the tab open. For 24/7 uptime with zero visits, use UptimeRobot
   (free) to ping your app URL every 5 minutes.

---

## UptimeRobot setup (free, keeps app alive 24/7)

1. Go to uptimerobot.com → Create free account
2. Add New Monitor:
   - Monitor Type: HTTP(s)
   - Friendly Name: Trust Labs Dashboard
   - URL: https://your-app-name.streamlit.app
   - Monitoring Interval: Every 5 minutes
3. Done. UptimeRobot hits your URL every 5 minutes.
   Streamlit Cloud sees traffic and never sleeps the app.

---

## Adding or changing users

Edit `config.yaml` directly. To add a new user:

```yaml
credentials:
  usernames:
    new_user:
      email: newuser@email.com
      name: New User Full Name
      password: PASTE_HASHED_PASSWORD_HERE
```

Generate the hash with `generate_passwords.py` — add their password
to the list, run it, copy the output.

---

## Login credentials (default — change these)

| Role | Username | Default password |
|---|---|---|
| Super Admin | `admin` | Set in generate_passwords.py |
| Branch Manager | `branch_manager` | Set in generate_passwords.py |

Session cookies last 7 days — users stay logged in across browser restarts.

---

## File structure

```
trustlabs/
├── app.py                  ← main application
├── config.yaml             ← user credentials (keep private)
├── requirements.txt        ← Python dependencies
├── generate_passwords.py   ← run once to hash passwords
├── trust_labs.db           ← SQLite database
└── .streamlit/
    └── config.toml         ← theme + server settings
```

---

## Security notes

- `config.yaml` contains password hashes — never commit to a public repo.
  Add it to `.gitignore` and use Streamlit Cloud Secrets instead:
  go to App Settings → Secrets and paste the YAML content there,
  then update `app.py` to read from `st.secrets` instead of the file.
- The cookie key in `config.yaml` signs session tokens — treat it like a password.
- All search queries use parameterised SQL — no injection risk.
