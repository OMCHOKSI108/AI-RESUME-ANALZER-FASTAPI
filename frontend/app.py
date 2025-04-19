import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Resume Parser", layout="wide")

tab1, tab2 = st.tabs(["Upload Resume", "View History"])

with tab1:
    st.title("📤 Upload Resume")
    jd = st.text_area("Paste Job Description")
    uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

    if st.button("Submit") and uploaded_file and jd:
        with st.spinner("Analyzing Resume..."):
            try:
                files = {"file": uploaded_file.getvalue()}
                data = {"jd": jd}
                response = requests.post(f"{API_URL}/upload_resume/", files=files, data=data)
                response.raise_for_status()
                res = response.json()
                st.success("Analysis complete!")
                st.subheader("🧾 Analysis Output")

                # Display raw JSON
                st.json(res)

                # Display formatted output
                if "error" not in res:
                    st.subheader("Formatted Analysis")
                    st.write(f"**Candidate Name:** {res.get('name', 'Not specified')}")
                    st.write(f"**Email:** {res.get('email', 'Not specified')}")
                    st.write(f"**Core Skills:** {', '.join(res.get('core_skills', [])) or 'None'}")
                    st.write(f"**Soft Skills:** {', '.join(res.get('soft_skills', [])) or 'None'}")
                    st.write(f"**Resume Rating:** {res.get('resume_rating', 0)}%")
                    st.write(f"**Improvement Areas:** {res.get('improvement_areas', 'None')}")
                    st.write(f"**Uploaded File:** {res.get('uploaded_file_name', 'Not specified')}")
                    st.write(f"**Job Fit Score:** {res.get('job_fit_score', 0)}%")
                    st.write(f"**Upskill Suggestions:** {res.get('upskill_suggestions', 'None')}")
                    st.write(f"**Skillset Improvements:** {', '.join(res.get('skillset_improvements', [])) or 'None'}")
                else:
                    st.error(f"Error: {res['error']}")

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
            except requests.exceptions.JSONDecodeError:
                st.error("Server response is not valid JSON.")
                st.text(response.text)

with tab2:
    st.title("📜 Resume History")
    with st.spinner("Fetching past resumes..."):
        try:
            response = requests.get(f"{API_URL}/history/")
            response.raise_for_status()
            history = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch history: {e}")
            st.stop()
        except requests.exceptions.JSONDecodeError:
            st.error("Received invalid JSON from the server.")
            st.text(f"Response content: {response.text}")
            st.stop()

    for res in history:
        file_name = res.get("uploaded_file_name", "Unknown File")
        name = res.get("name", "Unknown Name")
        with st.expander(f"{file_name} - {name}"):
            st.json(res)
            if "error" not in res:
                st.write(f"**Candidate Name:** {res.get('name', 'Not specified')}")
                st.write(f"**Email:** {res.get('email', 'Not specified')}")
                st.write(f"**Core Skills:** {', '.join(res.get('core_skills', [])) or 'None'}")
                st.write(f"**Soft Skills:** {', '.join(res.get('soft_skills', [])) or 'None'}")
                st.write(f"**Resume Rating:** {res.get('resume_rating', 0)}%")
                st.write(f"**Improvement Areas:** {res.get('improvement_areas', 'None')}")
                st.write(f"**Uploaded File:** {res.get('uploaded_file_name', 'Not specified')}")
                st.write(f"**Job Fit Score:** {res.get('job_fit_score', 0)}%")
                st.write(f"**Upskill Suggestions:** {res.get('upskill_suggestions', 'None')}")
                st.write(f"**Skillset Improvements:** {', '.join(res.get('skillset_improvements', [])) or 'None'}")