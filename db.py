import json


def load_projects():
    with open("projects.json") as f:
        projects = dict(json.load(f))

    return projects["projects"]


import json


def edit_project(project_name, new_data):
    with open("projects.json", "r") as file:
        data = json.load(file)

    projects = data["projects"]
    for i, project in enumerate(projects):
        if project["name"] == project_name:
            for key, value in project.items():
                project[key] = (
                    new_data[key]
                    if key in new_data and new_data[key] is not None
                    else value
                )
            break

    with open("projects.json", "w") as file:
        json.dump(data, file, indent=2)


def delete(project_name):
    with open("projects.json", "r") as file:
        data = json.load(file)

    projects = data["projects"]
    for project in projects:
        if project["name"] == project_name:
            projects.remove(project)
            data["projects"] = projects
            break
        
    with open("projects.json", "w") as file:
        json.dump(data, file, indent=2)
