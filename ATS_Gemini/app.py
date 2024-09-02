import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Act as a highly advanced ATS (Applicant Tracking System) with deep expertise in tech fields, including software engineering, data science, data analytics, and big data engineering. 

Your tasks are as follows:

1. **Evaluate the Resume:** Compare the resume against the given job description (JD) and assess its relevance. Consider the competitive job market and provide a **percentage match** score that reflects how well the resume aligns with the JD.
2. **Grammatical Corrections:** Identify and correct any grammatical errors in the resume to ensure professionalism and clarity.
3. **Line Improvements:** Suggest specific improvements for any lines in the resume that could be more impactful or clearer.
4. **Keyword Suggestions:** Recommend additional keywords that could improve the resume's alignment with the job description, especially in the context of ATS optimization.

Provide the response in the following JSON structure:

```json
{
  "JD Match": "%",
  "MissingKeywords": [],
  "GrammaticalErrors": [],
  "LineImprovements": [],
  "ProfileSummary": ""
}

Resume: {text}
Job Description: {jd}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)