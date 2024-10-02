import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initialize session state for projects and people if not already initialized
if 'projects_df' not in st.session_state:
    st.session_state.projects_df = pd.DataFrame()
if 'people_df' not in st.session_state:
    st.session_state.people_df = pd.DataFrame()


# Functions to manage projects and people
def get_projects():
    if not st.session_state.projects_df.empty:
        return st.session_state.projects_df
    else:
        projects = [
            {
                'Project Name': 'AI Accountability Project',
                'Product Leader': 'Jane Doe',
                'Engineering Leader': 'John Smith',
                'Total Cost ($)': 15000,
                'Projected Revenue ($)': 500000,
                'Start Date': '2023-01-01',
                'Timeline Proposed (months)': 12,
                'Time Spent (hours)': 350,
                'Compute and Services Cost': [
                    {'Cost Name': 'AWS', 'Cost Amount': 5000},
                    {'Cost Name': 'OpenAI', 'Cost Amount': 2000},
                    {'Service': 'Amazon S3', 'Cost ($)': 50},
                    {'Service': 'Amazon SageMaker', 'Cost ($)': 200}
                ],
                'People Cost': [
                    {'Name': 'Alice Smith', 'Role': 'Data Scientist', 'Time Proposed (hours)': 150,
                     'Time Spent (hours)': 100, 'Cost ($)': 5000},
                    {'Name': 'Bob Johnson', 'Role': 'ML Engineer', 'Time Proposed (hours)': 160,
                     'Time Spent (hours)': 150, 'Cost ($)': 7500}
                ]
            },
            {
                'Project Name': 'Machine Learning Pipeline',
                'Product Leader': 'Emily Davis',
                'Engineering Leader': 'Michael Brown',
                'Total Cost ($)': 20000,
                'Projected Revenue ($)': 600000,
                'Start Date': '2023-03-15',
                'Timeline Proposed (months)': 18,
                'Time Spent (hours)': 400,
                'Compute and Services Cost': [
                    {'Cost Name': 'GCP', 'Cost Amount': 8000},
                    {'Cost Name': 'Azure', 'Cost Amount': 3000}
                ],
                'People Cost': [
                    {'Name': 'Carol Williams', 'Role': 'Data Analyst', 'Time Proposed (hours)': 140,
                     'Time Spent (hours)': 120, 'Cost ($)': 6000},
                    {'Name': 'Dave Wilson', 'Role': 'Data Engineer', 'Time Proposed (hours)': 180,
                     'Time Spent (hours)': 170, 'Cost ($)': 8500}
                ]
            },
        ]
        st.session_state.projects_df = pd.DataFrame(projects)
        return st.session_state.projects_df


def get_project_details(project_name):
    projects_df = get_projects()
    project_row = projects_df[projects_df['Project Name'] == project_name].iloc[0]
    data = {
        'Project Name': project_row['Project Name'],
        'Product Leader': project_row['Product Leader'],
        'Engineering Leader': project_row['Engineering Leader'],
        'Start Date': project_row['Start Date'],
        'Timeline Proposed (months)': project_row['Timeline Proposed (months)'],
        'Compute and Services Cost': project_row['Compute and Services Cost'],
        'People Cost': project_row['People Cost'],
        'Total Cost ($)': project_row['Total Cost ($)'],
        'Potential Business Value': project_row['Projected Revenue ($)'],
        'Time Spent (hours)': project_row['Time Spent (hours)'],
    }
    return data


def update_project(project_name, updated_data):
    idx = st.session_state.projects_df[st.session_state.projects_df['Project Name'] == project_name].index[0]
    for key in updated_data.keys():
        if key in st.session_state.projects_df.columns:
            st.session_state.projects_df.at[idx, key] = updated_data[key]



def calculate_total_cost(project):
    compute_services_cost = sum(item.get('Cost Amount', 0) for item in project['Compute and Services Cost'])
    people_cost = sum(person['Cost ($)'] for person in project['People Cost'])
    total_cost = compute_services_cost + people_cost
    return total_cost, compute_services_cost, people_cost


def refresh_state():
    st.session_state['refresh'] = not st.session_state.get('refresh', False)


def main():
    st.title("AI Kanaku - AI Accountability Dashboard")

    # Create tabs
    tabs = st.tabs(["Project Productivity View", "People Productivity View", "Add New Project"])

    # Project Productivity View
    with tabs[0]:
        if 'selected_project' not in st.session_state:
            st.session_state.selected_project = None

        if st.session_state.selected_project is None:
            st.header("Projects Overview")

            projects_df = get_projects()

            for index, row in projects_df.iterrows():
                st.subheader(f"Project: {row['Project Name']}")
                cols = st.columns(4)
                cols[0].write(f"**Product Leader:** {row['Product Leader']}")
                cols[1].write(f"**Engineering Leader:** {row['Engineering Leader']}")
                cols[2].write(f"**Total Cost ($):** {row['Total Cost ($)']:,}")
                cols[3].write(f"**Projected Revenue ($):** {row['Projected Revenue ($)']:,}")
                cols = st.columns(4)
                cols[0].write(f"**Start Date:** {row['Start Date']}")
                cols[1].write(f"**Timeline Proposed (months):** {row['Timeline Proposed (months)']}")
                cols[2].write(f"**Time Spent (hours):** {row['Time Spent (hours)']}")

                if st.button("Details", key=f"details_{index}"):
                    st.session_state.selected_project = row['Project Name']

                if st.button("Edit", key=f"edit_{index}"):
                    st.session_state.selected_project = row['Project Name']
                    st.session_state.edit_mode = True

                st.markdown("---")
        else:
            project_name = st.session_state.selected_project
            project_details = get_project_details(project_name)

            st.header(f"Project Details: {project_name}")

            if st.button("Back to Projects"):
                st.session_state.selected_project = None

            if 'edit_mode' not in st.session_state:
                st.session_state.edit_mode = False

            if st.session_state.edit_mode:
                st.subheader("Edit Project Information")
                project_name_input = st.text_input("Project Name", value=project_details['Project Name'])
                product_leader = st.text_input("Product Leader", value=project_details['Product Leader'])
                engineering_leader = st.text_input("Engineering Leader", value=project_details['Engineering Leader'])
                start_date = st.date_input("Start Date", pd.to_datetime(project_details['Start Date']))
                timeline = st.number_input("Timeline Proposed (months)",
                                           value=int(project_details['Timeline Proposed (months)']), min_value=0)
                projected_revenue = st.number_input("Projected Revenue ($)",
                                                    value=float(project_details['Potential Business Value']),
                                                    min_value=0.0)
                time_spent_hours = st.number_input("Time Spent (hours)",
                                                   value=int(project_details['Time Spent (hours)']), min_value=0)

                st.subheader("Compute and Services Cost")
                compute_services_cost = project_details['Compute and Services Cost']
                for idx, item in enumerate(compute_services_cost):
                    cols = st.columns([1, 1, 1])
                    item['Cost Name'] = cols[0].text_input("Cost Name", value=item.get('Cost Name', ''),
                                                           key=f"edit_compute_cost_name_{idx}")
                    item['Cost Amount'] = cols[1].number_input("Cost Amount", value=float(item.get('Cost Amount', 0.0)),
                                                               min_value=0.0, key=f"edit_compute_cost_amount_{idx}")
                    if cols[2].button("Remove", key=f"remove_compute_{idx}"):
                        compute_services_cost.pop(idx)

                if st.button("Add Compute Cost"):
                    compute_services_cost.append({'Cost Name': '', 'Cost Amount': 0.0})

                st.subheader("People Cost")
                people_cost = project_details['People Cost']
                for idx, person in enumerate(people_cost):
                    st.write(f"Person {idx + 1}")
                    cols = st.columns([1, 1, 1])
                    person['Name'] = cols[0].text_input("Name", value=person['Name'], key=f"edit_person_name_{idx}")
                    person['Role'] = cols[1].text_input("Role", value=person['Role'], key=f"edit_person_role_{idx}")
                    if cols[2].button("Remove", key=f"remove_person_{idx}"):
                        people_cost.pop(idx)
                    person['Time Proposed (hours)'] = st.number_input("Time Proposed (hours)",
                                                                      value=int(person['Time Proposed (hours)']),
                                                                      min_value=0, key=f"edit_time_proposed_{idx}")
                    person['Time Spent (hours)'] = st.number_input("Time Spent (hours)",
                                                                   value=int(person['Time Spent (hours)']), min_value=0,
                                                                   key=f"edit_time_spent_{idx}")
                    person['Cost ($)'] = st.number_input("Cost ($)", value=float(person['Cost ($)']), min_value=0.0,
                                                         key=f"edit_person_cost_{idx}")

                if st.button("Add Person"):
                    people_cost.append(
                        {'Name': '', 'Role': '', 'Time Proposed (hours)': 0, 'Time Spent (hours)': 0, 'Cost ($)': 0.0})

                if st.button("Save Changes"):
                    updated_project = {
                        'Project Name': project_name_input,
                        'Product Leader': product_leader,
                        'Engineering Leader': engineering_leader,
                        'Start Date': str(start_date),
                        'Timeline Proposed (months)': timeline,
                        'Projected Revenue ($)': projected_revenue,
                        'Time Spent (hours)': time_spent_hours,
                        'Compute and Services Cost': compute_services_cost,
                        'People Cost': people_cost,
                    }
                    total_cost, compute_services_total, people_total = calculate_total_cost(updated_project)
                    updated_project['Total Cost ($)'] = total_cost
                    update_project(project_name, updated_project)
                    st.success("Project updated successfully!")
                    st.session_state.edit_mode = False
                    refresh_state()  # Trigger a page refresh

            else:
                st.subheader("Basic Information")
                cols = st.columns(2)
                cols[0].write(f"**Product Leader:** {project_details['Product Leader']}")
                cols[1].write(f"**Engineering Leader:** {project_details['Engineering Leader']}")
                cols = st.columns(2)
                cols[0].write(f"**Start Date:** {project_details['Start Date']}")
                cols[1].write(f"**Timeline Proposed (months):** {project_details['Timeline Proposed (months)']}")

                st.subheader("Compute and Services Cost")
                compute_services_cost = project_details['Compute and Services Cost']
                compute_services_df = pd.DataFrame(compute_services_cost)
                st.write(compute_services_df)

                st.subheader("People Cost")
                people_cost = project_details['People Cost']
                people_cost_df = pd.DataFrame(people_cost)
                people_cost_df['Time Remaining (hours)'] = people_cost_df['Time Proposed (hours)'] - people_cost_df[
                    'Time Spent (hours)']
                st.write(people_cost_df[
                             ['Name', 'Role', 'Time Proposed (hours)', 'Time Spent (hours)', 'Time Remaining (hours)',
                              'Cost ($)']])

    # People Productivity View
    with tabs[1]:
        st.header("People Productivity View")

        projects_df = get_projects()
        all_people_data = []
        for _, project in projects_df.iterrows():
            for person in project['People Cost']:
                person_data = person.copy()
                person_data['Project Name'] = project['Project Name']
                all_people_data.append(person_data)
        all_people_df = pd.DataFrame(all_people_data)

        if not all_people_df.empty:
            for index, person in all_people_df.iterrows():
                st.subheader(f"{person['Name']} - {person['Role']}")
                cols = st.columns(3)
                cols[0].write(f"**Project Name:** {person['Project Name']}")
                cols[1].write(f"**Time Proposed (hours):** {person['Time Proposed (hours)']}")
                cols[2].write(f"**Time Spent (hours):** {person['Time Spent (hours)']}")
                st.write(
                    f"**Time Remaining (hours):** {person['Time Proposed (hours)'] - person['Time Spent (hours)']}")
                cols = st.columns(2)
                cols[0].write(f"**Cost ($):** ${person['Cost ($)']:,.2f}")
                cols[1].write(
                    f"**Percentage of Time Spent:** {person['Time Spent (hours)'] / person['Time Proposed (hours)'] * 100:.2f}%")

                if st.button(f"Edit {person['Name']}", key=f"edit_person_{index}"):
                    st.session_state.selected_person = index
                    st.session_state.edit_people_mode = True
                    refresh_state()

                st.markdown("---")
        else:
            st.write("No people data available.")

    # Add New Project
    with tabs[2]:
        st.header("Add New Project")

        if 'projects_input' not in st.session_state:
            st.session_state.projects_input = []

        def add_project_row():
            st.session_state.projects_input.append({
                'Project Name': '',
                'Product Leader': '',
                'Engineering Leader': '',
                'Projected Revenue ($)': 0.0,
                'Start Date': '',
                'Timeline Proposed (months)': 0,
                'Time Spent (hours)': 0,
                'Compute and Services Cost': [],
                'People Cost': []
            })

        def remove_project_row(idx):
            st.session_state.projects_input.pop(idx)

        if st.button("Add Project Row"):
            add_project_row()

        projects_to_add = []
        for idx, project in enumerate(st.session_state.projects_input):
            st.markdown(f"**Project {idx + 1}**")
            cols = st.columns([1, 1, 1])
            project['Project Name'] = cols[0].text_input("Project Name", value=project['Project Name'],
                                                         key=f"project_name_{idx}")
            project['Product Leader'] = cols[1].text_input("Product Leader", value=project['Product Leader'],
                                                           key=f"product_leader_{idx}")
            project['Engineering Leader'] = cols[2].text_input("Engineering Leader",
                                                               value=project['Engineering Leader'],
                                                               key=f"engineering_leader_{idx}")
            project['Projected Revenue ($)'] = st.number_input("Projected Revenue ($)",
                                                               value=project['Projected Revenue ($)'], min_value=0.0,
                                                               step=1000.0, key=f"projected_revenue_{idx}")
            project['Start Date'] = st.date_input("Start Date", key=f"start_date_{idx}")
            project['Timeline Proposed (months)'] = st.number_input("Timeline Proposed (months)",
                                                                    value=project['Timeline Proposed (months)'],
                                                                    min_value=0, step=1, key=f"timeline_{idx}")
            project['Time Spent (hours)'] = st.number_input("Time Spent (hours)", value=project['Time Spent (hours)'],
                                                            min_value=0, step=1, key=f"time_spent_{idx}")

            st.subheader(f"Compute and Services Cost for Project {idx + 1}")
            if f'compute_services_cost_{idx}' not in st.session_state:
                st.session_state[f'compute_services_cost_{idx}'] = []

            def add_compute_service_cost(idx=idx):
                st.session_state[f'compute_services_cost_{idx}'].append({'Cost Name': '', 'Cost Amount': 0.0})

            if st.button(f"Add Compute/Service Cost Item for Project {idx + 1}", key=f"add_compute_service_{idx}"):
                add_compute_service_cost()

            compute_services_cost = []
            for c_idx, cost in enumerate(st.session_state[f'compute_services_cost_{idx}']):
                st.write(f"Cost Item {c_idx + 1}")
                cols = st.columns([1, 1, 1])
                cost['Cost Name'] = cols[0].text_input("Cost Name", value=cost['Cost Name'],
                                                       key=f"compute_service_cost_name_{idx}_{c_idx}")
                cost['Cost Amount'] = cols[1].number_input("Cost Amount", value=cost['Cost Amount'], min_value=0.0,
                                                           step=10.0, key=f"compute_service_cost_amount_{idx}_{c_idx}")
                if cols[2].button("Remove", key=f"remove_compute_service_{idx}_{c_idx}"):
                    st.session_state[f'compute_services_cost_{idx}'].pop(c_idx)
                compute_services_cost.append(cost)
            project['Compute and Services Cost'] = compute_services_cost

            st.subheader(f"People Cost for Project {idx + 1}")
            if f'people_cost_{idx}' not in st.session_state:
                st.session_state[f'people_cost_{idx}'] = []

            def add_people_cost(idx=idx):
                st.session_state[f'people_cost_{idx}'].append(
                    {'Name': '', 'Role': '', 'Time Proposed (hours)': 0, 'Time Spent (hours)': 0, 'Cost ($)': 0.0})

            if st.button(f"Add People Cost Item for Project {idx + 1}", key=f"add_people_cost_{idx}"):
                add_people_cost()

            people_cost = []
            for p_idx, person in enumerate(st.session_state[f'people_cost_{idx}']):
                st.write(f"Person {p_idx + 1}")
                cols = st.columns([1, 1, 1])
                person['Name'] = cols[0].text_input("Name", value=person['Name'], key=f"person_name_{idx}_{p_idx}")
                person['Role'] = cols[1].text_input("Role", value=person['Role'], key=f"person_role_{idx}_{p_idx}")
                if cols[2].button("Remove", key=f"remove_person_{idx}_{p_idx}"):
                    st.session_state[f'people_cost_{idx}'].pop(p_idx)
                person['Time Proposed (hours)'] = st.number_input("Time Proposed (hours)",
                                                                  value=person['Time Proposed (hours)'], min_value=0,
                                                                  step=1, key=f"time_proposed_{idx}_{p_idx}")
                person['Time Spent (hours)'] = st.number_input("Time Spent (hours)", value=person['Time Spent (hours)'],
                                                               min_value=0, step=1, key=f"time_spent_{idx}_{p_idx}")
                person['Cost ($)'] = st.number_input("Cost ($)", value=person['Cost ($)'], min_value=0.0, step=100.0,
                                                     key=f"person_cost_{idx}_{p_idx}")
                people_cost.append(person)
            project['People Cost'] = people_cost

            total_cost, compute_services_total, people_total = calculate_total_cost(project)
            project['Total Cost ($)'] = total_cost

            if st.button("Remove Project", key=f"remove_project_{idx}"):
                remove_project_row(idx)

            projects_to_add.append(project)
            st.markdown("---")

        if st.button("Add Projects"):
            if projects_to_add:
                projects_df = pd.DataFrame(projects_to_add)
                if projects_df['Project Name'].isnull().any() or projects_df['Project Name'].str.strip().eq('').any():
                    st.error("All projects must have a 'Project Name'.")
                else:
                    if 'Start Date' in projects_df.columns:
                        projects_df['Start Date'] = projects_df['Start Date'].astype(str)
                    st.session_state.projects_df = pd.concat([st.session_state.projects_df, projects_df],
                                                             ignore_index=True)
                    st.success("Projects added successfully!")
                    st.session_state.projects_input = []
                    keys_to_remove = [key for key in st.session_state.keys() if
                                      key.startswith('compute_services_cost_') or key.startswith('people_cost_')]
                    for key in keys_to_remove:
                        del st.session_state[key]
                    refresh_state()  # Trigger page refresh
            else:
                st.warning("No project data to add.")


if __name__ == "__main__":
    main()
