import streamlit as st
import os
from io import StringIO

# control to view diffs in github style
from diff_viewer import diff_viewer

from smartResumeWriterCrew import buildSmartResume

# read & send the contents of the file
def readFile(f):
    with open(f, 'r') as f:
        return f.read()

# title
st.title('Smart Resume Builder 🧠')
st.markdown('#### Convert your _boring_ resume to ATS Compatible Smart Resume 💪🏻')

# Gather Inputs
old_resume = st.file_uploader(label='Provide your boring resume', type='.md', accept_multiple_files= False)

job_posting_url = st.text_input(label = 'Enter a job listing site', placeholder='Eg www.linkedin.com/jobs or https://www.indeed.com')

github_url = st.text_input(label = 'Enter your github URL _(optional)_', placeholder='Eg your github profile or short bio')

personal_writeup = st.text_area(label = 'Enter your peronsal writeup _(optional)_', placeholder='Eg short bio')

if old_resume :
    with open('temp/sample_resume.md', 'w+') as f:
        f.write(StringIO(old_resume.getvalue().decode("utf-8")).read())
    if st.button(label='Kick off 🚀', type='primary',use_container_width=True) :
        with st.spinner(text='Agent Working...'):
            buildSmartResume(resume_path='temp/old_resume.md', job_posting_url=job_posting_url, github_url=github_url, personal_info=personal_writeup)
        st.markdown('## Here is your smart re-written resume')
        with st.expander(label='Click ⬇️ to look at the difference between _boring_ resume and _smart_ resume', icon=':material/difference:'):
            diff_viewer(old_text=readFile('temp/sample_resume.md'), new_text=readFile('temp/tailored_resume.md'), lang='none')
        with st.expander(label='## Click ⬇️ to view the *_smart_* resume', icon=':material/visibility:'):
            tab1, tab2, tab3 = st.tabs(['Boring Resume','Smart Resume', 'Backup'])
            with tab1:
                st.markdown(readFile('temp/sample_resume.md'))
            with tab2:  
                st.markdown(readFile('temp/tailored_resume.md'))
            with tab3:  
                st.markdown(readFile('config/tailored_resume.md'))  