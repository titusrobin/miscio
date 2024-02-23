from dotenv import load_dotenv
import openai
import time
import streamlit as st

# Environment variables and initialization
load_dotenv()
thread_id = 'thread_hAcAVAS7i6W4NRNrnFLkH7H8'
assis_id = 'asst_vopEA8SnLWp9WGtfdYqVwPQD'
model = "gpt-3.5-turbo-1106"

# Initialize the session state variables
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Set up the front-end page
st.set_page_config(page_title="MiscioAgent", page_icon=":memo:")

# Ask user to input OpenAI API Key
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

if openai_api_key:
    openai.api_key = openai_api_key

    # ===Functions===
    # Function: upload document to openai and return file ID
    def upload_to_openai(filepath):
        with open(filepath, "rb") as file:
            response = openai.files.create(file=file, purpose="assistants")
        return response.id


    # Function: initiate assistant run and display response
    def initiate_assistant_run(file_id):
        st.session_state.thread_id = openai.beta.threads.create().id
        openai.beta.assistants.files.create(assistant_id=assis_id, file_id=file_id)

        # Start the assistant run
        run = openai.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assis_id,
            instructions="""You are an assistant that analyzes feedback documents.
            Your role is to identify the main themes and sentiments within the feedback.
            Extract key tags as bullet pointers that represent the subjects of the feedback and analyze the sentiment (positive, negative, neutral) associated with each tag.""",
        )

        with st.spinner("Generating response..."):
            while run.status != "completed":
                time.sleep(1)
                run = openai.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id, run_id=run.id
                )

            messages = openai.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )

            # Display the assistant response on the Streamlit web page
            for message in messages.data:
                if message.role == "assistant":
                    content = message.content[0].text.value
                    with st.chat_message("assistant"):
                        st.markdown(content, unsafe_allow_html=True)

    # Sidebar for file upload
    file_uploaded = st.sidebar.file_uploader("", type=["pdf", "txt"])

    # Upload file button
    if st.sidebar.button("Upload File"):
        if file_uploaded:
            with open(file_uploaded.name, "wb") as f:
                f.write(file_uploaded.getbuffer())
            file_id = upload_to_openai(file_uploaded.name)
            st.session_state.file_id_list.append(file_id)

            # Call the function to initiate assistant run and display response
            initiate_assistant_run(file_id)

# Main user interface
st.title("MiscioAgent")
st.write("Explore Student Feedback")

# Chat interface
if st.session_state.file_id_list:
    # Show existing messages
    for message in st.session_state.messages:
        st.tex
