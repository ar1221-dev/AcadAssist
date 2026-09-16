"""State management layer for AcadAssist UI.

Handles initialization of Streamlit session state from mock data
and provides mutation functions for interactive prototype features.
"""

import time
import copy
import streamlit as st
from typing import Optional, Dict, Any, List

from app.ui.mock_data import (
    USER_PROFILE,
    STATS_SUMMARY,
    SUBJECTS,
    TODAY_STUDY_PLAN,
    PLANNER_TIMELINE_TASKS,
    UPCOMING_EXAMS,
    UPCOMING_DEADLINES,
    KNOWLEDGE_MATERIALS,
    RECENT_ACTIVITIES,
    ASSESSMENT_PERFORMANCE,
    RECENT_ATTEMPTS,
    POPULAR_PRACTICE_SETS,
    STUDY_GOALS,
    MILESTONES,
    BADGES,
    HELP_CATEGORIES,
    SYSTEM_STATUS_ITEMS,
    CHAT_HISTORY_INITIAL,
)

def init_session_state() -> None:
    """Initialize session state with mock data if not already present."""
    if "initialized" not in st.session_state:
        # Core navigation
        st.session_state.current_page = "Dashboard"
        
        # Deep copy mock data so mutations don't affect the static file
        st.session_state.user_profile = copy.deepcopy(USER_PROFILE)
        st.session_state.stats = copy.deepcopy(STATS_SUMMARY)
        st.session_state.subjects = copy.deepcopy(SUBJECTS)
        st.session_state.today_plan = copy.deepcopy(TODAY_STUDY_PLAN)
        st.session_state.planner_tasks = copy.deepcopy(PLANNER_TIMELINE_TASKS)
        st.session_state.upcoming_exams = copy.deepcopy(UPCOMING_EXAMS)
        st.session_state.upcoming_deadlines = copy.deepcopy(UPCOMING_DEADLINES)
        st.session_state.knowledge_materials = copy.deepcopy(KNOWLEDGE_MATERIALS)
        st.session_state.recent_activities = copy.deepcopy(RECENT_ACTIVITIES)
        st.session_state.assessment_performance = copy.deepcopy(ASSESSMENT_PERFORMANCE)
        st.session_state.recent_attempts = copy.deepcopy(RECENT_ATTEMPTS)
        st.session_state.popular_practice = copy.deepcopy(POPULAR_PRACTICE_SETS)
        st.session_state.study_goals = copy.deepcopy(STUDY_GOALS)
        st.session_state.milestones = copy.deepcopy(MILESTONES)
        st.session_state.badges = copy.deepcopy(BADGES)
        st.session_state.chat_history = copy.deepcopy(CHAT_HISTORY_INITIAL)
        
        # UI interaction states
        st.session_state.upload_queue = []
        
        # User settings mock
        st.session_state.settings = {
            "notifications": True,
            "dark_mode": False,
            "daily_reminders": True,
            "email_summaries": False,
        }
        
        st.session_state.initialized = True

# --- Mutations ---

def toggle_task_completion(task_id: str, is_planner: bool = True) -> None:
    """Toggle the completion status of a task."""
    collection = st.session_state.planner_tasks if is_planner else st.session_state.today_plan
    status_key = "completed" if is_planner else "status"
    
    for task in collection:
        if task["id"] == task_id:
            if is_planner:
                task[status_key] = not task[status_key]
            else:
                task[status_key] = "completed" if task[status_key] != "completed" else "pending"
            
            # Record activity
            action_text = f"{'Completed' if (task[status_key] == True or task[status_key] == 'completed') else 'Unchecked'} task: {task['title']}"
            st.session_state.recent_activities.insert(0, {
                "icon_color": "#10b981",
                "text": action_text,
                "time": "Just now",
                "action": "study"
            })
            break

def add_chat_message(role: str, text: str) -> None:
    """Add a message to the AI assistant chat history."""
    st.session_state.chat_history.append({
        "role": role,
        "time": "Just now",
        "text": text
    })

def toggle_setting(key: str) -> None:
    """Toggle a boolean setting."""
    if key in st.session_state.settings:
        st.session_state.settings[key] = not st.session_state.settings[key]

def queue_file_upload(filename: str, size: str) -> None:
    """Add a file to the processing queue for Knowledge page."""
    file_id = f"file_{int(time.time())}"
    st.session_state.upload_queue.append({
        "id": file_id,
        "name": filename,
        "size": size,
        "status": "Processing",
        "progress": 0,
    })
    
def step_processing_queue() -> None:
    """Simulate progress on uploaded files. Called on rerun."""
    has_changes = False
    for file in st.session_state.upload_queue:
        if file["status"] == "Processing":
            file["progress"] += 35
            has_changes = True
            if file["progress"] >= 100:
                file["status"] = "Ready"
                file["progress"] = 100
                
                # Move to knowledge materials
                st.session_state.knowledge_materials.insert(0, {
                    "name": file["name"],
                    "subject": "Uncategorized",
                    "type": file["name"].split(".")[-1].upper() if "." in file["name"] else "DOC",
                    "size": file["size"],
                    "added_on": "Just now",
                    "status": "Ready",
                    "starred": False,
                })
                
                # Add activity
                st.session_state.recent_activities.insert(0, {
                    "icon_color": "#3b82f6",
                    "text": f"Uploaded {file['name']}",
                    "time": "Just now",
                    "action": "upload",
                })
    return has_changes
