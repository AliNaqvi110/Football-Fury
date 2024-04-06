import webview
import subprocess
import os

def on_closing():
        # Terminate the Streamlit process (if applicable)
        if streamlit_process:
            streamlit_process.terminate()


def open_browser():
    url = "http://192.168.10.2:8501"  # Assuming Streamlit app listens on this URL
    webview.create_window('Football Fury', url=url, width=800, height=600)

    
    webview.on_closing = on_closing  # Register the event listener

    webview.start()  # Start the webview window

if __name__ == "__main__":
    # Start Streamlit in a separate process
    current_dir = os.getcwd()
    # print(current_dir)
    # Split the path into components
    path_components = current_dir.split(os.sep)  # os.sep is the path separator

    # Remove the last component to go back one directory
    new_dir = os.sep.join(path_components[:-1])
    # print(new_dir)

    # Change the working directory
    os.chdir(new_dir)

    streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"])

    # Open webview window
    open_browser()

    # Wait for the Streamlit process to finish (optional, depending on your app's needs)
    streamlit_process.wait()  