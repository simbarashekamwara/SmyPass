# SmyPass 🔐
> A terminal-based password manager built in Python — currently under active development.

![Status](https://img.shields.io/badge/status-in%20development-orange)
![Python](https://img.shields.io/badge/python-3.x-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What is SmyPass?

SmyPass is a CLI password manager that lets you securely store and manage your credentials from the terminal. It supports multiple users, encrypted vaults, and a clean tabulated interface — all without leaving the command line.

---

## Current Features

- Multi-user registration & login
- Password hashing with **Scrypt** (key derivation)
- Per-user encrypted credential vaults (Fernet/AES)
- Add, update, and delete saved credentials
- Account settings (change password, delete account)
- Clean tabulated display using `tabulate`

---

## Project Status

SmyPass is currently at **v0.4** and under active development.

| Version | Status |
|---------|--------|
| v0.1 — Basic CRUD | ✅ Done |
| v0.2 — Fernet vault encryption | ✅ Done |
| v0.3 — Replace MD5 with Scrypt | ✅ Done |
| v0.4 — Password strength checker | 🔄 In progress |
| v0.5 — Search + copy to clipboard | 🔜 Planned |
| v1.0 — Cross-platform + packaging | 🔜 Planned |

---

## Installation

```bash
git clone https://github.com/simbarashekamwara/SmyPass.git
cd SmyPass
pip install -r requirements.txt
python passman.py
```

### Dependencies

| Library | Purpose |
|---------|---------|
| `tabulate` | Pretty-print vault table |
| `cryptography` | Fernet encryption + Scrypt key derivation |
| `getpass` | Hidden password input |

Install all at once:
```bash
pip install tabulate cryptography
```

---

## File Structure

```
SmyPass/
├── passman.py        # Main application
└── README.md
```

---

## Security

- Passwords hashed with **Scrypt** (not MD5 or SHA)
- Vault credentials encrypted at rest with **Fernet (AES-128)**
- Hidden password input via `getpass`

### Upcoming security improvements
- [ ] Master password timeout / session lock
- [ ] Input validation on all fields
- [ ] Login attempt limiting
- [ ] Migrate from `.txt` to encrypted SQLite

---

## Author

Built by **[Simbarashe Kamwara]** 
🔗 [LinkedIn](www.linkedin.com/in/simbarashekamwara) · [GitHub](https://github.com/simbarashekamwara)

---

> ⚠️ This project is under active development. Not recommended for production use yet.
