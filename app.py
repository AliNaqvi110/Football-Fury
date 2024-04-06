import os
import sqlite3
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from create_database import create_table, insert_data
from fetch_data_csv import fetch_data
# from testfunct import play_webcam
from model import callback



# Get data from database table in a csv file
def get_csv_file(db_path, table_name):
    # check csv data
    conn = sqlite3.connect(db_path)
    fetch_data(conn, table_name)
    conn.close()


    
# main function
def main():

    # set layout
    st.set_page_config(page_title="Football Fury", page_icon=":soccer_ball")
    os.environ["STREAMLIT_THEME"] = "dark"
    


    # Define CSS code
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    .reportview-container .sidebar-content {display: none;}
    .stDeployButton {visibility: hidden;}
    #stDecoration {display: none;}
    </style>
    """

    # Display the CSS code
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


    # Logo image path
    logo_path = "Logo.png"

    # logo css style
    logo_style = """
    .css-override {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    """
    st.markdown(f'<style>{logo_style}</style>', unsafe_allow_html=True)

    # Create a horizontal container for logo and title
    col1, col2 = st.columns(2)

    # Display logo in the first column
    with col1:
        st.image(logo_path, width=100)  # Optional: Adjust width as needed

    # Display title in the second column
    with col2:
        st.title("Football Fury")
    

    # webrtc_streamer(key="football",video_frame_callback=infer_video)
    # play_webcam()
    webrtc_streamer(key="football",
                    video_frame_callback=callback,
                    rtc_configuration={  # Add this line
                        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                        
                    },
                    media_stream_constraints={"video": True, "audio": False},
                    async_processing=True
    )

    
        
# Call to main function
if __name__ == "__main__":
    main()
