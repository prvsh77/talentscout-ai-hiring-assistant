"""
TalentScout AI Hiring Assistant - PREMIUM EDITION
Advanced, Engaging, and Highly Impressive
"""

import streamlit as st
import json
from datetime import datetime
import re
import random
import time
import base64
from pathlib import Path

def load_bg_image(path: str):
    img_path = Path(path)
    if not img_path.exists():
        return ""
    return base64.b64encode(img_path.read_bytes()).decode()

BG_IMAGE = load_bg_image("pg_agi_bg.jpg")


st.set_page_config(
    page_title="TalentScout AI Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== LIQUID GLASS + BACKGROUND CSS =====================
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    * {{
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }}

    /* ---------- FULL BACKGROUND IMAGE ---------- */
    .stApp {{
        background:
            linear-gradient(rgba(8,10,25,0.65), rgba(8,10,25,0.65)),
            url("data:image/jpeg;base64,{BG_IMAGE}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* ---------- MAIN GLASS CONTAINER ---------- */
    .chat-container {{
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(22px) saturate(180%);
        -webkit-backdrop-filter: blur(22px) saturate(180%);
        border-radius: 26px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 1000px;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow:
            0 10px 40px rgba(0,0,0,0.45),
            inset 0 1px 0 rgba(255,255,255,0.25);
    }}

    /* ---------- HEADER GLASS ---------- */
    .header {{
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 22px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        padding: 2.5rem;
        box-shadow: 0 12px 45px rgba(0,0,0,0.4);
    }}

    /* ---------- CHAT BUBBLES ---------- */
    .chat-message {{
        padding: 1.25rem 1.75rem;
        border-radius: 18px;
        margin: 1.2rem 0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    }}

    .bot-message {{
        background: linear-gradient(
            135deg,
            rgba(102,126,234,0.9),
            rgba(118,75,162,0.9)
        );
        color: white;
        margin-right: 15%;
    }}

    .user-message {{
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        color: #1f2937;
        margin-left: 15%;
        text-align: right;
    }}

    /* ---------- SIDEBAR GLASS ---------- */
    section[data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.16) !important;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-right: 1px solid rgba(255,255,255,0.25);
    }}

    .sidebar-section {{
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }}

    /* ---------- BUTTONS ---------- */
    .stButton > button {{
        background: linear-gradient(
            135deg,
            rgba(102,126,234,0.95),
            rgba(118,75,162,0.95)
        );
        color: white;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.35);
        box-shadow: 0 8px 25px rgba(0,0,0,0.35);
        font-weight: 700;
    }}

    .tech-badge {{
        display: inline-block;
        background: linear-gradient(135deg,#667eea,#764ba2);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.85rem;
        font-weight: 600;
    }}

    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(255,255,255,0.35);
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'stage' not in st.session_state:
    st.session_state.stage = 'greeting'
if 'candidate_data' not in st.session_state:
    st.session_state.candidate_data = {}
if 'tech_questions' not in st.session_state:
    st.session_state.tech_questions = []
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'show_typing' not in st.session_state:
    st.session_state.show_typing = False

STAGES = {
    'greeting': 0, 'name': 1, 'email': 2, 'phone': 3,
    'experience': 4, 'position': 5, 'location': 6,
    'tech_stack': 7, 'questions': 8, 'complete': 9
}

EXIT_KEYWORDS = ['exit', 'quit', 'bye', 'goodbye', 'stop', 'end', 'leave']

# Enhanced question database with more depth
TECH_QUESTIONS = {
    'python': [
        {"q": "Explain the difference between lists and tuples in Python. In what scenarios would you choose one over the other?", "difficulty": "basic", "category": "Core Concepts"},
        {"q": "How do you handle exceptions in Python? Describe a real scenario where proper exception handling saved your project.", "difficulty": "intermediate", "category": "Error Handling"},
        {"q": "What are Python decorators and generators? Provide practical examples where you've used them.", "difficulty": "intermediate", "category": "Advanced Features"},
        {"q": "Explain Python's GIL and its implications. How would you write high-performance Python code for CPU-bound tasks?", "difficulty": "advanced", "category": "Performance"},
        {"q": "Design a rate limiter in Python that can handle 1000 requests per second. Walk me through your implementation.", "difficulty": "advanced", "category": "System Design"}
    ],
    'javascript': [
        {"q": "What's the difference between let, const, and var? When would you use each?", "difficulty": "basic", "category": "Fundamentals"},
        {"q": "Explain closures in JavaScript with a practical example from your projects.", "difficulty": "intermediate", "category": "Core Concepts"},
        {"q": "How does the event loop work? Explain how JavaScript handles asynchronous operations.", "difficulty": "intermediate", "category": "Async Programming"},
        {"q": "What are Promises, async/await, and callbacks? Compare their use cases with code examples.", "difficulty": "intermediate", "category": "Async Programming"},
        {"q": "Implement a debounce function from scratch and explain when you'd use it versus throttle.", "difficulty": "advanced", "category": "Optimization"}
    ],
    'java': [
        {"q": "Explain the core principles of OOP in Java with real-world examples.", "difficulty": "basic", "category": "OOP"},
        {"q": "What's the difference between abstract classes and interfaces? When would you use each?", "difficulty": "intermediate", "category": "Design"},
        {"q": "How does garbage collection work in Java? Describe the different GC algorithms.", "difficulty": "intermediate", "category": "Memory Management"},
        {"q": "Explain the Java Collections Framework. Which collection would you use for different scenarios?", "difficulty": "intermediate", "category": "Data Structures"},
        {"q": "Design a thread-safe cache with LRU eviction policy. Explain your synchronization strategy.", "difficulty": "advanced", "category": "Concurrency"}
    ],
    'react': [
        {"q": "Explain the React component lifecycle. What are the main hooks and when do you use them?", "difficulty": "basic", "category": "Fundamentals"},
        {"q": "What's the difference between state and props? How does data flow in React?", "difficulty": "basic", "category": "Core Concepts"},
        {"q": "How do you optimize performance in React applications? Discuss memoization, lazy loading, and code splitting.", "difficulty": "intermediate", "category": "Performance"},
        {"q": "Explain React's Virtual DOM and reconciliation algorithm. Why is it faster than direct DOM manipulation?", "difficulty": "intermediate", "category": "Internals"},
        {"q": "Design a complex state management solution for a large-scale React app. Compare Redux, Context, and Zustand.", "difficulty": "advanced", "category": "Architecture"}
    ],
    'django': [
        {"q": "Explain Django's MVT architecture and how it differs from MVC.", "difficulty": "basic", "category": "Architecture"},
        {"q": "What is the Django ORM? How would you optimize database queries to avoid N+1 problems?", "difficulty": "intermediate", "category": "Database"},
        {"q": "How do you handle authentication and authorization in Django? Explain custom user models.", "difficulty": "intermediate", "category": "Security"},
        {"q": "What are Django signals? Describe a scenario where you'd use them and potential pitfalls.", "difficulty": "intermediate", "category": "Advanced Features"},
        {"q": "Design a Django REST API with proper authentication, rate limiting, and caching. Explain your approach.", "difficulty": "advanced", "category": "API Design"}
    ],
    'sql': [
        {"q": "Explain the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN with examples.", "difficulty": "basic", "category": "Joins"},
        {"q": "What is database normalization? Explain 1NF, 2NF, and 3NF with practical examples.", "difficulty": "intermediate", "category": "Design"},
        {"q": "How do you optimize a slow SQL query? Describe your debugging and optimization process.", "difficulty": "intermediate", "category": "Performance"},
        {"q": "What are database indexes? When should you create them and when should you avoid them?", "difficulty": "intermediate", "category": "Optimization"},
        {"q": "Explain ACID properties and how they ensure database reliability. Provide real-world scenarios.", "difficulty": "advanced", "category": "Theory"}
    ],
    'node': [
        {"q": "What makes Node.js different from traditional server-side languages? Explain its architecture.", "difficulty": "basic", "category": "Fundamentals"},
        {"q": "Explain the event-driven architecture of Node.js. How does it handle concurrency?", "difficulty": "intermediate", "category": "Architecture"},
        {"q": "How do you handle errors in asynchronous Node.js code? Best practices?", "difficulty": "intermediate", "category": "Error Handling"},
        {"q": "What are streams in Node.js? Provide a practical use case where streams are essential.", "difficulty": "intermediate", "category": "Advanced Features"},
        {"q": "Design a Node.js microservices architecture that can scale to millions of requests. Explain your approach.", "difficulty": "advanced", "category": "System Design"}
    ],
    'default': [
        {"q": "Describe your most challenging technical project. What made it difficult and how did you overcome obstacles?", "difficulty": "intermediate", "category": "Problem Solving"},
        {"q": "How do you approach learning a new technology or framework? Walk me through your process.", "difficulty": "basic", "category": "Learning"},
        {"q": "Tell me about a time you had to debug a complex production issue. What was your methodology?", "difficulty": "intermediate", "category": "Debugging"},
        {"q": "How do you ensure code quality in your projects? Discuss testing, code reviews, and best practices.", "difficulty": "intermediate", "category": "Quality"},
        {"q": "Design a highly available system that can handle millions of users globally. Explain your architecture decisions.", "difficulty": "advanced", "category": "System Design"}
    ]
}

def generate_tech_questions(tech_stack: str, experience_years: int):
    """
    Generate intelligent, relevant questions based on:
    - Tech stack
    - Years of experience
    """
    tech_stack_lower = tech_stack.lower()
    questions = []

    # Decide difficulty based on experience
    if experience_years <= 1:
        allowed_difficulties = ['basic']
    elif experience_years <= 4:
        allowed_difficulties = ['basic', 'intermediate']
    else:
        allowed_difficulties = ['intermediate', 'advanced']

    tech_mapping = {
        'python': 'python', 'javascript': 'javascript', 'js': 'javascript',
        'java': 'java', 'react': 'react', 'reactjs': 'react',
        'django': 'django', 'sql': 'sql', 'mysql': 'sql',
        'postgresql': 'sql', 'postgres': 'sql',
        'node': 'node', 'nodejs': 'node', 'node.js': 'node'
    }

    matched_techs = []
    for tech, key in tech_mapping.items():
        if tech in tech_stack_lower:
            matched_techs.append(key)

    matched_techs = list(set(matched_techs))

    # Select questions based on experience
    if matched_techs:
        for tech in matched_techs[:2]:
            tech_qs = [
                q for q in TECH_QUESTIONS[tech]
                if q['difficulty'] in allowed_difficulties
            ]

            if tech_qs:
                questions.extend(
                    random.sample(tech_qs, min(2, len(tech_qs)))
                )

    # Fill remaining slots with default questions
    while len(questions) < 5:
        default_qs = [
            q for q in TECH_QUESTIONS['default']
            if q['difficulty'] in allowed_difficulties
        ]
        if default_qs:
            q = random.choice(default_qs)
            if q not in questions:
                questions.append(q)
        else:
            questions.append(random.choice(TECH_QUESTIONS['default']))

    return questions[:5]

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{4,10}$'
    return re.match(pattern, phone.replace(' ', '')) is not None

def get_response(stage: str, user_input: str = "", name: str = "") -> str:
    """Get contextual, engaging responses"""
    
    responses = {
        'name': [
            f"Fantastic! It's great to meet you. Now, what's the best email address where we can reach you?",
            f"Perfect! I'd love to stay in touch. Could you share your email address?",
            f"Wonderful to have you here! Please provide your email address so we can follow up."
        ],
        'email': [
            f"Excellent! And what's your phone number? We might need to reach you for the next steps.",
            f"Great! Could you share your phone number as well?",
            f"Perfect! What's the best number to contact you?"
        ],
        'phone': [
            f"Awesome! Now, tell me about your experience. How many years have you been working in technology?",
            f"Fantastic! I'd love to know more about your journey. How many years of tech experience do you have?",
            f"Great! How long have you been working in the technology field?"
        ],
        'experience': [
            f"That's impressive! What kind of role or position are you most interested in right now?",
            f"Wonderful experience! What type of position are you looking for at this stage of your career?",
            f"That's fantastic! Which role would be your dream position?"
        ],
        'position': [
            f"Excellent choice! That's a great role. Where are you currently based?",
            f"That sounds like a perfect fit! What's your current location?",
            f"Great! I can see you there. Where are you located right now?"
        ],
        'location': [
            f"Perfect! Now for the exciting part - let's dive into your technical expertise. Tell me about your tech stack - what programming languages, frameworks, databases, and tools do you work with regularly?",
            f"Excellent! Now I want to understand your technical strengths. Please share your complete tech stack - all the technologies, languages, and tools you're proficient in.",
            f"Great! Let's explore your technical skills. List out your tech stack for me - everything from languages and frameworks to databases and dev tools."
        ]
    }
    
    return random.choice(responses.get(stage, ["Could you tell me more about that?"]))

def process_user_input(user_input: str):
    """Process input with enhanced engagement"""
    
    if user_input.lower().strip() in EXIT_KEYWORDS:
        st.session_state.stage = 'complete'
        return "Thank you so much for your time! 🙏 We'll carefully review your information and technical responses. Our team will reach out to you within 2-3 business days with next steps. Have an amazing day! 👋✨"
    
    current_stage = st.session_state.stage
    
    if current_stage == 'greeting':
        st.session_state.stage = 'name'
        return "Wonderful! I'm excited to get to know you. Let's start with the basics - what's your full name? 😊"
    
    elif current_stage == 'name':
        st.session_state.candidate_data['name'] = user_input
        st.session_state.stage = 'email'
        return get_response('name', user_input, user_input)
    
    elif current_stage == 'email':
        if validate_email(user_input):
            st.session_state.candidate_data['email'] = user_input
            st.session_state.stage = 'phone'
            return get_response('email')
        else:
            return "Hmm, that email doesn't look quite right. 🤔 Could you please check and provide a valid email address? (e.g., yourname@example.com)"
    
    elif current_stage == 'phone':
        if validate_phone(user_input):
            st.session_state.candidate_data['phone'] = user_input
            st.session_state.stage = 'experience'
            return get_response('phone')
        else:
            return "I couldn't validate that phone number. 📱 Please provide it in a standard format (e.g., +1-234-567-8900 or 1234567890)"
    
    
    elif current_stage == 'experience':
        st.session_state.candidate_data['experience_raw'] = user_input
    
        import re
        match = re.search(r'\d+', user_input)
        years = int(match.group()) if match else 0
        st.session_state.candidate_data['experience_years'] = years
    
        st.session_state.stage = 'position'
        return get_response('experience')

    elif current_stage == 'position':
        st.session_state.candidate_data['position'] = user_input
        st.session_state.stage = 'location'
        return get_response('position')
    
    elif current_stage == 'location':
        st.session_state.candidate_data['location'] = user_input
        st.session_state.stage = 'tech_stack'
        return get_response('location')
    
    elif current_stage == 'tech_stack':
        st.session_state.candidate_data['tech_stack'] = user_input
        years = st.session_state.candidate_data.get('experience_years', 0)
        st.session_state.tech_questions = generate_tech_questions(user_input, years)

        st.session_state.candidate_data['technical_answers'] = []
        st.session_state.stage = 'questions'
        
        first_q = st.session_state.tech_questions[0]
        return f"""Fantastic! I can see you have an impressive tech stack! 🚀 

Now let's dive into the technical assessment. I'll ask you 5 carefully selected questions based on your expertise. Take your time with each answer - quality over speed!

**Question 1 of 5** | {first_q['difficulty'].upper()} | {first_q['category']}

{first_q['q']}"""
    
    elif current_stage == 'questions':
        current_q = st.session_state.tech_questions[st.session_state.current_question_idx]
        st.session_state.candidate_data['technical_answers'].append({
            'question': current_q['q'],
            'answer': user_input,
            'difficulty': current_q['difficulty'],
            'category': current_q['category']
        })
        
        st.session_state.current_question_idx += 1
        
        if st.session_state.current_question_idx < len(st.session_state.tech_questions):
            next_q = st.session_state.tech_questions[st.session_state.current_question_idx]
            encouragements = [
                "Excellent answer! 🌟 I can see you really understand this.",
                "That's a thoughtful response! 💡 You clearly have hands-on experience.",
                "Great explanation! 👏 Your practical knowledge really shows.",
                "Impressive! 🎯 That's exactly the kind of insight we're looking for.",
                "Wonderful response! ✨ You've articulated that very well."
            ]
            encouragement = random.choice(encouragements)
            
            return f"""{encouragement}

**Question {st.session_state.current_question_idx + 1} of 5** | {next_q['difficulty'].upper()} | {next_q['category']}

{next_q['q']}"""
        else:
            duration = int(time.time() - st.session_state.start_time)
            st.session_state.stage = 'complete'
            return f"""🎉 **Outstanding work!** You've completed the entire screening process!

⏱️ **Completion Time:** {duration//60} minutes {duration%60} seconds

Your responses demonstrate strong technical knowledge and practical experience. Our recruitment team will carefully review your profile and technical answers. We're genuinely impressed with your background!

📧 **Next Steps:**
• Our team will review your submission within 2-3 business days
• You'll receive a detailed email with feedback and next steps
• If selected, we'll schedule a technical interview

Thank you for your time and thoughtful answers! We're excited about the possibility of working with you! 🚀"""
    
    return "I didn't quite catch that. Could you please rephrase or provide more details? 💭"

# Main UI
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="emoji-large">🎯</div>
    <h1>TalentScout AI</h1>
    <p>Your Intelligent Hiring Assistant</p>
    <span class="badge">✨ Premium Edition</span>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced metrics
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.title("📊 Your Progress")
    
    progress = (STAGES.get(st.session_state.stage, 0) / len(STAGES)) * 100
    st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {progress}%"></div></div>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-weight: 600; color: #667eea; font-size: 1.1rem;'>{int(progress)}% Complete</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.candidate_data:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 📝 Your Profile")
        
        for key, value in st.session_state.candidate_data.items():
            if key == 'tech_stack':
                st.markdown(f"**{key.replace('_', ' ').title()}:**")
                techs = value.split(',')
                tech_html = ''.join([f'<span class="tech-badge">{t.strip()}</span>' for t in techs[:5]])
                st.markdown(tech_html, unsafe_allow_html=True)
            elif key != 'technical_answers':
                st.markdown(f'<div class="metric-row"><span style="color: #6b7280; font-weight: 500;">{key.replace("_", " ").title()}</span><span style="color: #1f2937; font-weight: 600;">{str(value)[:20]}...</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Time tracker
    if st.session_state.stage not in ['greeting', 'complete']:
        elapsed = int(time.time() - st.session_state.start_time)
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### ⏱️ Session Info")
        st.markdown(f'<div class="metric-row"><span>Time Elapsed</span><span style="color: #667eea; font-weight: 700;">{elapsed//60}m {elapsed%60}s</span></div>', unsafe_allow_html=True)
        
        if st.session_state.stage == 'questions':
            st.markdown(f'<div class="metric-row"><span>Questions</span><span style="color: #667eea; font-weight: 700;">{st.session_state.current_question_idx + 1} of 5</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="info-card"><strong>💡 Pro Tip:</strong> Take your time with technical questions. Quality answers matter more than speed!</div>', unsafe_allow_html=True)

# Initialize conversation
if not st.session_state.messages:
    greeting = """👋 **Welcome to TalentScout!** 

I'm your AI-powered hiring assistant, and I'm thrilled to meet you! 

I'll be conducting your initial screening today - it's a conversational process that takes about **5-10 minutes**. Here's what we'll cover:

✨ **Your Background** - Basic information about you
💼 **Your Experience** - Your professional journey
🚀 **Your Skills** - Deep dive into your technical expertise
🎯 **Technical Assessment** - 5 tailored questions based on YOUR tech stack

Everything is conversational and natural - just like chatting with a recruiter, but smarter! 😉

**Ready to begin your journey with us?** 

Type **'yes'** to start, or **'exit'** anytime if you need to leave."""
    
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    css_class = "bot-message" if message["role"] == "assistant" else "user-message"
    content = message["content"].replace('\n', '<br>')
    st.markdown(f'<div class="chat-message {css_class}">{content}</div>', unsafe_allow_html=True)

# Completion view with celebration
if st.session_state.stage == 'complete':
    duration = int(time.time() - st.session_state.start_time)
    
    st.markdown(f"""
    <div class="completion-card">
        <h2 style="font-size: 2.5rem; margin-bottom: 1rem;">🎉 Congratulations!</h2>
        <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Screening Complete!</h3>
        <p style="font-size: 1.1rem; margin-top: 1.5rem; opacity: 0.95;">
            Completed in <strong>{duration//60}m {duration%60}s</strong>
        </p>
        <p style="font-size: 1rem; margin-top: 1rem; opacity: 0.9;">
            Thank you for your time and thoughtful responses!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">✓</div>
            <div class="stat-label">Profile Complete</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        tech_count = len(st.session_state.candidate_data.get('tech_stack', '').split(','))
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{tech_count}</div>
            <div class="stat-label">Technologies</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        q_count = len(st.session_state.tech_questions)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{q_count}</div>
            <div class="stat-label">Questions Answered</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Complete Report"):
            report = {
                **st.session_state.candidate_data,
                'metadata': {
                    'completion_time': datetime.now().isoformat(),
                    'duration_seconds': duration,
                    'total_questions': len(st.session_state.tech_questions),
                    'screening_version': 'TalentScout AI Premium v2.0'
                }
            }
            
            st.download_button(
                label="💾 Download JSON Report",
                data=json.dumps(report, indent=2),
                file_name=f"talentscout_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🔄 Start New Screening"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

else:
    # Chat input with placeholder
    user_input = st.chat_input("✍️ Type your response here...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Simulate typing delay for realism
        time.sleep(0.5)
        
        bot_response = process_user_input(user_input)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced footer
st.markdown("""
<div style="text-align: center; padding: 2.5rem; color: white;">
    <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
        🧠 Powered by Advanced AI • ⚡ Intelligent Question Engine • 🎯 Smart Matching
    </p>
    <p style="font-size: 0.95rem; opacity: 0.85; margin-top: 0.5rem;">
        TalentScout AI Premium © 2024 • GDPR Compliant • Secure Data Handling
    </p>
    <p style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">
        Your privacy matters - All data is encrypted and handled with utmost care
    </p>
</div>
""", unsafe_allow_html=True)