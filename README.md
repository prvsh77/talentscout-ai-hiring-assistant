TalentScout AI – Intelligent Hiring Assistant

TalentScout AI is an AI-powered hiring assistant designed to automate initial technical screening through structured, context-aware conversations.

The system focuses on conversational flow, prompt design principles, and system architecture, rather than raw model calls or external APIs.
It was developed as part of an AI/ML Internship assignment with emphasis on determinism, reliability, and privacy.

Problem

Early-stage technical screening is repetitive, time-consuming, and inconsistent across candidates.
Manual screening also lacks structured evaluation and is difficult to scale.

Solution

TalentScout AI automates first-round screening by:

Collecting essential candidate information

Understanding declared technical expertise

Generating role- and experience-aware technical questions

Maintaining a smooth, human-like conversational flow

Ending the interaction cleanly with clear next steps

The system is fully local, deterministic, and privacy-conscious, making it suitable for early-stage hiring workflows and demos.

System Architecture

The application follows a modular, system-oriented design:

Core Components

UI Layer (Streamlit)

Handles user interaction

Displays chat, progress, and feedback

Conversation Controller

Manages conversation stages

Routes input to the correct handlers

Session State Manager

Maintains multi-turn context

Stores candidate data securely in memory

Question Generation Engine

Matches declared tech stack keywords

Adjusts difficulty based on years of experience

Selects questions deterministically

Key Features
Conversational Hiring Assistant

Friendly onboarding

Natural multi-step dialogue

Graceful exit handling (exit, quit)

Information Gathering

Collects:

Full Name

Email Address

Phone Number

Years of Experience

Desired Role

Location

Complete Tech Stack

Intelligent Question Generation

Generates 3–5 technical questions

Based on:

Declared technologies

Experience level

Covers multiple difficulty levels:

Basic

Intermediate

Advanced

Context Awareness & Fallback Handling

Maintains conversational continuity

Handles unclear input gracefully

Prevents irrelevant or repeated prompts

Graceful Completion

Summarizes screening

Explains next steps

Optional report download

Technology Stack
Category	Tools
Language	Python
Frontend	Streamlit
State Management	Streamlit Session State
Styling	Custom CSS (Glassmorphism)
Data Handling	In-memory (No persistence)

No external APIs or databases are used, ensuring privacy, reliability, and easy local deployment.

Installation & Setup
git clone https://github.com/prvsh77/talentscout-ai-hiring-assistant.git
cd talentscout-ai-hiring-assistant
python -m venv venv


Activate the environment:

Windows

venv\Scripts\activate


macOS / Linux

source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the application:

streamlit run app.py


Open:

http://localhost:8501

Prompt Design Strategy

Although no external LLM API is used, the system mirrors real-world prompt engineering principles through deterministic logic:

Clear intent per conversation stage

Controlled transitions between phases

Experience-aware difficulty selection

Guardrails to prevent topic deviation

This emphasizes:

Specificity

Context preservation

Output control

Safety and predictability

Data Privacy & Security

No permanent data storage

All candidate data remains in session memory

No external network calls

GDPR-conscious by design

Suitable for demos and early-stage hiring workflows.

Challenges & Solutions

Challenge: Maintaining multi-turn context
Solution: Explicit stage-based session state management

Challenge: Generating relevant technical questions
Solution: Keyword-to-question mapping filtered by experience level

Challenge: Avoiding API dependency
Solution: Deterministic question engine that mimics LLM behavior

Future Enhancements

Integration with LLMs (OpenAI, LLaMA, etc.)

Sentiment analysis during interviews

Multilingual support

Recruiter dashboard and analytics

Cloud deployment (AWS / GCP)

Demo

🎥 Walkthrough of the full screening flow and UI:
https://www.loom.com/share/4723fa852386442ba3e3cf4e5dc20378

Repository Structure
├── app.py
├── requirements.txt
├── assets/
│   ├── ui_preview.jpg
│   ├── architecture.png
│   └── background.jpg
└── README.md

Conclusion

TalentScout AI demonstrates:

Applied AI/ML system thinking

Prompt engineering concepts

Conversational system design

Clean, recruiter-friendly UI/UX
