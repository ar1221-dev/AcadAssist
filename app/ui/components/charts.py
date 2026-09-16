"""Chart and visual metric components for AcadAssist."""

from typing import List, Tuple
import streamlit as st


def render_circular_score(
    score: int,
    label: str = "Average Score",
    sublabel: str = "↑ 12% from last month",
) -> None:
    """Render a clean SVG circular score gauge matching the assessment & progress designs."""
    radius = 42
    circumference = 2 * 3.14159 * radius
    stroke_dashoffset = circumference - (score / 100.0) * circumference
    
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 12px 0;">
            <div style="position: relative; width: 110px; height: 110px; display: flex; align-items: center; justify-content: center;">
                <svg width="110" height="110" viewBox="0 0 110 110" style="transform: rotate(-90deg);">
                    <circle cx="55" cy="55" r="{radius}" fill="none" stroke="#e8ede9" stroke-width="10" />
                    <circle cx="55" cy="55" r="{radius}" fill="none" stroke="#2d5f47" stroke-width="10"
                            stroke-dasharray="{circumference}" stroke-dashoffset="{stroke_dashoffset}"
                            stroke-linecap="round" />
                </svg>
                <div style="position: absolute; text-align: center;">
                    <span style="font-size: 1.45rem; font-weight: 700; color: #15221b;">{score}%</span>
                    <div style="font-size: 0.65rem; color: #6b7770; font-weight: 500;">{label}</div>
                </div>
            </div>
            <div style="margin-top: 8px; font-size: 0.76rem; font-weight: 600; color: #2d5f47;">
                {sublabel}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress_bar(
    value: int,
    color: str = "#2d5f47",
    height: int = 8,
) -> None:
    """Render a clean CSS progress bar."""
    st.markdown(
        f"""
        <div style="width: 100%; background: #eceae4; border-radius: 9999px; height: {height}px; overflow: hidden; margin: 6px 0;">
            <div style="width: {value}%; background: {color}; height: 100%; border-radius: 9999px; transition: width 0.3s ease;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_weekly_barchart(data: List[Tuple[str, float]]) -> None:
    """Render the weekly study hours bar chart."""
    max_val = 8.0  # scale max
    bars_html = ""
    
    for day, hours in data:
        bar_height_pct = min(100.0, (hours / max_val) * 100)
        bars_html += f"""
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px; flex: 1; height: 140px; justify-content: flex-end;">
            <div style="font-size: 0.68rem; color: #738078; font-weight: 500;">{hours}h</div>
            <div style="width: 24px; background: #6b8f7d; height: {bar_height_pct}%; border-radius: 4px 4px 0 0; transition: height 0.2s ease;"></div>
            <div style="font-size: 0.72rem; color: #435149; font-weight: 600;">{day}</div>
        </div>
        """
        
    st.markdown(
        f"""
        <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 8px; padding: 12px 10px 4px 10px; background: #ffffff; border-radius: 10px;">
            {bars_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_activity_donut(
    activities: List[Tuple[str, int, str]],
    total_time: str = "24.5 hrs",
) -> None:
    """Render the activity distribution donut chart using SVG."""
    segments_html = ""
    legend_html = ""
    
    radius = 50
    circumference = 2 * 3.14159 * radius
    current_offset = 0.0
    
    for label, pct, color in activities:
        dash_len = (pct / 100.0) * circumference
        gap_len = circumference - dash_len
        segments_html += f"""
        <circle cx="70" cy="70" r="{radius}" fill="none" stroke="{color}" stroke-width="22"
                stroke-dasharray="{dash_len} {gap_len}" stroke-dashoffset="{-current_offset}" />
        """
        current_offset += dash_len
        
        legend_html += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.78rem; margin-bottom: 6px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="width: 10px; height: 10px; border-radius: 50%; background: {color};"></span>
                <span style="color: #3b4640;">{label}</span>
            </div>
            <span style="font-weight: 700; color: #15221b;">{pct}%</span>
        </div>
        """
        
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 10px 0;">
            <div style="position: relative; width: 140px; height: 140px; flex-shrink: 0;">
                <svg width="140" height="140" viewBox="0 0 140 140" style="transform: rotate(-90deg);">
                    {segments_html}
                </svg>
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; pointer-events: none;">
                    <span style="font-size: 1rem; font-weight: 700; color: #17241d;">{total_time}</span>
                    <span style="font-size: 0.65rem; color: #727e77;">Total</span>
                </div>
            </div>
            <div style="flex: 1;">
                {legend_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress_line_chart() -> None:
    """Render smooth progress line chart for 30-day journey."""
    points = [(0, 75), (20, 70), (40, 62), (60, 50), (80, 42), (100, 22)]
    path_d = "M 0,75 L 50,70 L 100,62 L 150,50 L 200,42 L 260,22"
    area_d = f"{path_d} L 260,100 L 0,100 Z"
    
    st.markdown(
        f"""
        <div style="padding: 10px 0;">
            <svg width="100%" height="110" viewBox="0 0 260 105" preserveAspectRatio="none">
                <defs>
                    <linearGradient id="grad-area" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="#2d5f47" stop-opacity="0.3" />
                        <stop offset="100%" stop-color="#2d5f47" stop-opacity="0.0" />
                    </linearGradient>
                </defs>
                <path d="{area_d}" fill="url(#grad-area)" />
                <path d="{path_d}" fill="none" stroke="#2d5f47" stroke-width="2.5" stroke-linecap="round" />
                <circle cx="0" cy="75" r="3.5" fill="#2d5f47" />
                <circle cx="50" cy="70" r="3.5" fill="#2d5f47" />
                <circle cx="100" cy="62" r="3.5" fill="#2d5f47" />
                <circle cx="150" cy="50" r="3.5" fill="#2d5f47" />
                <circle cx="200" cy="42" r="3.5" fill="#2d5f47" />
                <circle cx="260" cy="22" r="3.5" fill="#2d5f47" />
            </svg>
            <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: #728078; margin-top: 4px;">
                <span>17 Aug</span>
                <span>24 Aug</span>
                <span>31 Aug</span>
                <span>7 Sep</span>
                <span>14 Sep</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
