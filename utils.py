from uuid import uuid4

import dropbox
import streamlit as st

dbx = dropbox.Dropbox(
    oauth2_refresh_token=st.secrets["dropbox_refresh_token"],
    app_key=st.secrets["dropbox_app_key"],
    app_secret=st.secrets["dropbox_app_secret"],
)


def add_vertical_space(num_lines: int = 1) -> None:
    for _ in range(num_lines):
        st.write("")


def upload_file(data, filename) -> None:
    """Upload a file.

    Return the request response, or None in case of error.
    """
    dropbox_file_path = f"/Data/{filename}"
    try:
        dbx.files_upload(data, dropbox_file_path)
    except dropbox.exceptions.ApiError as err:
        print("*** API error", err)
        return None


def unique_audio_filename(lesson_id: str) -> str:
    id = uuid4().hex
    return f"{lesson_id}_{id}.mp3"
