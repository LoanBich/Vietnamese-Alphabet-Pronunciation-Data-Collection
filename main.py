import streamlit as st
from audiorecorder import audiorecorder

from utils import add_vertical_space, unique_audio_filename, upload_file

st.set_page_config("Data Collection", ":material/home:")


QUESTIONS = [
    {"title": "Chữ cái E", "id": "E"},
    {"title": "Chữ cái H", "id": "H"},
    {"title": "Chữ cái I", "id": "I"},
    {"title": "Chữ cái L", "id": "L"},
    {"title": "Chữ cái N", "id": "N"},
    {"title": "Chữ cái Ơ", "id": "Ơ"},
    {"title": "Chữ cái U", "id": "U"},
    {"title": "Chữ cái V", "id": "V"},
]
N_QUESTIONS = len(QUESTIONS)


def next_step():
    st.session_state["step"] += 1


@st.fragment
def show_greeting():
    st.subheader("Greeting!")
    add_vertical_space(1)

    st.write("Anonymous data collection + privacy message.")
    st.write("Instruction...")

    add_vertical_space(1)
    if st.button(label="Start", type="primary"):
        next_step()
        st.rerun()


@st.fragment
def show_question(question):
    question_title = question["title"]
    question_id = question["id"]

    st.subheader(f"{st.session_state['step']}/{len(QUESTIONS)}. {question_title}")
    add_vertical_space(1)

    left_col, right_col = st.columns([1, 2])

    with left_col:
        audio = audiorecorder(
            "Click to record",
            "Click to stop recording",
            key=question_id,
        )

    with right_col:
        if len(audio) > 0:
            st.info("You can check the recorded audio below", icon="ℹ️")
            st.audio(audio.export().read())

    add_vertical_space(2)
    if st.button(label="Submit", type="primary"):
        if len(audio) > 0:
            with st.spinner("Uploading..."):
                upload_file(audio.export().read(), unique_audio_filename(question_id))
            next_step()
            st.rerun()
        else:
            st.error("Please record your voice again.", icon="🚨")


@st.fragment
def show_thankyou():
    st.subheader("Done!")
    add_vertical_space(1)
    st.write("Thank you for your effort and your time!")


st.title("Data Collection")

if "step" not in st.session_state:
    st.session_state["step"] = 0

with st.container(border=True):
    if st.session_state["step"] == 0:
        show_greeting()
    elif st.session_state["step"] <= N_QUESTIONS:
        question_idx = st.session_state["step"] - 1
        show_question(QUESTIONS[question_idx])
    else:
        show_thankyou()
