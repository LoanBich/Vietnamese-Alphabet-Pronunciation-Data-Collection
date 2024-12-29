import streamlit as st
from audiorecorder import audiorecorder
import io

from utils import add_vertical_space, unique_audio_filename, upload_file

st.set_page_config("Data Collection", ":material/home:")


QUESTIONS = [
    {"title": "Chữ cái E", "id": "E"},
    {"title": "Chữ cái H", "id": "H"},
    {"title": "Chữ cái i", "id": "i"},
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
    st.subheader("Cảm ơn bạn đã giúp!")
    add_vertical_space(1)

    st.write(
        "Tớ đang cần thu thập data giọng nói về 8 chữ cái trong bảng chữ cái tiếng Việt để làm nghiên cứu cá nhân, hãy giúp tớ nhé!"
    )
    st.write(
        "Yên tâm là mọi dữ liệu tớ sẽ bảo mật và không có gì là nguy hiểm hết đâu ạ."
    )
    st.write(
        "Hãy ấn bắt đầu và giúp tớ thu âm các chữ cái, giúp tớ đọc chính xác rõ ràng từng chữ nhaaaa"
    )
    st.markdown("**Lưu ý:**")
    left_col, right_col = st.columns(2, border=True)
    left_col.markdown("![guideline](app/static/mic.png)")
    right_col.markdown("![guideline](app/static/audio_recorder.png)")

    add_vertical_space(1)
    if st.button(label="Bắt đầu", type="primary"):
        next_step()
        st.rerun()


@st.fragment
def show_question(question):
    question_title = question["title"]
    question_id = question["id"]

    st.subheader(f"{st.session_state['step']}/{len(QUESTIONS)}. {question_title}")
    add_vertical_space(1)

    audio = audiorecorder(
        "",  # "Ấn để bắt đầu ghi âm",
        "",  # "Ấn để dừng lại",
        key=question_id,
    )

    if len(audio) > 0:
        st.info(
            "Hãy giúp tớ check lại phát âm xem đã đúng và rõ ràng chưa nhé ạ! Nếu chưa được thì hãy ghi âm lại giúp tớ nha ạ!!",
            icon="ℹ️",
        )
        st.audio(audio.export().read())

    add_vertical_space(2)
    if st.button(label="Âm tiếp theo", type="primary"):
        if len(audio) > 0:
            with st.spinner("Uploading..."):
                audio_buffer = io.BytesIO()
                audio.export(audio_buffer, format="wav", parameters=["-ar", str(16000)])
                upload_file(audio_buffer.getvalue(), unique_audio_filename(question_id))
            next_step()
            st.rerun()
        else:
            st.error("Chưa được rồi, giúp tớ thu âm lại nha", icon="🚨")


@st.fragment
def show_thankyou():
    st.subheader("Done!")
    add_vertical_space(1)
    st.write(
        "Cảm ơn rất nhiều vì đã dành thời gian giúp tớ, chúc cậu nhiều sức khoẻ nha!!"
    )


st.title("Thu thập dữ liệu")

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
