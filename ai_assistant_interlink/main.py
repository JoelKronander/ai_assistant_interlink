import streamlit as st
import os
from openai import OpenAI
import time
import threading
import yaml

host_openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# load config.yaml file settings
with open("config.yaml") as file:
    config = yaml.safe_load(file)
    print(config)
host_assistant_id = config['OPENAI_HOST_ASSISTANT']['ID']
host_assistant = host_openai_client.beta.assistants.retrieve(host_assistant_id)

HOST_AVATAR_IMG = 'content/images/hostAI.png'
GUEST_AVATAR_IMG = 'content/images/guestAI.png'


def get_last_assistant_message(client, thread_id):
    messages_response = client.beta.threads.messages.list(thread_id=thread_id)
    messages = messages_response.data
  
    # Iterate through messages in reverse chronological order to find the last assistant message
    for message in messages:
        if message.role == 'assistant':
            # Get the content of the last assistant message
            assistant_message_content = " ".join(
                content.text.value for content in message.content if hasattr(content, 'text')
            )
            return assistant_message_content.strip()
  
    return ""  # Return an empty string if there is no assistant message


def converse(
      assistant_1_client,
      assistant_1,
      assistant_2_client,
      assistant_2,
      topic,
      message_count):
    # Initialize Assistants
    assistant_1 = assistant_1_client.beta.assistants.retrieve(assistant_1.id)
    assistant_2 = assistant_2_client.beta.assistants.retrieve(assistant_2.id)

    assistant_1.avatar = HOST_AVATAR_IMG
    assistant_2.avatar = GUEST_AVATAR_IMG

    # Create Threads
    thread_1 = assistant_1_client.beta.threads.create()
    thread_2 = assistant_2_client.beta.threads.create()

    # Function for the conversation between two assistants
    def assistant_conversation(start_message, assistant_a, thread_a, client_a, assistant_b, thread_b, client_b, msg_limit):
      message_content = start_message

      for i in range(msg_limit):
          # Determine which assistant is speaking for color coding
          if assistant_a == assistant_1:
              assistant_color = '\033[94m\033[1m' 
              assistant_name = assistant_1.name
          else:
              assistant_color = '\033[92m\033[1m'
              assistant_name = assistant_2.name
  
          # Debug print in console
          print(f"{assistant_color}{assistant_name} speaking...\033[0m (Turn {i + 1})")

          # Send the message and wait for a response
          assistant_1_client.beta.threads.messages.create(
              thread_id=thread_a.id,
              role="user",
              content=message_content
          )
  
          # Run the assistant and wait until it's done
          run = assistant_1_client.beta.threads.runs.create(
              thread_id=thread_a.id,
              assistant_id=assistant_a.id
          )
          while True:
              run_status = assistant_1_client.beta.threads.runs.retrieve(
                  thread_id=thread_a.id,
                  run_id=run.id
              )
              if run_status.status == 'completed':
                  break
              time.sleep(1)  # sleep to avoid hitting the API too frequently
  
          # Get all messages from the assistant since the last 'user' message
          message_content = get_last_assistant_message(assistant_1_client, thread_a.id)
  
          # Print out each of the assistant's messages
          print(message_content+"\n")
          with st.chat_message(assistant_name, avatar=assistant_a.avatar):
            st.markdown(message_content)
  
          # Swap the assistants and threads for the next turn in the conversation
          client_a, client_b = client_b, client_a
          assistant_a, assistant_b = assistant_b, assistant_a
          thread_a, thread_b = thread_b, thread_a

    # Start the conversation
    host_start_message = f"Welcome {assistant_2.name}. How can I help you with today? I see that you come to talk to me about {topic}."

    assistant_conversation(host_start_message, assistant_1, thread_1, assistant_1_client, assistant_2, thread_2, assistant_1_client, message_count)


topic = None
user_assistant = None
num_messages = 0
## Sidebar controls
# Add a selectbox to the sidebar:
st.sidebar.image('content/images/ai_interlink.jpg', width=300)
openai_api_key = st.sidebar.text_input('OpenAI API Key for your OpenAI assistant')
if not openai_api_key:
   st.sidebar.warning('Please enter your OpenAi API key to connect your assistant', icon='⚠')
else:
  user_openai_client = OpenAI(api_key=openai_api_key)
  user_assistants = user_openai_client.beta.assistants.list(
    order="desc",
    limit="20",
  )
  user_assistant_name = st.sidebar.selectbox(
      'Pick which of your assitants you would like to talk to my assistant.',
      [a.name for a in user_assistants]
  )
  user_assistant = [a for a in user_assistants if a.name == user_assistant_name][0]
  topic = st.sidebar.text_input('What would you like our assistants to discuss?')
  num_messages = st.sidebar.number_input('Max messages to exchange.', min_value=1, max_value=10, value=10)

## Main window
st.title('AI Assistant Interlink')
st.write(f'#### Link your OpenAI assistant with my OpenAI assistant {host_assistant.name} to have them talk to each other and resolve tasks, questions, and more.')
if not topic or not user_assistant.name:
  st.warning(f'Please select which of your assistant that you would like to talk to {host_assistant.name} and the topic for them to talk about.', icon='⚠')
else:
  st.write('***')
  col1, col2 = st.columns(2, gap='small')
  col1.write('Host Assistant: **'+host_assistant.name+'**')
  col1.image(HOST_AVATAR_IMG, width=100)
  col2.write(f'Selected User Assistant: **{user_assistant.name}**')
  col2.image(GUEST_AVATAR_IMG, width=100)
  st.write(f'**Selected Topic**: {topic}')
  st.write('### Conversation')
  
  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  conv_ongoing = True
  while conv_ongoing:
    converse(host_openai_client, host_assistant, user_openai_client, user_assistant, topic, num_messages)
    
    conv_ongoing = False

