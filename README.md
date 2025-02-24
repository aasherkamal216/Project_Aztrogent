# 🤖 Project Aztrogent

Project Aztrogent is an advanced AI Agent orchestration system that helps users manage various tasks efficiently across multiple platforms including LinkedIn, GitHub, Gmail, and Google Calendar. Built with LangGraph and powered by Google Gemini, Aztrogent provides a seamless interface for task delegation and execution. Aztrogent learns from conversations, store important information about the user to improve its responses.

![Aztrogent](/static/Aztrogent.png)

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for different services:
  - LinkedIn Agent
  - GitHub Agent
  - Email Agent
  - Calendar Agent

- **Intelligent Task Delegation**: Aztrogent agent intelligently delagates tasks to specialized agents
- **Memory Management**: Built-in memory system for personalized interactions
- **Human-in-the-Loop**: Confirmation & Feedback system for critical actions
- **Retry Mechanism**: Error handling with automatic retries for Tool Calling
- **Web Search Integration**: Real-time information gathering capabilities

## Architecture

<table>
  <tr>
    <td><img src="static/Aztrogent_Graph_Light_Collapsed.png" alt="Graph (Collapsed)" title="Graph (Collapsed)"></td>
    <td><img src="static/Aztrogent_Graph_Dark.png" alt="Graph (Expanded)" title="Graph (Expanded)"></td>
  </tr>
</table>

## 🛠️ Tech Stack

- **Frameworks**: LangGraph, LangMeme
- **Language Models**: 
  - Google Gemini 2.0 Flash
  - Llama 3.3 70b
- **Embeddings**: Cohere Multilingual V3
- **Tools**: 
  - Composio for 3rd party integrations
  - Tavily for web search

## 📋 Prerequisites

- Python 3.11+
- Poetry package manager
- Required API keys:
  - Google API Key
  - Groq API Key
  - Composio API Key
  - Tavily API Key
  - Cohere API Key (You can also use OpenAI embeddings)
  - LangSmith API Key

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/project-aztrogent.git
cd aztrogent
```
2. Create and Activate Virtual Environment:
```bash

poetry shell
```
3. Install dependencies using Poetry:
```bash
poetry install
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Add your API keys in `.env` file. 

5. Composio Tools Integration
For using Composio tools, you need to add Integrations for the services being used. This can either be done manually on [Composio Apps](https://app.composio.dev/apps) (Recommended way) or running the following script:
```bash
composio add github likedin gmail googlecalendar
```
5. Run the Project in LangGraph studio
- If you want to use in-memory version of LangGraph studio, run this command:
```bash
poetry run langgraph dev
```
- If you have docker installed, you can run the studio using the following command:
```bash
langgraph build
langgraph up
```

## 🔧 Configuration

The project uses a modular configuration system. Each agent can be configured separately:

- Aztrogent configuration: `src/aztrogent_agent/configuration.py`
- LinkedIn Agent configuration: `src/linkedin_agent/configuration.py`
- GitHub Agent configuration: `src/github_agent/configuration.py`
- Email Agent configuration: `src/email_agent/configuration.py`
- Calendar Agent configuration: `src/calendar_agent/configuration.py`

## 👥 Contributing

Feel free to contribute to this project by submitting issues and pull requests.