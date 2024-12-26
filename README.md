# Big Data Federation Task

This repository contains a simple implementation of a chatbot that can search the web, retain chat history, and provide responses based on the conversation.

## Installation

Before getting started, make sure to install [*git*](https://git-scm.com/downloads) and [*Python version 3.10.7*](https://www.python.org/downloads/release/python-3107/) on your computer.

1. Clone the Repository  
   Open a terminal/command prompt on your computer and enter the following commands:
   ```bash
   git clone https://github.com/ViruSs51/BigDataFederationTask.git
   cd BigDataFederationTask
   ```

2. Set Up a Python Virtual Environment (Optional but Recommended)  
   Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install Required Dependencies  
   Install the necessary libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Project  
   Execute the chatbot script:
   ```bash
   python3 chatbot.py
   ```

## Requirements

- Python 3.10.7
- pip (Python's package installer)
- git
- Operating System: Windows, macOS, or Linux

## Features

- **Web Search**: The chatbot can search the web for relevant information.
- **Chat History**: Maintains a history of previous messages and responses.
- **Contextual Responses**: Uses the chat history to provide meaningful answers.