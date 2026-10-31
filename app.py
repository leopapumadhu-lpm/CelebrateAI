import streamlit as st
import pandas as pd
from datetime import date, timedelta
from modules.planner import create_plan
from modules.exports import make_pdf

st.set_page_config(page_title="CelebrateAI", page_icon="🎉", layout="wide")

st.title("🎉 CelebrateAI")
st.subheader("Your AI-powered celebration and event planner")
st.write("Plan weddings, birthdays and community events with confidence.")

with st.sidebar:
    st.header("Your Event")
    event_type = st.selectbox("Event type", ["Birthday", "Wedding", "Community Event", "Anniversary", "Other"])
    event_name = st.text_input("Event name", "My Special Celebration")
    location = st.text_input("Location", "Chennai")
    event_date = st.date_input("Event date", date.today() + timedelta(days=30), min_value=date.today())
    guests = st.number_input("Expected guests", min_value=1, max_value=10000, value=100)
    budget = st.number_input("Total budget (₹)", min_value=1000, value=50000, step=1000)
    theme = st.text_input("Preferred theme", "Elegant and colorful")
    preferences = st.text_area("Additional preferences", "Vegetarian food, photography and music")
    api_key = st.text_input("Gemini API key (optional)", type="password")

if st.button("✨ Generate My Event Plan", type="primary", use_container_width=True):
    with st.spinner("Creating your celebration plan..."):
        st.session_state.plan = create_plan(
            event_type, event_name, location, str(event_date),
            guests, budget, theme, preferences, api_key
        )

if "plan" in st.session_state:
    plan = st.session_state.plan
    st.success("Your event plan is ready!")

    st.header("🌟 Event Concept")
    st.write(plan["concept"])

    st.header("🎨 Personalized Ideas")
    for idea in plan["ideas"]:
        st.write("• " + idea)

    st.header("💰 Budget Breakdown")
    df = pd.DataFrame(plan["budget"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.bar_chart(df.set_index("Category")["Amount (INR)"])
    st.download_button("Download Budget CSV", df.to_csv(index=False), "event_budget.csv", "text/csv")

    st.header("📅 Event Timeline")
    timeline = pd.DataFrame(plan["timeline"])
    st.dataframe(timeline, use_container_width=True, hide_index=True)
    st.download_button("Download Timeline CSV", timeline.to_csv(index=False), "event_timeline.csv", "text/csv")

    st.header("📋 Vendor Checklist")
    checklist = pd.DataFrame(plan["vendors"])
    edited = st.data_editor(checklist, use_container_width=True, hide_index=True)
    st.download_button("Download Vendor Checklist", edited.to_csv(index=False), "vendor_checklist.csv", "text/csv")

    st.header("📄 Complete Event Plan")
    pdf = make_pdf(plan)
    st.download_button("Download Event Plan PDF", pdf, "CelebrateAI_Event_Plan.pdf", "application/pdf")

else:
    st.info("Enter your event details in the sidebar and click Generate My Event Plan.")
    st.write("### What CelebrateAI can help with")
    c1, c2, c3 = st.columns(3)
    c1.metric("Event planning", "Personalized")
    c2.metric("Budget tracking", "Organized")
    c3.metric("Vendor checklist", "Ready to use")

st.divider()
st.caption("CelebrateAI | Plan • Celebrate • Create Memories")
