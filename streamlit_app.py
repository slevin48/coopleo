import streamlit as st
import openai, re, csv

# Set page title and icon
st.set_page_config(page_title="Coopleo", page_icon="💝")
st.logo('img/logo_coopleo.png')

avatar = {"assistant": "🤖", "user": "🐱"}
model = 'gpt-4o-mini'
# openai.api_key = st.secrets['OPENAI_API_KEY']

# Functions
def new_chat():
   st.session_state.convo = []

def chat_stream(messages,model='gpt-4o-mini'):
  # Generate a response from the ChatGPT model
  completion = openai.chat.completions.create(
        model=model,
        messages= messages,
        stream = True
  )
  report = []
  res_box = st.empty()
  # Looping over the response
  for resp in completion:
      if resp.choices[0].finish_reason is None:
          # join method to concatenate the elements of the list 
          # into a single string, then strip out any empty strings
          report.append(resp.choices[0].delta.content)
          result = ''.join(report).strip()
          result = result.replace('\n', '')        
          res_box.write(result) 
  return result

def store_email(email):
  with open('data/emails.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([email])

# Initialization
if 'convo' not in st.session_state:
    st.session_state.convo = []

if st.button('Nouvelle conversation 💝'):
   new_chat()


if not st.session_state['convo']:
    st.session_state['convo'] = [{'role': 'system', 'content': open('data/system_prompt.txt',encoding='utf-8').read()},
                                 {'role': 'assistant', 'content': open('data/welcome_message.txt',encoding='utf-8').read()}]
   
# Display the response in the Streamlit app
for line in st.session_state.convo:
    # st.chat_message(line.role,avatar=avatar[line.role]).write(line.content)
    if line['role'] == 'user':
      st.chat_message('user',avatar=avatar['user']).write(line['content'])
    elif line['role'] == 'assistant':
      st.chat_message('assistant',avatar=avatar['assistant']).write(line['content'])

# Create a text input widget in the Streamlit app
prompt = st.chat_input('Entrez votre message ici...')

if prompt:
  # Append the text input to the conversation
  with st.chat_message('user',avatar=avatar['user']):
    st.write(prompt)
  st.session_state.convo.append({'role': 'user', 'content': prompt })

  # --- Email detection and storage ---
  email_pattern = r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b'
  email_match = re.search(email_pattern, prompt)
  if email_match:
      store_email(email_match.group(0))
  # -----------------------------------

  # Query the chatbot with the complete conversation
  with st.chat_message('assistant',avatar=avatar['assistant']):
     result = chat_stream(st.session_state.convo,model)
  # Add response to the conversation
  st.session_state.convo.append({'role':'assistant', 'content':result})
