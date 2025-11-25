# JEE Aspirant SOCA Analysis 🎓

An AI-powered assessment and analysis tool designed to help JEE aspirants evaluate their academic performance and well-being. This application provides a detailed **SOCA (Strengths, Opportunities, Challenges, Action Plan)** report using Google's Gemini AI.

## ✨ Features

*   **Subject-wise Assessment**: Covers Physics, Chemistry, and Mathematics.
*   **Timed Core Section**: A 30-minute timer for the academic section to simulate exam pressure.
*   **Well-being Check**: A dedicated section for mental health and time management assessment.
*   **Smart Transition**: Interstitial screen to guide students between academic and well-being sections.
*   **AI-Powered Analysis**: Uses **Google Gemini Pro** to generate personalized, actionable insights based on student responses.
*   **Modern UI**: Built with React, Tailwind CSS, and Framer Motion for a smooth, responsive experience.

## 🛠️ Tech Stack

*   **Frontend**: React, Vite, Tailwind CSS, Framer Motion, Axios.
*   **Backend**: FastAPI, Python, Uvicorn.
*   **AI Model**: Google Gemini API (`gemini-pro`).

## 🚀 Setup Instructions

### Prerequisites
*   Node.js (v16+)
*   Python (v3.8+)
*   Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/))

### 1. Backend Setup

1.  Navigate to the root directory:
    ```bash
    cd JEE_SOCA
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add your API Key:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

5.  Start the Backend Server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The backend will run at `http://localhost:8000`.

### 2. Frontend Setup

1.  Open a new terminal and navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install --legacy-peer-deps
    ```

3.  Start the Development Server:
    ```bash
    npm run dev
    ```
    The frontend will run at `http://localhost:5173`.

## ☁️ Deployment (Vercel)

This project is configured for easy deployment on [Vercel](https://vercel.com).

1.  **Push to GitHub**: Push this repository to your GitHub account.
2.  **Import Project**: Go to Vercel and import the repository.
3.  **Configure Project Settings**:
    *   **Framework Preset**: Vite
    *   **Root Directory**: `.` (Leave as default)
    *   **Build Command**: `cd frontend && npm install && npm run build`
    *   **Output Directory**: `frontend/dist`
    *   **Install Command**: `pip install -r requirements.txt` (Vercel usually detects Python, but you might need to ensure it installs backend deps)
4.  **Environment Variables**:
    *   Add `GOOGLE_API_KEY` with your Gemini API key.
5.  **Deploy**: Click Deploy!

Vercel will automatically detect the `api/` folder and deploy the Python backend as serverless functions, while serving the React frontend.

## 📝 Usage

1.  Open `http://localhost:5173` in your browser.
2.  Click **"Start Assessment"**.
3.  Complete the questions for Physics, Chemistry, and Maths within the 30-minute limit.
4.  Proceed through the Transition Screen to the Well-being section.
5.  Submit your answers to receive a detailed AI-generated SOCA report.

## 📂 Project Structure

```
JEE_SOCA/
├── backend/                 # FastAPI Backend
│   ├── api/                 # API Routes
│   ├── main.py              # App Entry Point
│   ├── model.py             # Gemini AI Integration
│   └── questions.py         # Question Bank
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── components/      # Reusable Components
│   │   ├── pages/           # Page Views (Home, Test, Analysis)
│   │   └── App.jsx          # Main App Component
├── requirements.txt         # Python Dependencies
└── README.md                # Project Documentation
```