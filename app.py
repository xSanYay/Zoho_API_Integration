import requests
import json
from datetime import datetime

# Constants
ACCESS_TOKEN = "PUT YOUR ACCESS TOKEN"
EMPLOYEE_SEARCH_API = "https://people.zoho.in/people/api/forms/P_Employee/getRecords?sIndex=1&limit=100"
LEAVE_API_URL = "https://people.zoho.in/people/api/forms/json/P_ApplyLeave/insertRecord"
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

LEAVE_TYPES = {
    "CL": "203716000000270060",
    "EL": "203716000000270068",
    "LWP": "203716000000270080",
    "PL": "203716000000270076",
    "SBL": "203716000000270084",
    "SL": "203716000000270064"
}

# Functions
def get_employee_id(employee_name):
    headers = {
        "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {"query": employee_name}
    response = requests.get(EMPLOYEE_SEARCH_API, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("response") and data["response"].get("result"):
            for record in data["response"]["result"]:
                for employee_id, employee_list in record.items():
                    for employee in employee_list:
                        full_name = f"{employee.get('FirstName')} {employee.get('LastName')}"
                        if full_name.lower() == employee_name.lower():
                            return employee_id
            return "Employee not found."
    return "Error fetching employee data."

def request_leave(employee_name, leave_date, from_date, to_date, reason):
    employee_id = get_employee_id(employee_name)
    if "not found" in employee_id.lower():
        return employee_id
    return f"Requesting leave for {employee_name} (ID: {employee_id}) from {from_date} to {to_date} for reason: {reason}. Confirm? (yes/no)"

def process_leave(employee_name, leave_type, from_date, to_date):
    employee_id = get_employee_id(employee_name)
    if "not found" in employee_id.lower():
        return employee_id

    headers = {
        "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputData": json.dumps({
            "Employee_ID": employee_id,
            "Leavetype": leave_type,
            "From": from_date,
            "To": to_date,
            "days": {
                from_date: {
                    "LeaveCount": 1,
                    "Session": 1
                }
            }
        })
    }
    response = requests.post(LEAVE_API_URL, headers=headers, params=payload)
    if response.status_code == 200:
        return "Leave processed successfully."
    return f"Error processing leave: {response.text}"

def get_leave_balance_for_employee(employee_name):
    # Dummy response as an example
    return f"Leave balance for {employee_name}: 10 CL, 5 EL, 3 SL."

# Chatbot logic
def chatbot():
    print("Welcome to the HR chatbot!")
    print("How can I assist you today?")

    while True:
        user_input = input("You: ").strip().lower()

        if "leave balance" in user_input:
            employee_name = input("Please enter your name: ")
            response = get_leave_balance_for_employee(employee_name)
        
        elif "request leave" in user_input:
            employee_name = input("Enter your name: ")
            leave_date = input("Enter leave date (dd-MMM-yyyy): ")
            from_date = input("Enter start date (dd-MMM-yyyy): ")
            to_date = input("Enter end date (dd-MMM-yyyy): ")
            reason = input("Enter reason for leave: ")
            response = request_leave(employee_name, leave_date, from_date, to_date, reason)
        
        elif "approve leave" in user_input:
            employee_name = input("Enter your name: ")
            leave_type = input(f"Enter leave type code ({', '.join(LEAVE_TYPES.keys())}): ").upper()
            from_date = input("Enter start date (dd-MMM-yyyy): ")
            to_date = input("Enter end date (dd-MMM-yyyy): ")
            if leave_type in LEAVE_TYPES:
                response = process_leave(employee_name, LEAVE_TYPES[leave_type], from_date, to_date)
            else:
                response = "Invalid leave type."
        
        elif "exit" in user_input:
            print("Goodbye!")
            break
        
        else:
            response = "I'm sorry, I didn't understand that. Please try again."
        
        print(f"Bot: {response}")

# Start the chatbot
chatbot()
