FROM langchain/langgraph-api:3.11

ADD . /deps/project-aztrogent

RUN pip install --upgrade pip

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

ENV LANGSERVE_GRAPHS='{"aztrogent": "./src/aztrogent_agent/graph.py:graph", "calendar_agent": "./src/calendar_agent/graph.py:graph"}, "github_agent": "./src/github_agent/graph.py:graph", "email_agent": "./src/email_agent/graph.py:graph"}, "linkedin_agent": "./src/linkedin_agent/graph.py:graph"'

WORKDIR /deps/project-aztrogent