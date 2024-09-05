import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🤖 JanaBot")
st.write(
    "Hi, I'm JanaBot!"
    "I'm your virtual assistant. Let me know what information you're looking for and I will direct you to the correct report. "
    "You can ask me anything and I will do my best to help you, or ask for more information."
)

dashboard_information = """
    Turnover Report: Metrics and data concerning new starters, leavers (terminated employees), and headcount turnover
    HR Custom Forms: Basic data output for custom forms
    Right To Work (HR): An aggregation of right to work document data stored in Sona.
    Employee Directory: Personal information about staff members (leavers and active), including “Next of Kin”, “Length of Service” & “Working Preferences” reports
    Birthdays: Upcoming birthdays for employees including contact details
    Shifts Overview: A very simple way to look at shifts from multiple locations, date ranges, employees etc at once and export them
    Contracted Hours: A comparison of rostered or clocked hours against contracted hours
    Absence: Metrics and data concerning absences, including an ‘Absent Today’ report and ‘Consecutive Absences’ report
    Holiday: Holiday requests, holiday allowance, holiday entitlement (taken, booked, remaining)
    Shift Fulfilment: Analysis of shifts and hours by allocation (claimed in app or assigned by manager) and by fulfilment status (claimed, unclaimed, assigned)
    Rota Compliance: Percentages of allocated shifts on the roster by week
    Time and Attendance: Time and attendances analysis against the related rostered shifts
    Agency Usage: An overview of agency staff usage communicating why, where and when agency staff have been used.
    Fire Report: Employees currently on site
    Absence Map: A pivot overview of absences over several months
    Current Pay Rates: Current pay rates for employees (can be filtered to a historic date to view the then-current rates)
    Wages Overview: 
    Commissioned Hours: Over and under staffing analysis for PWSs
    Sleep In Report: Who is working or scheduled to work sleep in shifts, where and when
    Open Pay Queries: An aggregate of unresolved pay queries (flags)
    Shift Cancellations: Metrics and data concerning cancelled shifts
    Workforce Demographics: Analysis of the workforce's demographics. Including information on age, gender and seniority
    Shifts Worked In Other Locations: Shifts worked in locations that aren’t employees’ primary locations
    Locked Weeks Overview: An overview of locked and unlocked weeks within a specified organization, allowing users to filter and view details such as department, date range, and locking status (indicated by visual icons), facilitating easy tracking and management of locked periods
    Reporting Lines and Permissions: Who employees report to and what their permission roles and levels are
    Overlapping Payroll Records: Catch and fix payroll records that will block payroll run submissions
    Audit Logs: A very simple data collection for all events on shifts
    Address Details Change Flag: Flag if an employee’s address details have changed
    Gender Pay Gap: Reporting the difference between the average pay of men and women in an organisation.
    """

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.secrets["api_key"]


if not openai_api_key:
     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

#     # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:
        st.session_state.messages = [{"role": "system", "content": f"You are a Standard Reporting expert helping people understand what information is available in what report. Answer either with name of one or more reports from provided list or by saying you don't have enough information to answer. In the provided file is the list of reports with their descriptions:{dashboard_information}. Do not provide any advice or information except which report or combination of reports to use, or information about the reports."},
            ]


    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        if message["role"] == "user" or message["role"] == "assistant":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Ask JanaBot a question..."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
