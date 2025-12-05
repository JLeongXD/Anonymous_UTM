
# Anonymous UTM - Project Documentation

**GitHub Repository:** [Insert Your GitHub Link Here]

## 1. Summary
**Anonymous UTM** is a full-stack confession platform designed for university students. It bridges the gap between the need for emotional expression and the fear of judgment. The system consists of a **React-based Web Portal** (Frontend) that simulates a secure chat interface to guide users, and a **Python-based Telegram Bot** (Backend) that handles the actual submission processing. The core innovation is the integration of **Google Gemini AI**, which acts as automated moderator to filter inappropriate content (nudity, violence, hate speech) and analyze sentiment before publishing confessions to a public Telegram channel.

---

## 2. Problem Overview
In many universities, students often wish to express their feelings, opinions, or personal experiences anonymously. However, there is currently no dedicated platform that allows them to do so safely and privately. Without such a system, students may struggle to share their thoughts or seek emotional support, leading to:
*   Limited communication within the student body.
*   Social isolation.
*   Unaddressed mental stress.

Existing solutions (like Google Forms) lack real-time engagement and automated safety filtering, often requiring manual moderation which is slow and prone to human error.

---

## 3. Desired Outcome
The goal is to deploy a fully functional, secure, and anonymous confession ecosystem.
*   **For Users:** A safe space to vent or confess without fear of identity exposure.
*   **For Admins:** A significant reduction in manual moderation workload due to AI filtering.
*   **For the Community:** A healthier social environment where toxic content is filtered out before it reaches the public eye.

---

## 4. Execution Plan

The project execution is divided into three main architectural layers:

### Phase 1: Frontend Development (The Portal)
*   **Objective:** Create a welcoming, "app-like" landing page.
*   **Technology Stack:**
    *   **React (TypeScript):** Chosen for its component-based architecture, enabling a dynamic "Single Page Application" (SPA) feel that mimics a native chat app.
    *   **Tailwind CSS:** Used for rapid, utility-first styling. It handles the complex "Glassmorphism" effects, gradients, and mobile-first responsiveness essential for the design.
    *   **Vite:** The build tool used for lightning-fast development and optimized production bundling.
    *   **Lucide React:** Provides a consistent, lightweight set of SVG icons (User, Venetian Mask, etc.).
    *   **Vercel:** The hosting platform for continuous deployment and global edge network delivery.
*   **Action:**
    *   Design a mobile-first interface resembling a dark-mode chat app.
    *   Implement "Anonymous" vs. "Named" mode selection.
    *   Use deep linking to redirect users to the Telegram Bot with specific parameters.

### Phase 2: Backend Development (The Bot)
*   **Objective:** Handle message reception and processing.
*   **Tech:** Python, Telethon Library.
*   **Action:**
    *   Set up a Telegram Client to listen for incoming messages.
    *   Implement state management to track user modes (Anonymous/Named).
    *   Create admin logging for audit trails.

### Phase 3: AI Integration (The Moderator)
*   **Objective:** Filter unsafe content automatically.
*   **Tech:** Google Gemini 2.5 Flash API.
*   **Action:**
    *   Send image/text payloads to Gemini.
    *   Engineer prompts to detect Nudity, Gore, and Hate Speech.
    *   Implement conditional logic: If `SAFE` -> Publish; If `UNSAFE` -> Block & Warn.

---

## 5. Environment Setup & Installation

### Prerequisites
*   **Node.js** (v18+)
*   **Python** (v3.10+)
*   **Telegram API ID & Hash** (from my.telegram.org)
*   **Bot Token** (from @BotFather)
*   **Google Gemini API Key** (from AI Studio)

### A. Frontend Setup (Web Portal)
1.  **Clone the repository:**
    ```bash
    git clone [Insert Your GitHub Link Here]
    cd anonymous-utm
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run locally:**
    ```bash
    npm run dev
    ```
    Access the app at `http://localhost:5173`.

### B. Backend Setup (Telegram Bot)
1.  **Navigate to backend directory:**
    ```bash
    cd backend
    ```
2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows: venv\Scripts\activate
    # Mac/Linux: source venv/bin/activate
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install telethon google-generativeai python-dotenv
    ```
4.  **Configure Environment Variables:**
    Create a `.env` file in the `backend/` folder:
    ```env
    API_ID=12345678
    API_HASH=your_api_hash
    BOT_TOKEN=your_bot_token
    GEMINI_API_KEY=your_gemini_key
    CHANNEL_ID=@your_public_channel
    ADMIN_ID=your_admin_id
    ```
5.  **Run the Bot:**
    ```bash
    python confessionbot.py
    ```

---

## 6. Risks & Mitigation Strategies

| Risk Category | Potential Issue | Mitigation Strategy |
| :--- | :--- | :--- |
| **Technical** | API Rate Limits (Gemini/Telegram) | Implement asynchronous queues and error handling (exponential backoff). |
| **Safety** | AI "False Negatives" (Missing bad content) | Maintain an admin log channel where *all* posts are sent for post-publication review if needed. |
| **Privacy** | Data Leaks | Do not store user IDs in a persistent database; keep logs transient or admin-only. Use `.gitignore` for secrets. |
| **Operational** | Bot Downtime | Deploy backend on a cloud service (e.g., Railway/Heroku) with auto-restart policies. |

---

## 7. Deliverables
1.  **Web Portal URL:** Hosted on Vercel (e.g., `https://anonymous-utm.vercel.app`).
2.  **Live Telegram Bot:** Accessible via Telegram (`@LeongConfession_bot`).
3.  **Source Code:** Complete GitHub repository with Frontend and Backend folders.
4.  **Documentation:** This document explaining architecture and usage.

---

## 8. Weekly Progress

### Week 1: Planning & Setup
*   [x] Defined problem statement and requirements.
*   [x] Set up GitHub repository.
*   [x] Obtained API keys (Telegram & Gemini).

### Week 2: Frontend Development
*   [x] Built the React UI structure.
*   [x] Implemented Tailwind CSS styling (Dark Mode/Glassmorphism).
*   [x] Created interaction logic (Mode selection -> Bot Link).
*   [x] Deployed frontend to Vercel.

### Week 3: Backend Logic & Bot
*   [x] Set up Telethon client.
*   [x] Implemented `/start` and `/help` commands.
*   [x] Created logic for handling text and image inputs.
*   [x] Established connection to the Public Channel.

### Week 4: AI Integration & Testing
*   [x] Integrated Google Gemini SDK.
*   [x] Developed prompt engineering for safety checks.
*   [x] Tested with various image types (Safe vs. Unsafe).
*   [ ] Final bug fixes and code cleanup.

### Week 5: Final Presentation
*   [ ] Documentation finalization.
*   [ ] Live demo preparation.

---

## 9. References

### Frontend Development
*   **React Documentation:** [https://react.dev/](https://react.dev/)
*   **Tailwind CSS Documentation:** [https://tailwindcss.com/docs](https://tailwindcss.com/docs)
*   **Vite Guide:** [https://vitejs.dev/guide/](https://vitejs.dev/guide/)
*   **YouTube Tutorial:** [React JS Crash Course 2024](https://www.youtube.com/watch?v=w7ejDZ8SWv8)

### Backend Development (Python & Telegram)
*   **Telethon Library Docs:** [https://docs.telethon.dev/en/stable/](https://docs.telethon.dev/en/stable/)
*   **Python `asyncio` Library:** [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)
*   **YouTube Tutorial:** [Python Telegram Bot Tutorial](https://www.youtube.com/watch?v=PTAkiukJO7k)

### Artificial Intelligence
*   **Google Gemini API Docs:** [https://ai.google.dev/docs](https://ai.google.dev/docs)
*   **Prompt Engineering Guide:** [https://www.promptingguide.ai/](https://www.promptingguide.ai/)
*   **YouTube Tutorial:** [Google Gemini API Crash Course](https://www.youtube.com/watch?v=_jgb_2TqGfY)
