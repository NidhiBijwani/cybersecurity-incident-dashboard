# 🛡️ AI-Powered Cybersecurity Incident Dashboard

An AI-powered web application for monitoring, analyzing, and managing cybersecurity incidents.

The project combines a **FastAPI backend**, **React frontend**, **SQLite database**, and **machine-learning-based anomaly detection** to provide a centralized security operations dashboard.

---

## 📌 Overview

Cybersecurity teams need a simple way to monitor security incidents, identify suspicious activity, assess risk, and track incident status.

This project provides a dashboard where authenticated users can:

- Monitor cybersecurity incidents
- Add new security incidents
- Automatically calculate risk scores
- Detect potentially anomalous activity using Machine Learning
- Search and filter incidents
- View detailed incident information
- Close and reopen incidents
- Delete incidents
- Analyze security trends using charts
- Manage authentication securely using JWT

---

## ✨ Features
## Dashboard
## Dashboard

The dashboard provides a centralized view of cybersecurity incidents, including severity, risk scores, incident status, and AI-assisted anomaly detection!!

### 🔐 Authentication

- User registration
- Secure password hashing using Argon2
- JWT-based authentication
- Protected backend API endpoints
- Protected frontend routes
- Login and logout functionality

### 🚨 Incident Management

- Create security incidents
- View all incidents
- View detailed incident information
- Update incident status
- Close and reopen incidents
- Delete incidents
- Search incidents
- Filter by severity
- Filter by status

### 🤖 AI-Based Anomaly Detection

The project uses **Isolation Forest** from Scikit-learn to identify unusual security-event patterns.

The ML model analyzes:

- Failed login attempts
- Request count
- Connection count
- Bytes transferred

The detected anomaly is combined with incident severity to calculate a risk score between **0 and 100**.

### 📊 Dashboard

The dashboard provides:

- Total incident count
- Critical incident count
- High-risk incident count
- Open incident count
- Incident severity distribution
- System status
- Incident table
- Incident search and filters

### 📈 Analytics

The analytics page provides:

- Total incidents
- Open vs closed incidents
- High-risk incidents
- Severity distribution
- Incident status visualization
- Risk-score visualization
- Security summary

### 🧪 Testing

The backend includes automated tests for:

- User registration
- Login
- Invalid login
- Incident retrieval
- Incident creation
- Incident status updates
- Incident deletion
- Unauthorized access

Tests use an isolated in-memory SQLite database.

### ⚙️ CI

GitHub Actions automatically runs backend tests when code is pushed or a pull request is created.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                               │ HTTP / REST API
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
       │    JWT      │  │   SQLite     │  │  ML Detector │
       │    Auth     │  │   Database   │  │IsolationForest│
       └─────────────┘  └──────────────┘  └──────────────┘
                                                │
                                                ▼
                                      ┌──────────────────┐
                                      │   Risk Score     │
                                      │    0 - 100       │
                                      └──────────────────┘