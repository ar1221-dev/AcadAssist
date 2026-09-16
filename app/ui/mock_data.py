"""Mock data store for AcadAssist UI prototype.

Centralizes all UI data models, ensuring clean separation between frontend
and future backend integrations.
"""

from typing import Any, Dict, List

USER_PROFILE: Dict[str, Any] = {
    "name": "Raj",
    "full_name": "Rajesh Sharma",
    "role": "",
    "field": "",
    "academic_level": "",
    "email": "",
    "location": "",
    "member_since": "",
    "bio": "",
    "tags": [],
    "quote": "",
    "streak_days": 0,
    "streak_status": "",
    "avatar_name": "Raj",
    "cgpa": "",
}

STATS_SUMMARY: Dict[str, Any] = {
    "day_streak": 12,
    "topics_completed": 5,
    "hours_studied": 6.5,
    "average_score": 78,
    "notes_learned": 82,
    "questions_practiced": 143,
    "total_study_time": 24.5,
    "overall_progress": 78,
    "notes_increase": "+12% this month",
    "questions_increase": "+28% this month",
    "study_time_increase": "+16% this month",
    "progress_increase": "+10% this month",
}

SUBJECTS: List[Dict[str, Any]] = [
    {
        "id": "dsa",
        "name": "Data Structures",
        "full_name": "Data Structures & Algorithms",
        "documents_count": 12,
        "progress": 76,
        "topics_completed": 8,
        "total_topics": 12,
        "color": "#2d5f47",
        "tag": "DSA",
    },
    {
        "id": "dbms",
        "name": "DBMS",
        "full_name": "Database Management Systems",
        "documents_count": 8,
        "progress": 61,
        "topics_completed": 5,
        "total_topics": 11,
        "color": "#e07a5f",
        "tag": "DBMS",
    },
    {
        "id": "cn",
        "name": "Computer Networks",
        "full_name": "Computer Networks",
        "documents_count": 10,
        "progress": 48,
        "topics_completed": 4,
        "total_topics": 10,
        "color": "#6366f1",
        "tag": "CN",
    },
    {
        "id": "java",
        "name": "Java Programming",
        "full_name": "Java Object Oriented Programming",
        "documents_count": 6,
        "progress": 35,
        "topics_completed": 3,
        "total_topics": 9,
        "color": "#d97706",
        "tag": "Java",
    },
    {
        "id": "os",
        "name": "Operating Systems",
        "full_name": "Operating Systems & Concurrency",
        "documents_count": 7,
        "progress": 42,
        "topics_completed": 4,
        "total_topics": 10,
        "color": "#0ea5e9",
        "tag": "OS",
    },
    {
        "id": "math",
        "name": "Mathematics",
        "full_name": "Discrete Mathematics & Probability",
        "documents_count": 9,
        "progress": 76,
        "topics_completed": 7,
        "total_topics": 9,
        "color": "#8b5cf6",
        "tag": "Math",
    },
]

TODAY_STUDY_PLAN: List[Dict[str, Any]] = [
    {
        "id": "plan-1",
        "time": "09:00 AM",
        "title": "Linked Lists – Revision",
        "description": "Recap key concepts and solve 5 problems",
        "subject": "Data Structures",
        "tag": "DSA",
        "duration": "45 min",
        "status": "completed",
        "action_label": "Review",
        "color": "#2d5f47",
        "icon": "file-text",
    },
    {
        "id": "plan-2",
        "time": "11:00 AM",
        "title": "Binary Trees – Practice",
        "description": "Solve mixed questions on traversals & BST",
        "subject": "Data Structures",
        "tag": "DSA",
        "duration": "30 min",
        "status": "pending",
        "action_label": "Start",
        "color": "#e07a5f",
        "icon": "code",
    },
    {
        "id": "plan-3",
        "time": "03:00 PM",
        "title": "Normalization",
        "description": "Read notes and make summary (1NF to BCNF)",
        "subject": "DBMS",
        "tag": "DBMS",
        "duration": "40 min",
        "status": "pending",
        "action_label": "Start",
        "color": "#3b82f6",
        "icon": "database",
    },
    {
        "id": "plan-4",
        "time": "07:00 PM",
        "title": "Quick Quiz",
        "description": "10 questions • Mixed topics across semester",
        "subject": "Mixed",
        "tag": "Mixed",
        "duration": "20 min",
        "status": "pending",
        "action_label": "Start",
        "color": "#f59e0b",
        "icon": "check-square",
    },
]

PLANNER_TIMELINE_TASKS: List[Dict[str, Any]] = [
    {
        "id": "pt-1",
        "time": "08:00 AM",
        "title": "Quick Review",
        "description": "Revise Linked List basics",
        "subject_tag": "DSA",
        "duration": "30 min",
        "completed": True,
        "type": "study",
    },
    {
        "id": "pt-2",
        "time": "09:00 AM",
        "title": "Study Session",
        "description": "Linked Lists – Theory & Pointers",
        "subject_tag": "DSA",
        "duration": "45 min",
        "completed": True,
        "type": "study",
    },
    {
        "id": "pt-3",
        "time": "11:00 AM",
        "title": "Practice Questions",
        "description": "Solve 10 medium problems",
        "subject_tag": "DSA",
        "duration": "45 min",
        "completed": False,
        "type": "practice",
    },
    {
        "id": "pt-4",
        "time": "01:00 PM",
        "title": "Break",
        "description": "Lunch & relax",
        "subject_tag": "Break",
        "duration": "1 hr",
        "completed": True,
        "type": "break",
    },
    {
        "id": "pt-5",
        "time": "02:00 PM",
        "title": "Read Notes",
        "description": "Normalization (Chapter 2)",
        "subject_tag": "DBMS",
        "duration": "40 min",
        "completed": False,
        "type": "study",
    },
    {
        "id": "pt-6",
        "time": "04:00 PM",
        "title": "Mock Test",
        "description": "Mixed Topics (20 Questions)",
        "subject_tag": "Mixed",
        "duration": "30 min",
        "completed": False,
        "type": "quiz",
    },
    {
        "id": "pt-7",
        "time": "07:00 PM",
        "title": "Revise & Summarize",
        "description": "Make short notes on Subnetting",
        "subject_tag": "CN",
        "duration": "30 min",
        "completed": False,
        "type": "study",
    },
]

UPCOMING_EXAMS: List[Dict[str, Any]] = [
    {
        "id": "exam-1",
        "subject": "Data Structures",
        "exam_name": "Data Structures (End Sem)",
        "days_left": 8,
        "date_str": "24 Sep 2026",
        "urgency": "high",
        "icon": "book-open",
    },
    {
        "id": "exam-2",
        "subject": "DBMS",
        "exam_name": "DBMS (End Sem)",
        "days_left": 14,
        "date_str": "30 Sep 2026",
        "urgency": "medium",
        "icon": "database",
    },
    {
        "id": "exam-3",
        "subject": "Computer Networks",
        "exam_name": "Computer Networks",
        "days_left": 21,
        "date_str": "7 Oct 2026",
        "urgency": "normal",
        "icon": "share-2",
    },
]

UPCOMING_DEADLINES: List[Dict[str, Any]] = [
    {
        "title": "DSA Internal Test",
        "days_left": "3 days left",
        "date_str": "19 Sep 2026",
        "urgency": "urgent",
    },
    {
        "title": "Data Structures (End Sem)",
        "days_left": "8 days left",
        "date_str": "24 Sep 2026",
        "urgency": "high",
    },
    {
        "title": "DBMS (End Sem)",
        "days_left": "14 days left",
        "date_str": "30 Sep 2026",
        "urgency": "medium",
    },
    {
        "title": "Computer Networks",
        "days_left": "21 days left",
        "date_str": "7 Oct 2026",
        "urgency": "normal",
    },
]

KNOWLEDGE_MATERIALS: List[Dict[str, Any]] = [
    {
        "name": "Linked_List_Notes.pdf",
        "subject": "Data Structures",
        "type": "PDF",
        "size": "2.4 MB",
        "added_on": "15 Sep 2026",
        "status": "Ready",
        "starred": True,
    },
    {
        "name": "Trees_Lecture.pptx",
        "subject": "Data Structures",
        "type": "PPT",
        "size": "4.1 MB",
        "added_on": "12 Sep 2026",
        "status": "Ready",
        "starred": False,
    },
    {
        "name": "Normalization_Notes.pdf",
        "subject": "DBMS",
        "type": "PDF",
        "size": "1.8 MB",
        "added_on": "10 Sep 2026",
        "status": "Ready",
        "starred": False,
    },
    {
        "name": "SQL_Practice.docx",
        "subject": "DBMS",
        "type": "DOCX",
        "size": "320 KB",
        "added_on": "9 Sep 2026",
        "status": "Ready",
        "starred": False,
    },
    {
        "name": "CN_Unit1_Introduction.pdf",
        "subject": "Computer Networks",
        "type": "PDF",
        "size": "3.2 MB",
        "added_on": "7 Sep 2026",
        "status": "Ready",
        "starred": False,
    },
    {
        "name": "Java_OOP_Concepts.docx",
        "subject": "Java Programming",
        "type": "DOCX",
        "size": "850 KB",
        "added_on": "5 Sep 2026",
        "status": "Ready",
        "starred": False,
    },
]

RECENT_ACTIVITIES: List[Dict[str, Any]] = [
    {
        "icon_color": "#10b981",
        "text": "Completed quiz on Stacks",
        "time": "2 hours ago",
        "action": "quiz",
    },
    {
        "icon_color": "#3b82f6",
        "text": "Uploaded DBMS Notes.pdf",
        "time": "5 hours ago",
        "action": "upload",
    },
    {
        "icon_color": "#8b5cf6",
        "text": "Studied Trees – 30 minutes",
        "time": "1 day ago",
        "action": "study",
    },
    {
        "icon_color": "#f59e0b",
        "text": "Asked question (AI Assistant)",
        "time": "1 day ago",
        "action": "chat",
    },
    {
        "icon_color": "#10b981",
        "text": "Completed reading Java_Notes.pdf",
        "time": "2 days ago",
        "action": "read",
    },
]

ASSESSMENT_PERFORMANCE: Dict[str, Any] = {
    "average_score": 78,
    "delta": "+12% from last month",
    "questions_attempted": 143,
    "correct_answers": 118,
    "topics_covered": 25,
}

RECENT_ATTEMPTS: List[Dict[str, Any]] = [
    {
        "topic": "Linked Lists",
        "difficulty": "Medium",
        "score_fraction": "8 / 10",
        "percentage": "80%",
        "date": "16 Sep 2026",
        "status": "passed",
    },
    {
        "topic": "DBMS",
        "difficulty": "Hard",
        "score_fraction": "6 / 10",
        "percentage": "60%",
        "date": "14 Sep 2026",
        "status": "average",
    },
    {
        "topic": "Trees",
        "difficulty": "Medium",
        "score_fraction": "7 / 10",
        "percentage": "70%",
        "date": "12 Sep 2026",
        "status": "passed",
    },
    {
        "topic": "Computer Networks",
        "difficulty": "Easy",
        "score_fraction": "9 / 10",
        "percentage": "90%",
        "date": "10 Sep 2026",
        "status": "excellent",
    },
]

POPULAR_PRACTICE_SETS: List[Dict[str, Any]] = [
    {
        "title": "DSA Essentials",
        "subtitle": "Arrays, Linked Lists, Stacks, Queues",
        "questions_count": 50,
        "type": "Mixed",
        "icon": "share-2",
        "color": "#f59e0b",
    },
    {
        "title": "DBMS Fundamentals",
        "subtitle": "Normalization, SQL, Transactions",
        "questions_count": 40,
        "type": "Mixed",
        "icon": "database",
        "color": "#3b82f6",
    },
    {
        "title": "Networks Basics",
        "subtitle": "OSI, TCP/IP, Routing",
        "questions_count": 40,
        "type": "Mixed",
        "icon": "wifi",
        "color": "#6366f1",
    },
    {
        "title": "Quick Revision",
        "subtitle": "Mixed topics from all subjects",
        "questions_count": 30,
        "type": "Mixed",
        "icon": "zap",
        "color": "#ef4444",
    },
]

STUDY_GOALS: List[Dict[str, Any]] = []

MILESTONES: List[Dict[str, Any]] = [
    {
        "title": "Completed 50 practice questions",
        "date": "5 Sep 2026",
        "completed": True,
    },
    {
        "title": "7 day study streak",
        "date": "8 Sep 2026",
        "completed": True,
    },
    {
        "title": "Finished Linked Lists module",
        "date": "10 Sep 2026",
        "completed": True,
    },
    {
        "title": "Complete 1 subject",
        "date": "Target: 20 Sep 2026",
        "completed": False,
    },
]

BADGES: List[Dict[str, Any]] = [
    {"name": "7-Day Streak", "icon": "calendar", "color": "#10b981", "unlocked": True},
    {"name": "100 Questions", "icon": "award", "color": "#3b82f6", "unlocked": True},
    {"name": "First Note", "icon": "book-open", "color": "#8b5cf6", "unlocked": True},
    {"name": "5 Subjects", "icon": "grid", "color": "#f59e0b", "unlocked": True},
    {"name": "Assessment Pro", "icon": "shield", "color": "#9ca3af", "unlocked": False},
]

HELP_CATEGORIES: List[Dict[str, Any]] = [
    {
        "title": "Getting Started",
        "description": "Set up your account, explore features, and get started quickly.",
        "icon": "compass",
        "color": "#10b981",
    },
    {
        "title": "My Knowledge",
        "description": "Learn how to upload, organize, and manage your study materials.",
        "icon": "folder",
        "color": "#3b82f6",
    },
    {
        "title": "Assessment",
        "description": "Understand quizzes, test settings, and results.",
        "icon": "check-circle",
        "color": "#f59e0b",
    },
    {
        "title": "Study Planner",
        "description": "Plan your study schedule and manage your goals.",
        "icon": "calendar",
        "color": "#10b981",
    },
    {
        "title": "AI Study Assistant",
        "description": "Get the most out of your AI companion.",
        "icon": "cpu",
        "color": "#8b5cf6",
    },
    {
        "title": "Progress Tracking",
        "description": "Track your learning journey and achievements.",
        "icon": "bar-chart-2",
        "color": "#10b981",
    },
    {
        "title": "Account & Settings",
        "description": "Manage your profile, preferences, and security.",
        "icon": "settings",
        "color": "#3b82f6",
    },
    {
        "title": "Data & Privacy",
        "description": "Learn how your data is protected and managed.",
        "icon": "shield",
        "color": "#10b981",
    },
]

SYSTEM_STATUS_ITEMS: List[Dict[str, str]] = [
    {"name": "Website & App", "status": "Operational"},
    {"name": "AI Assistant", "status": "Operational"},
    {"name": "Quiz & Assessment", "status": "Operational"},
    {"name": "Study Planner", "status": "Operational"},
    {"name": "File Processing", "status": "Operational"},
]

CHAT_HISTORY_INITIAL: List[Dict[str, Any]] = [
    {
        "role": "user",
        "time": "10:14 AM",
        "text": "Explain Normalization in DBMS with examples.",
    },
    {
        "role": "assistant",
        "time": "10:14 AM",
        "text": """Sure! Let's break down **Normalization in DBMS** step by step.

### 1. What is Normalization?
Normalization is the systematic process of organizing data in a relational database to reduce redundancy and improve data integrity. It involves decomposing large, unstructured tables into smaller, well-structured tables while maintaining relationships between them.

### 2. Need for Normalization
- **Avoids data redundancy**: Reduces duplicate storage across records.
- **Prevents update anomalies**: Eliminates insertion, deletion, and modification errors.
- **Maintains data consistency**: Ensures facts are recorded once.
- **Improves query efficiency**: Smaller rows fit better in memory caches.

### 3. Normal Forms (Brief Overview)

| Normal Form | Condition |
| :--- | :--- |
| **1NF** | All attributes have atomic (indivisible) values. No repeating groups. |
| **2NF** | In 1NF + no partial dependency (every non-key attribute depends on the entire primary key). |
| **3NF** | In 2NF + no transitive dependency (non-key attributes cannot depend on other non-key attributes). |
| **BCNF** | Stricter version of 3NF: for every functional dependency $X \\rightarrow Y$, $X$ must be a super key. |
""",
    },
]
