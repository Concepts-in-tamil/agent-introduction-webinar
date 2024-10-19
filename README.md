# llm-introduction-webinar

This repo accompanies LLM Agents Primer webinar streamed live on YT.

YT Link : https://www.youtube.com/live/zpWa6ccocOY 

## Details

`simple.ipynb` contains a simple demo on how to use 3 agents to generate a social media blog post based on a topic

`smartResumeBuilder.py` contains a streamlit app that takes a _boring_ resume and turns into a _smart_ resume using 3 agents

`smartResumeWriterCrew.py` contains the agent logic.

## How to use

```
git clone https://github.com/Concepts-in-tamil/llm-introduction-webinar
cd llm-introduction-webinar
python3 -venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run smartResumeBuilder.py
```