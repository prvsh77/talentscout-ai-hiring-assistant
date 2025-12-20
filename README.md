TalentScout AI – Intelligent Hiring Assistant

TalentScout AI is an AI-powered hiring assistant designed to streamline the initial screening of technical candidates.

It conducts structured, context-aware conversations to gather candidate information and dynamically generate role- and skill-specific technical questions.

This project was developed as part of an AI/ML Intern assignment, with a focus on prompt engineering, conversational flow, and system design rather than raw model calls.



Project Overview
Recruitment teams often spend significant time on repetitive initial screenings.

TalentScout AI automates this process by:

Collecting essential candidate details

Understanding declared technical expertise

Generating relevant technical questions

Maintaining a smooth, human-like conversational flow

Ending the interaction gracefully with clear next steps

The system is privacy-conscious, deterministic, and fully local, making it suitable for early-stage hiring workflows.

---------------------------------------------------------------------------------------------

UI Preview
Screenshots of the application UI
!\[TalentScout AI – UI Preview](assets/ui\_preview.png)



The interface uses a glassmorphism (“liquid glass”) design, enhanced with:

Background visuals

Smooth animations

Clear visual hierarchy

Recruiter-friendly layout

Architecture Overview
High-level system architecture
!\[TalentScout AI – Architecture Diagram](assets/architecture.png)



--------------------------------------------------------------------------------------------

Core Components


UI Layer (Streamlit)

Handles user interaction

Displays chat, progress, and metrics

Conversation Controller

Manages conversation stages

Routes user input to appropriate handlers

Session State Manager

Maintains context across multiple turns

Stores candidate data securely in memory

Question Generation Engine

Matches tech stack keywords

Adjusts difficulty using years of experience

Selects relevant technical questions deterministically

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Key Features

Conversational Hiring Assistant

Friendly greeting and onboarding

Natural, multi-step dialogue

Graceful exit handling (e.g., “exit”, “quit”)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Information Gathering



Collects:

Full Name
Email Address
Phone Number
Years of Experience
Desired Role
Current Location
Complete Tech Stack
Intelligent Question Generation
Generates 3–5 technical questions

Based on:
Declared technologies
Candidate experience level
Covers multiple difficulty levels:
Basic
Intermediate
Advanced

Context Awareness
Maintains conversation flow
Handles follow-up responses correctly
Avoids irrelevant or repeated prompts



Fallback Handling
Provides meaningful responses for unclear input
Prevents conversation derailment



Graceful Completion
Summarizes completion
Explains next steps
Allows report download



Technology Stack

Category	Tools

Language	Python

Frontend	Streamlit

State Management	Streamlit Session State

Styling	Custom CSS (Glassmorphism)

Data Handling	In-memory (No persistence)



No external APIs or databases are used.

This ensures privacy, reliability, and easy local deployment.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Installation \& Setup

1\. Clone the Repository

git clone https://github.com/your-username/talentscout-ai.git

cd talentscout-ai


2\. Create Virtual Environment (Recommended)

python -m venv venv

Activate the environment:
Windows:
venv\\Scripts\\activate

macOS/Linux:
source venv/bin/activate

3\. Install Dependencies

pip install -r requirements.txt


4\. Run the Application

streamlit run app.py


Open your browser at:

http://localhost:8501

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Usage Guide

Launch the application

Start the conversation

Enter requested details step by step

Declare your tech stack (e.g., Python, Django, SQL)

Answer generated technical questions

Complete the screening and download the report (optional)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Prompt Design Strategy

Although no external LLM API is invoked, the prompting logic is simulated deterministically:
Clear intent per stage (name, email, experience, etc.)
Controlled transitions between conversation phases
Experience-aware difficulty selection
Guardrails to prevent topic deviation
This mirrors real-world prompt engineering principles:
Specificity
Context preservation
Output control
Safety and predictability

Data Privacy \& Security
No data is stored permanently
All candidate information exists only in session memory
No external network calls
GDPR-conscious by design

This makes the system suitable for early-stage hiring and demos.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Challenges \& Solutions

Challenge: Maintaining conversation context
Solution:
Used Streamlit session state with explicit stage management.

Challenge: Generating relevant technical questions
Solution:
Mapped tech keywords to curated question banks and filtered by experience level.

Challenge: Avoiding API dependency
Solution:
Designed a deterministic question engine that mimics LLM behavior without external calls.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Future Enhancements

Integration with LLMs (OpenAI, LLaMA, etc.)
Sentiment analysis during interviews
Multilingual support
Recruiter dashboard \& analytics
Cloud deployment (AWS / GCP)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Demo

A short walkthrough demonstrating the full candidate screening flow, dynamic question generation, and UI.

Watch here: https://www.loom.com/share/4723fa852386442ba3e3cf4e5dc20378


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Repository Structure

├── app.py

├── requirements.txt

├── assets/

│   ├── ui\_preview.jpg

│   ├── architecture.png

│   └── background.jpg

├── README.md

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Conclusion

TalentScout AI demonstrates:
Applied AI/ML thinking
Prompt engineering concepts
Conversational system design
Clean UI/UX for hiring workflows

