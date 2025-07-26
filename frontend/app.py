import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Resume Parser", layout="wide")

# Add connection test
def test_api_connection():
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        return response.status_code == 200, response.status_code
    except requests.exceptions.RequestException as e:
        return False, str(e)

# Display connection status
with st.sidebar:
    st.header("🔗 Connection Status")
    if st.button("Test API Connection"):
        with st.spinner("Testing connection..."):
            is_connected, status = test_api_connection()
            if is_connected:
                st.success(f"✅ Connected! Status: {status}")
            else:
                st.error(f"❌ Connection failed: {status}")
                st.info("Make sure FastAPI server is running on http://localhost:8000")

tab1, tab2 = st.tabs(["Upload Resume", "View History"])

with tab1:
    st.title("📤 Upload Resume")
    jd = st.text_area("Paste Job Description", placeholder="Enter the job description here...")
    uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

    # Show validation status
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
    if jd:
        st.success(f"✅ Job description entered ({len(jd)} characters)")
    
    # Only enable submit if both are provided
    submit_enabled = uploaded_file is not None and jd.strip() != ""
    
    if not submit_enabled:
        if not uploaded_file:
            st.warning("⚠️ Please upload a PDF file")
        if not jd.strip():
            st.warning("⚠️ Please enter a job description")

    if st.button("Submit", disabled=not submit_enabled) and uploaded_file and jd:
        with st.spinner("Analyzing Resume..."):
            try:
                # Display debug info
                st.info(f"📄 File: {uploaded_file.name} ({uploaded_file.size} bytes)")
                st.info(f"📝 Job Description: {len(jd)} characters")
                
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                
                # Prepare the request
                files = {"file": (uploaded_file.name, uploaded_file.read(), "application/pdf")}
                data = {"jd": jd}
                
                st.info(f"🚀 Sending request to: {API_URL}/upload_resume/")
                
                # Make the request with timeout
                response = requests.post(
                    f"{API_URL}/upload_resume/", 
                    files=files, 
                    data=data,
                    timeout=30  # 30 second timeout
                )
                
                st.info(f"📡 Response Status: {response.status_code}")
                
                response.raise_for_status()
                res = response.json()
                st.success("Analysis complete!")
                st.subheader("🧾 Analysis Output")

                # Display raw JSON
                st.json(res)

                # Display formatted output
                if "error" not in res:
                    st.subheader("Formatted Analysis")
                    
                    # Check if this is a fallback analysis
                    if "warning" in res:
                        st.warning(f"⚠️ {res['warning']}")
                        st.info(f"💡 {res.get('message', '')}")
                    
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
                    st.error(f"❌ Error: {res['error']}")
                    if "error_type" in res:
                        st.info(f"Error Type: {res['error_type']}")
                    if "message" in res:
                        st.info(f"💡 {res['message']}")

            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out! The server might be slow or unresponsive.")
                st.info("💡 Try again or check if the FastAPI server is running.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Connection failed! Cannot reach the API server.")
                st.info("💡 Make sure the FastAPI server is running on http://localhost:8000")
                st.code("uvicorn backend.main:app --reload")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request failed: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    st.error(f"Status Code: {e.response.status_code}")
                    st.text(f"Response: {e.response.text}")
            except requests.exceptions.JSONDecodeError:
                st.error("❌ Server response is not valid JSON.")
                if 'response' in locals():
                    st.text(f"Raw response: {response.text}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
                st.info("💡 Check the console for more details.")

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