# AI Assistant Interlink

In the future we will let “My AI Assistant circle back to yours to hash out the details”. This is a simple protoype exploring this idea.

This project provides a web interface for a Host AI Assistant, designed to facilitate a seamless intractions with a guest (connecting) AI Assistants.
The streamlit interface serves as a connection interlink for the Host AI Assistant.

Guest users can enter the necessary information about their AI Assistant, and then let their AI assistant start a conversation with the host AI Assistant on the topic of choice.

The Guest AI Assistant can e.g. ask question of the host, perform negotiations, request information, sceheduling or so on. 
Depending on the capabilites of the Host and Guest AI Assistants, the conversation can be more or less complex.

![interlink](https://github.com/JoelKronander/ai_assistant_interlink/assets/18355572/88cf8359-29df-4878-a6ef-887d87af7c71)

## Features
- Config options for host AI Assistant.
- Simple and intuitive UI for inputting nessecary guest AI Assistant details
- Real-time conversation initiation
- Support for sleecting guest AI Assistant to connect.

## Quickstart
1. Clone the repository
2. Edit the `config.yaml` file to specify the host AI Assistant details
3. Run `poetry run streamlit run ai_assistant_interlink/main.py` to start the web interface

## Deploy your own Host AI Assistant interconnect
You can also easily deploy your Host AI Assistant page with streamlit.

1. Get a streamlit account
2. Fork this repository
3. Connect your forked repository to streamlit
4. Deploy your forked repository to streamlit, make sure to use advanced settings to specify the the python version as 3.11, and add the OPENAI_API_KEY for your host AI Assistant as a secret.

![Screenshot 2023-11-08 at 10 36 54 PM](https://github.com/JoelKronander/ai_assistant_interlink/assets/18355572/ff17f0e5-23ce-468e-9970-f01b97335589)
