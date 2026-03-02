import streamlit as st
from github import Github
import pandas as pd
import plotly.express as px

# 1. Page Configuration (The 'Look')
st.set_page_config(page_title="Project Zenith", page_icon="🛰️", layout="wide")

# 2. Secret Connection (Using the token we just made)
try:
    # This looks for the GITHUB_TOKEN we will put in Streamlit Cloud in the next step
    token = st.secrets["GITHUB_TOKEN"]
    g = Github(token)
    user = g.get_user()
    
    # Header Section
    st.title("🛰️ Project Zenith: Intelligence Hub")
    st.markdown(f"**Operator:** {user.name} | **Status:** Systems Online")
    st.divider()

    # 3. Data Columns
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("👤 Profile Analytics")
        st.image(user.avatar_url, width=150)
        st.metric("Public Repositories", user.public_repos)
        st.metric("Followers", user.followers)
        st.write(f"**Bio:** {user.bio}")

    with col2:
        st.header("📊 Technical Impact")
        # Creating a dynamic chart of your repository languages
        repo_data = []
        for repo in g.get_user().get_repos():
            if repo.language:
                repo_data.append(repo.language)
        
        if repo_data:
            df = pd.DataFrame(repo_data, columns=['Language'])
            lang_counts = df['Language'].value_counts().reset_index()
            lang_counts.columns = ['Language', 'Count']
            
            fig = px.pie(lang_counts, values='Count', names='Language', 
                         title="Core Language Proficiency", hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start coding! Once you have repos with languages, they will appear here.")

except Exception as e:
    st.error("Awaiting Connection... Please configure your GITHUB_TOKEN in Streamlit Secrets.")
