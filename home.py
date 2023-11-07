import json


def load_projects():
    projects = dict(json.loads(open("projects.json").read()))
    return projects


import hydralit.hydralit_ as hy
import streamlit as st
import hydralit_components.hydralit_components as hc


app = hy.HydraApp("Project Ideas")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

theme_bad = {
    "bgcolor": "#FFF0F0",
    "title_color": "red",
    "content_color": "red",
    "icon_color": "red",
}

theme_neutral = {
    "bgcolor": "#f9f9f9",
    "title_color": "orange",
    "content_color": "orange",
    "icon_color": "orange",
}

theme_good = {
    "bgcolor": "#EFF8F7",
    "title_color": "green",
    "content_color": "green",
    "icon_color": "green",
}


@app.addapp(is_home=True, title="Home", icon="🏠")
def home():
    hy.write(
        """
             # Introduction!

            ## What is this all about?

             This shit is meant to be a place for me to share my project ideas and useful resources for beginners.

             I will also share a few tips and important notes I think will be useful.

             """
    )


@app.addapp(title="Project Ideas", icon="💡")
def projects():
    projects = load_projects()
    for project in projects.keys():
        content = "\n".join([f"{k}: {v}\n" for k, v in projects[project].items()][:-1])
        difficulty = projects[project]["Difficulty"]

        with hy.expander(project):
            hy.write(content)
            hc.progress_bar(
                value=difficulty * 10,
                content_text="Difficulty",
                sentiment="good"
                if difficulty <= 3
                else "neutral"
                if difficulty <= 6
                else "bad",
            )


@app.addapp(title="Resources", icon="📜")
def resources():
    hy.info("Resources")


app.run()
