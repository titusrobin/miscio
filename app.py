import os
from dotenv import load_dotenv
import openai
import time
import logging
import streamlit as st

# Load environment variables and initialize the OpenAI client
load_dotenv()
client = openai.OpenAI()

# Specify the model to use
model = "gpt-3.5-turbo-1106"  

# Step 1. Upload the feedback document to OpenAI
feedback_file_path = "/Users/robintitus/Desktop/NPL/Miscio/miscio/feedback_rag/Launchpad Feedback Sample.pdf" 
feedback_file_object = client.files.create(file=open(feedback_file_path, "rb"), purpose="assistants")

# Step 2 - Create an assistant with instructions for processing feedback
# assistant = client.beta.assistants.create(
#     name="Feedback Processor",
#     instructions="""You are an assistant that analyzes feedback documents.
#     Your role is to identify the main themes and sentiments within the feedback.
#     Extract key tags that represent the subjects of the feedback and analyze the sentiment (positive, negative, neutral) associated with each tag.""",
#     tools=[{"type": "retrieval"}],
#     model=model,
#     file_ids=[feedback_file_object.id],
# )

# # Get the Assistant ID
# assis_id = assistant.id
# print(f"Assistant ID: {assis_id}")

# Step 3. Create a Thread and send a message to the assistant asking for analysis
# thread = client.beta.threads.create()
# thread_id = thread.id
# print(f"Thread ID: {thread_id}")

#Hardcoded
thread_id = "thread_hAcAVAS7i6W4NRNrnFLkH7H8"
assis_id = "asst_vopEA8SnLWp9WGtfdYqVwPQD"

# Construct a message with the feedback content or a request to analyze the document
feedback_message = "Please analyze the attached feedback document and provide tags and sentiments."

# Send the message to the assistant
message = client.beta.threads.messages.create(
    thread_id=thread_id, role="user", content=feedback_message
)

# Run the Assistant
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assis_id,
    instructions="Identify themes and sentiments from the feedback document."
)

# Function to wait for run completion (remains the same as your original code)
def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# Run the wait_for_run_completion function
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# Check the Run Steps - LOGS (remains the same as your original code)
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Run Steps --> {run_steps.data[0]}")
