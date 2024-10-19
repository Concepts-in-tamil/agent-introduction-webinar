import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

from crewai import (
    Agent, Task, Crew, LLM
)
from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  SerplyWebSearchTool
)

def buildSmartResume(resume_path, job_posting_url, github_url, personal_info):

    search_tool = SerplyWebSearchTool(limit=100)
    scrape_tool = ScrapeWebsiteTool()
    read_resume = FileReadTool(file_path=resume_path)
    llm_1 = LLM(model='groq/llama-3.1-70b-versatile')
    llm_2 = LLM(model='ollama/gemma2:latest', base_url='http://localhost:11434', api_key='could be anything')
    llm_3 = LLM(model='ollama/llama3.1:latest', base_url='http://localhost:11434', api_key='could be anything')
    llm_4 = LLM(model='ollama/gemma:latest', base_url='http://localhost:11434', api_key='could be anything')
    llm_5 = LLM(model='ollama/mistral:latest', base_url='http://localhost:11434', api_key='could be anything')

    # Agent 1: Researcher
    researcher = Agent(
        role="Tech Job Researcher",
        goal="Make sure to do amazing analysis on "
            "job posting to help job applicants",
        tools = [scrape_tool, search_tool],
        verbose=True,
        backstory=(
            "As a Job Researcher, your prowess in "
            "navigating and extracting critical "
            "information from job postings is unmatched."
            "Your skills help pinpoint the necessary "
            "qualifications and skills sought "
            "by employers, forming the foundation for "
            "effective application tailoring."
        ),
        llm = llm_3
    )

    # Agent 2: Profiler
    profiler = Agent(
        role="Personal Profiler for Engineers",
        goal="Do increditble research on job applicants "
            "to help them stand out in the job market",
        tools = [scrape_tool, search_tool,
                read_resume],
        verbose=True,
        backstory=(
            "Equipped with analytical prowess, you dissect "
            "and synthesize information "
            "from diverse sources to craft comprehensive "
            "personal and professional profiles, laying the "
            "groundwork for personalized resume enhancements."
        ),
        llm = llm_5
    )

    # Agent 3: Resume Strategist
    resume_strategist = Agent(
        role="Resume Strategist for Engineers",
        goal="Find all the best ways to make a "
            "resume stand out in the job market.",
        tools = [scrape_tool, search_tool,
                read_resume],
        verbose=True,
        backstory=(
            "With a strategic mind and an eye for detail, you "
            "excel at refining resumes to highlight the most "
            "relevant skills and experiences, ensuring they "
            "resonate perfectly with the job's requirements."
            "you are a pro in crafting ATS compliant resume "
            "that is garuenteed to score more than 80% ATS score."
        ),
        llm = llm_5
    )

    # Task for Researcher Agent: Extract Job Requirements
    research_task = Task(
        description=(
            "Analyze the job posting URL provided ({job_posting_url}) "
            "to extract key skills, experiences, and qualifications "
            "required. Use the tools to gather content and identify "
            "and categorize the requirements."
        ),
        expected_output=(
            "A structured list of job requirements, including necessary "
            "skills, qualifications, and experiences."
        ),
        agent=researcher,
        async_execution=True
    )

    # Task for Profiler Agent: Compile Comprehensive Profile
    profile_task = Task(
        description=(
            "Compile a detailed personal and professional profile "
            "using the GitHub ({github_url}) URLs, and personal write-up "
            "({personal_writeup}). Utilize tools to extract and "
            "synthesize information from these sources."
        ),
        expected_output=(
            "A comprehensive profile document that includes skills, "
            "project experiences, contributions, interests, and "
            "communication style."
        ),
        agent=profiler,
        async_execution=True,
        context= []
    )

    resume_strategy_task = Task(
        description=(
            "Using the profile and job requirements obtained from "
            "previous tasks, tailor the resume to highlight the most "
            "relevant areas. Employ tools to adjust and enhance the "
            "resume content. Make sure this is the best resume even but "
            "don't make up any information. Update every section, "
            "inlcuding the initial summary, work experience, skills, "
            "and education. All to better reflect the candidates "
            "abilities and how it matches the job posting."
        ),
        expected_output=(
            "A re-write of the original resume that effectively highlights the candidate's "
            "qualifications and experiences relevant to the job."
        ),
        output_file="temp/tailored_resume.md",
        context=[research_task, profile_task],
        agent=resume_strategist
    )

    job_application_crew = Crew(
        agents=[researcher,
                profiler,
                resume_strategist],

        tasks=[research_task,
            profile_task,
            resume_strategy_task],

        verbose=True
    )


    job_application_inputs = {
        'job_posting_url': job_posting_url,
        'github_url': github_url,
        'personal_writeup': personal_info
    }

    job_application_crew.kickoff(inputs=job_application_inputs)
