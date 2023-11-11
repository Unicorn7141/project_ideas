import numpy as np
import pandas as pd
import hydralit as hy
import streamlit as st
import hydralit_components as hc
from db import *

projects = load_projects()
edit = {}

app = hy.HydraApp("Project Ideas", favicon="💡")
allow_access = bool(app.check_access()[0])
updates = hy.container()


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
    for project in projects:
        edit[project["name"]] = False
        keys = project.keys()

        # placeholder = hy.container()

        content = "\n".join([f"{k.capitalize()}: {project[k]}\n" for k in keys][1:-1])
        difficulty = project["difficulty"]

        with hy.expander(f'**{project["name"]}**'):
            hy.write(content)

            hc.progress_bar(
                value=difficulty * 10,
                content_text=f"Difficulty: {'Easy' if difficulty <= 4 else 'Medium' if difficulty <= 7 else 'Hard'}",
                sentiment="good"
                if difficulty <= 4
                else "neutral"
                if difficulty <= 7
                else "bad",
            )

            if allow_access:
                del_btn = hy.button(
                    "Delete Project",
                    key=project["name"],
                    on_click=delete,
                    args=(project["name"],),
                )

                changes = {}
                with hy.form(project["name"]) as form:
                    name = hy.text_input(
                        "Project Name",
                        project["name"],
                    )

                    description = hy.text_area(
                        "Project Description",
                        project["description"],
                    )

                    requirements = hy.text_input(
                        "Project Requirements",
                        project["requirements"],
                    )

                    difficulty = hy.slider(
                        "Project Difficulty",
                        1.0,
                        10.0,
                        float(project["difficulty"]),
                        0.5,
                    )

                    if hy.form_submit_button("Save Changes"):
                        changes = {
                            "name": name,
                            "description": description,
                            "requirements": requirements,
                            "difficulty": difficulty,
                        }

                        edit_project(project["name"], changes)


@app.addapp(title="Resources", icon="📜")
def resources():
    hy.info("Still working on it....")
    # categories = ["Microcontrollers", "Components", "Informational", "Other"]

    # if allow_access:
    #     with hy.form("resource"):
    #         hy.title("Add a new resource")
    #         category = hy.selectbox("Category", categories)
    #         title = hy.text_input("Title")
    #         link = hy.text_input("Link")
    #         link_text = hy.text_input("Link Text")
    #         description = hy.text_area("Description")
    #         media = hy.file_uploader("Media/Files")
    #         embed_media = hy.checkbox("Embed")
    #         if hy.form_submit_button("Add Resource"):
    #             with open("resources.json", "r+") as file:
    #                 resources = dict(json.load(file))

    #             resources[category.lower()].append(
    #                 {
    #                     "title": title,
    #                     "description": description,
    #                     "link": link,
    #                     "link_text": link_text,
    #                     # "media": media.read(),
    #                     # "embed": embed_media,
    #                 }
    #             )
    #             with open("resources.json", "w") as file:
    #                 json.dump(resources, file, indent=2)

    # with open("resources.json", "r") as file:
    #     resources = json.load(file)

    # for category in categories:
    #     with hy.expander(category):
    #         try:
    #             for rsrc in resources[category.lower()]:
    #                 rsrc
    #         except KeyError as ke:
    #             hy.error("Nothing here yet")


@app.addapp(title="Add Project", icon="🔐")
def add_projects():
    global allow_access
    placeholder = hy.empty()
    placeholder.error("No Access", icon="🔒")
    with placeholder.form("login_form") as form:
        username = hy.text_input("Username")
        password = hy.text_input("Password", type="password")

        if hy.form_submit_button("Login"):
            secret_username = st.secrets.get("DB_USERNAME")
            secret_password = st.secrets.get("DB_PASSWORD")

            allow_access = secret_username == username and secret_password == password

    if allow_access:
        placeholder.empty()
        placeholder.success("Admin Acccess", icon="🔓")
        app.set_access(1, "Admin")
        with hy.form("project", True) as form:
            project_name = hy.text_input("Project Name")
            project_description = hy.text_area("Description")
            project_requirements = hy.text_input("Requirements")
            project_difficulty = hy.select_slider(
                "Difficulty", [i for i in np.arange(1, 10.5, 0.5)]
            )

            if hy.form_submit_button("Add project"):
                new_project = {
                    "name": project_name,
                    "description": project_description,
                    "requirements": project_requirements,
                    "difficulty": project_difficulty,
                }
                with open("projects.json", "r+") as f:
                    file_data = json.load(f)
                    file_data["projects"].append(new_project)
                    f.seek(0)
                    json.dump(file_data, f, indent=2)


app.run()
