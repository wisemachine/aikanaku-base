import streamlit as st
import pandas as pd
import io

# Function to load data from CSV
def load_csv(file):
    if file is not None:
        data = pd.read_csv(file)
        return data
    else:
        return None

# Streamlit App Layout
st.title("AI Governance Insights Dashboard")

# 1. Project Name
st.header("Project Information")
project_name = st.text_input("Enter Project Name")

# Option to input data: CSV or Text
st.subheader("Data Input Method")
input_method = st.radio("Choose data input method:", ('Upload CSV File', 'Manual Input'))

# Initialize variables
aws_data = None
jira_data = None
people_data = None
compliance_data = None

if input_method == 'Upload CSV File':
    # CSV file upload
    uploaded_file = st.file_uploader("Upload your CSV file here", type="csv")

    if uploaded_file:
        # Read CSV and separate into different dataframes based on sheet names or headers
        try:
            aws_data = pd.read_csv(uploaded_file, sheet_name='AWSData')
            jira_data = pd.read_csv(uploaded_file, sheet_name='JiraData')
            people_data = pd.read_csv(uploaded_file, sheet_name='PeopleData')
            # Assuming compliance data is in a separate sheet
            compliance_data = pd.read_csv(uploaded_file, sheet_name='ComplianceData')
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
else:
    # Manual Input
    st.subheader("Manual Data Entry")

    # AWS Data
    st.subheader("AWS Services Compute Information")
    aws_service = st.text_input("AWS Service")
    aws_resource = st.text_input("Resource Name")
    aws_cost = st.number_input("Cost", min_value=0.0)
    aws_time_used = st.number_input("Time Used (hours)", min_value=0)
    aws_start_date = st.date_input("Start Date")

    if aws_service and aws_resource:
        aws_data = pd.DataFrame({
            'Service': [aws_service],
            'Resource Name': [aws_resource],
            'Cost': [aws_cost],
            'Time Used (hours)': [aws_time_used],
            'Start Date': [aws_start_date]
        })

    # Jira Data
    st.subheader("Jira Tickets Data")
    completed_tickets = st.number_input("Completed Tickets", min_value=0)
    in_progress_tickets = st.number_input("In Progress Tickets", min_value=0)
    todo_tickets = st.number_input("To Do Tickets", min_value=0)

    if completed_tickets or in_progress_tickets or todo_tickets:
        jira_data = pd.DataFrame({
            'Status': ['Completed', 'In Progress', 'To Do'],
            'Count': [completed_tickets, in_progress_tickets, todo_tickets]
        })

    # People Data
    st.subheader("People Associated with Project")
    person_name = st.text_input("Person Name")
    person_role = st.text_input("Role")
    person_time_spent = st.number_input("Time Spent (hours)", min_value=0)
    person_hourly_rate = st.number_input("Hourly Rate", min_value=0)

    if person_name and person_role:
        people_data = pd.DataFrame({
            'Name': [person_name],
            'Role': [person_role],
            'Time Spent (hours)': [person_time_spent],
            'Hourly Rate': [person_hourly_rate]
        })

    # Compliance Data (Manual entry for demonstration)
    st.subheader("Regulatory Compliance Data")
    compliance_data = {
        'AI Compliance': ['EU AI Act', 'NYC Law No. 144', 'Colorado Law SB21-169'],
        'Standards & Guidelines': ['EEOC Technical Assistance on ADA & AI', 'DIU Responsible AI Guidelines', 'NIST AI RMF, SR 11'],
        'Industry Best Practices': ['The Data & Trust Alliance']
    }

# Display Data and Insights

if aws_data is not None:
    st.subheader("ML Services Compute Information")
    st.write("AWS Resources used in the project:")
    st.dataframe(aws_data)

if jira_data is not None:
    st.subheader("Project Progress")
    st.write("Overall Score: 7/10")
    st.write("Jira Tickets Progress:")
    st.bar_chart(jira_data.set_index('Status'))

if people_data is not None:
    st.subheader("People Associated with Project and Time Spent")
    st.write("Calculating running cost based on billable hours for each person:")
    people_data['Running Cost'] = people_data['Time Spent (hours)'] * people_data['Hourly Rate']
    st.dataframe(people_data)

# 7. Potential Business Value
st.subheader("Potential Business Value")
potential_value = st.number_input("Enter estimated business value ($)", min_value=0)
st.write(f"Estimated Potential Business Value: ${potential_value}")

# 8. Input Data
st.subheader("Input Data")
st.write("Input data details:")
st.write("Location: AWS S3 - InputBucket")
st.write("Access permissions: Restricted to Data Engineers")
st.write("Data size: 150GB")

# 9. Output Data
st.subheader("Output Data")
st.write("Output data details:")
st.write("Format: CSV, JSON")
st.write("Location: AWS S3 - OutputBucket")

# 10. Regulatory Compliance
st.subheader("Regulatory Compliance")
st.write("Details on compliance with various AI regulations:")
if compliance_data:
    st.write("AI Compliance Laws:")
    for law in compliance_data['AI Compliance']:
        st.write(f"- {law}")
    st.write("Standards & Guidelines:")
    for guideline in compliance_data['Standards & Guidelines']:
        st.write(f"- {guideline}")
    st.write("Industry Best Practices:")
    for practice in compliance_data['Industry Best Practices']:
        st.write(f"- {practice}")
