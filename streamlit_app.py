import streamlit as st
from openai import OpenAI
from pathlib import Path

# Show title and description.
st.title("🤖 JanaBot")
st.write(
    "Hi, I'm JanaBot! ('Jah'-'Nah'-'Bot') "
    "I'm your virtual assistant. Let me know what information you're looking for and I will direct you to the correct report. "
    "You can ask me anything and I will do my best to help you, or ask for more information."
)

avatar_path = Path("jana.png")
avatar_image = avatar_path.read_bytes()



file_path = "dashboard-descriptions.txt"

with open(file_path, 'r') as file:
    file_content = file.read()

dashboard_information = file_content


# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.secrets["api_key"]


if not openai_api_key:
     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

#     # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:
        st.session_state.messages = [{"role": "system", "content": f"You are a Standard Reporting expert helping people understand what information is available in what report. Answer either with name of one or more reports from provided list or by saying you don't have enough information to answer. In the provided file is the list of reports with their descriptions:{dashboard_information}. Do not provide any advice or information except which report or combination of reports to use, or information about the reports. Assume all questions excluding requests for report lists or descriptions are asking what report to use. When reccommending a report use full sentences."},
            ]


    # # Display the existing chat messages via `st.chat_message`.
    # for message in st.session_state.messages:
    #     if message["role"] == "user" or message["role"] == "assistant":
    #         with st.chat_message(message["role"]):
    #             st.markdown(message["content"])

    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            # Include avatar with assistant message
            if avatar_image:
                with st.chat_message("assistant", avatar=avatar_image):
                    st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Ask JanaBot a question..."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)            

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant", avatar=avatar_image):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
