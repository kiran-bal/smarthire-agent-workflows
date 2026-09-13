# 🚀 SmartHire AI: Agentic Interview Assistant

An **Agentic Interview Assistant** — a powerful, real-time, agent-powered application that automates interview question generation from candidate resumes and sends them via email.

---

## 🎯 What It Does

This app lets you upload a candidate resume, extract content (skills, projects, etc.), and generates relevant interview questions in real time. The results are also emailed to the user. It’s perfect for recruiters, HR tools, or hiring platforms.

---

## ⚙️ Workflow

1. **📤 Resume Upload:** Candidate resume is uploaded via a Streamlit UI.  
2. **🔍 Text Extraction Agent:** Parses the resume into structured content.  
3. **🎯 Question Generation Agent:** Generates resume-based interview questions.  
4. **📧 Email Agent:** Sends the questions to the user’s email.  
5. **📡 Streaming:** Questions are streamed live to the UI using LangGraph’s real-time capabilities.

---

## 🖼️ Screenshots

**Upload & Email Interface:**  
![Upload UI](https://github.com/kiran-bal/Smart_Hire_AI_Langgraph_CrewAI/blob/main/resources/screenshots/start_page.png?raw=true)

**Data Extraction:**  
![Text Extraction](https://github.com/kiran-bal/Smart_Hire_AI_Langgraph_CrewAI/blob/main/resources/screenshots/text_extraction.png?raw=true)  
![PDF Extract Agent](https://github.com/kiran-bal/Smart_Hire_AI_Langgraph_CrewAI/blob/main/resources/screenshots/pdf_extract_agent.png?raw=true)

**Interview Question Generation:**  
![Interview Qns](https://github.com/kiran-bal/Smart_Hire_AI_Langgraph_CrewAI/blob/main/resources/screenshots/interview_qns.png?raw=true)  
![Interview Qn Agent](https://github.com/kiran-bal/Smart_Hire_AI_Langgraph_CrewAI/blob/main/resources/screenshots/interview_qn_agent.png?raw=true)

**Email Agent:**  
![Email Agent](https://github.com/kiran-bal/Smart_Hire_AI_Langgraph_CrewAI/blob/main/resources/screenshots/email_agent.png?raw=true)

---

## 🧱 Powered by LangGraph + CrewAI

The app uses a **LangGraph-based workflow** with three modular agents:

- **ExtractorAgent** – Reads and extracts data from the resume.  
- **QuestionGenAgent** – Creates relevant interview questions.  
- **MailerAgent** – Emails the output to the user.  

This modular design using **CrewAI** ensures flexibility and scalability.

---

## 📽️ Demo Video

[![Watch the demo](https://img.shields.io/badge/Watch%20Demo-Click%20Here-blue?logo=github)](https://drive.google.com/file/d/1pjPbhxTma0Qo2r09JSNlb7-SYtct4g-B/view?usp=sharing)

The screen recordings are also attached to the [demo-videos release](https://github.com/kiran-bal/smarthire-agent-workflows/releases/tag/demo-videos).

> ⚠️ *If the video does not open directly in your browser, try downloading it or playing it in a compatible media player.*

---

## 💡 Use Cases

- Recruitment platforms  
- University career services  
- Internal HR tools  
- Automated mock interview systems
