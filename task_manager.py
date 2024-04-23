# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# - Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # - Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(
        task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


def update_task_file(task_list):
    """Updates the task.txt file with the new set of tasks that have 
        been changed locally in the task_list"""
    # - open tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        # - itterate through tasks and convert to an array
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        # - write the formatted tasks to the file
        task_file.write("\n".join(task_list_to_write))


def reg_user():
    """Add a new user to the user.txt file"""

    # - Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # - Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    # - Request input of a new username
    new_username = input("New Username: ")

    if new_username not in username_password.keys():

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")

    else:
        # - print error message for duplicate user registeration
        print(f'''
              Error: The username - {new_username} is already taken. 
              Try registering with a different username''')


def add_task():
    """Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task."""
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    # - Else statement is used to replace continue statement outside of loop
    else:
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(
                    task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # - Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
                Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")


def view_mine():
    """Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)"""

    # - Number the task list
    task_list_num = enumerate(task_list)
    # - Initialise empty array and counter to track the tasks on different arrays
    task_map = {}
    counter = 0
    # - Iterate through the enumerated task list
    for t in task_list_num:
        if t[1]['username'] == curr_user:
            # - Create formatted print statement using line breaks
            disp_str = str(counter) + "\n"
            disp_str += f"Task {str(counter)}: \t\t {t[1]['title']}\n"
            disp_str += f"Assigned to: \t {t[1]['username']}\n"
            disp_str += f"Date Assigned: \t {t[1]['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t[1]['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t[1]['description']}\n"
            print(disp_str)
            task_map[counter] = t[0]
            counter += 1
    # - Print the next menu
    task_menu = "Select one of the following tasks below by entering the corresponding value: \n"
    # - For loop iterates through task map to find the users task in original array
    for x in task_map:
        # - Fstring generated for each task
        task_menu += f"{str(x)} -  select task {str(x)}: {task_list[task_map[x]]['title']} \n"
    task_menu += f"-1 - return to the main menu \n"
    task_menu += ":"
    task_choice = input(task_menu)
    # - If statement checks value inputed
    if task_choice == "-1":
        print("\n")
    # - Check if input integer corresponds to a user task
    elif int(task_choice) in task_map.keys():
        # - Give user option to edit or mask task using input
        second_question = f"\nPlease enter either- \n"
        second_question += f"'edit' - to edit task {task_choice} OR \n"
        second_question += f"'mark' - to mark task {task_choice} as complete:"
        second_response = input(second_question)
        # - User chooses to edit task
        if second_response == "edit":
            # - Check if task has been completed
            if task_list[task_map[int(task_choice)]]['completed'] == True:
                print(
                    f'Task {task_choice} cannot be edited it has already been completed')
            else:
                # - Give user option to select user or date
                third_question = f"\n \nPlease enter either - \n"
                third_question += f"'user' - to change the user task {task_choice} is assigned to OR \n"
                third_question += f"'date' -  to change the due date of task {task_choice}:"
                third_response = input(third_question)

                # - User chooses to edit user
                if third_response == "user":
                    # - Read in user_data
                    with open("user.txt", 'r') as user_file:
                        user_data = user_file.read().split("\n")

                    # - Convert to a dictionary using for loop and split method
                    username_password = {}
                    for user in user_data:
                        username, password = user.split(';')
                        username_password[username] = password
                    new_user = input(
                        f"Please enter the new user assigned to task {task_choice}:")
                    # - Check if user is registered
                    if new_user in username_password.keys():
                        # - Update task list and tasks.txt file
                        task_list[task_map[int(task_choice)]
                                  ]['username'] = new_user
                        update_task_file(task_list)
                        print(f'Task {task_choice} has been updated')
                    else:
                        # - Else statement triggers print of error message
                        print(
                            f"Error. {new_user} is not a registered username. Try again")

                # - User chooses to edit due date
                elif third_response == "date":
                    # - Prompt user to input the new due date
                    while True:
                        try:
                            new_task_due_date = input(
                                f"Please enter the new due date of task {task_choice} (YYYY-MM-DD): ")
                            due_date_time = datetime.strptime(
                                new_task_due_date, DATETIME_STRING_FORMAT)
                            break
                        # - Except block will catch incorrect formatted inputs
                        except ValueError:
                            print(
                                "Invalid datetime format. Please use the format specified")
                    # - change the date in the task list and update the tasks.txt file
                    task_list[task_map[int(task_choice)]
                              ]['due_date'] = due_date_time
                    update_task_file(task_list)

                    # - Print relevant message
                    print(f'Task {task_choice} has been updated \n')
                else:
                    # - Print error message if inputed value is not on menu
                    print("Error: Inputed value is not on the menu. Try again!")
        elif second_response == "mark":
            # - Check if task selected has already been completed
            if task_list[task_map[int(task_choice)]]['completed'] == True:
                # - Print message
                print(f'Task {task_choice} has already been completed')
            else:
                # - Mark task as complted and update the tasks.txt file
                task_list[task_map[int(task_choice)]]['completed'] = True
                update_task_file(task_list)
                print(f'Task {task_choice} has been marked completed \n')
        else:
            # - Print error message if inputed value is not on menu
            print("Error: Inputed value is not on the menu. Try again!")
    else:
        # - Print error message if inputed value is not on menu
        print("Error: Inputed value is not on the menu. Try again!")


def view_all():
    """ Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) """

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def generate_report():
    """ Generates reports, user_overview.txt and task_overview.txt, that contain statistics"""

    # - Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # - Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    # - Initialise counters to hold report statistics
    num_completed_tasks = 0
    num_overdue_tasks = 0

    # - Iterate through task list and update counter when conditions met
    for t in task_list:
        if t['completed'] == True:
            num_completed_tasks += 1
        elif t['completed'] == False and t['due_date'] < datetime.today():
            num_overdue_tasks += 1

    # - Calculating report statistics
    num_uncompleted_tasks = num_tasks - num_completed_tasks
    percentage_incomplete = (num_uncompleted_tasks / num_tasks) * 100
    percentage_overdue = (num_overdue_tasks / num_tasks) * 100

    # - Creating the report using f strings line by line
    task_report = "TASK OVERVIEW\n"
    task_report += f"The total number of tasks tracked:{num_tasks}\n"
    task_report += f"The total number of completed tasks:{num_completed_tasks}\n"
    task_report += f"The total number of uncompleted tasks:{num_uncompleted_tasks}\n"
    task_report += f"The total number of overdue tasks:{num_overdue_tasks}\n"
    task_report += f"The percentage of incomplete tasks:{percentage_incomplete:.2f}%\n"
    task_report += f"The percentage of overdue tasks:{percentage_overdue:.2f}%\n"

    # - Creating the report file and adding the completed f string
    with open("task_overview.txt", "w") as out_file:
        out_file.write(task_report)
    # - Begin forming the report using f strings line by line
    user_string = "USER OVERVIEW \n"
    user_string += f"The total number of users registered:{num_users}\n"
    user_string += f"The total number of tasks tracked:{num_tasks}\n"

    # - Iterate through users
    for u in username_password.keys():
        # - initialise counters at zero that will hold the statistics
        num_user_tasks = 0
        num_user_completed_tasks = 0
        num_user_overdue_tasks = 0

        # - Iterate through user tasks and update the counter when conditions met
        for t in task_list:
            if t['username'] == u:
                num_user_tasks += 1
            if t['username'] == u and t['completed'] == True:
                num_user_completed_tasks += 1
            if t['username'] == u and t['completed'] == False and t['due_date'] < datetime.today():
                num_user_overdue_tasks += 1
        # - Check if the user has zero tasks to prevent ZeroDivisionError
        if num_user_tasks == 0:
            user_string += f"-"*30 + "\n"
            user_string += f"* User - {u}\n"
            user_string += f"{num_user_tasks} total tasks assigned to {u}\n"
        else:
            # - Calculating report statistics
            percentage_user_tasks = (num_user_tasks/num_tasks)*100
            percentage_user_completed = (
                num_user_completed_tasks/num_user_tasks)*100
            percentage_user_incomplete = 100 - percentage_user_completed
            percentage_user_overdue = (
                num_user_overdue_tasks/num_user_tasks)*100

            # - Creating the report for each line by line using fstrings
            user_string += f"-"*30 + "\n"
            user_string += f"* User - {u}\n"
            user_string += f"{num_user_tasks} total tasks assigned to {u}\n"
            user_string += f"{percentage_user_tasks}% of total tasks are assigned to {u}\n"
            user_string += f"{percentage_user_completed}% of {u}'s tasks are completed\n"
            user_string += f"{percentage_user_incomplete}% of {u}'s tasks are incomplete\n"
            user_string += f"{percentage_user_overdue}% of {u}'s tasks are overdue\n"

    # - Creating the report file
    with open("user_overview.txt", "w") as out_file:
        out_file.write(user_string)


def display_statistics():
    """If the user is an admin they can display statistics about number of users
        and tasks."""
    # - Produce the reports where the data is read from
    generate_report()

    print("\n")
    # - Read the task_overview.txt report generated and collect data
    with open("task_overview.txt", 'r') as task_report:
        task_report_data = task_report.read()
    # - Print result to admin terminal
    print(task_report_data)
    print("\n")

    # - Read the user_overview.txt report generated and collect data
    with open("user_overview.txt", 'r') as user_report:
        user_report_data = user_report.read()
    # - Print result to admin terminal
    print(user_report_data)


'''
LOGIN SECTION
This code reads usernames and password from the user.txt file to 
allow a user to login
'''

# - If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# - Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# - Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # - Presenting the menu to the user and
    # - Making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        generate_report()

    elif menu == 'ds' and curr_user == 'admin':
        display_statistics()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
