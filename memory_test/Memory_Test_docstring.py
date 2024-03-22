from IPython. display import display, HTML, Image, clear_output
import time
import ipywidgets as widgets
from jupyter_ui_poll import ui_events
import requests
from bs4 import BeautifulSoup
import random
import json 
import pandas as pd
import matplotlib.pyplot as plt

# Global dictionary to store information about buttons
event_info = {
    'type': '', # Type of the event (e.g., 'click')
    'description': '',
    'time': -1 
}

def wait_for_event(interval=0.001, max_rate=20, allow_interupt=True):    
    """
    This function monitors for user interactions (button clicks in this case)
    
    When the function detects an interaction, it gathers information like what kind of interaction it was, a brief description, and when it happened. 
    
    Parameters:
    - interval (float): Time in seconds to wait between polls.
    - max_rate (int): Maximum number of events to process in a single poll.
    - allow_interupt (bool): If True, returns immediately when an event is detected.
    
    This function returns: a dictionary with the type, description, and time of button click. 
    """
    start_wait = time.time()
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:
            # process UI events
            ui_poll(n_proc)

            # end loop if event has occured
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                
            # add pause before looping to check events again
            time.sleep(interval)
    
    # will be set to empty string '' if no event occured
    return event_info

def register_event(btn):
    """
    This function will be called when a button is clicked. It updates the global
    event_info dictionary with the type of event ('click'), the button's description, and the
    time the event occurred.
    
    Parameters:
    - btn: Expected to have a 'description' attribute.
    """
    # display button description in output area
    event_info['type'] = "click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return
    
    
    #Define a list of button descriptions
button_options= ["a", "b", "c",">9","7-9","<7", "female", "male", "non-binary", "prefer no to say"]
#Creates a button for each option in the list above
btn1= widgets.Button(description= button_options[0])
btn2= widgets.Button(description= button_options[1]) 
btn3= widgets.Button(description= button_options[2]) 
btn4= widgets.Button(description= button_options[3])
btn5= widgets.Button(description= button_options[4]) 
btn6= widgets.Button(description= button_options[5]) 
btn7= widgets.Button(description= button_options[6])
btn8= widgets.Button(description= button_options[7])
btn9= widgets.Button(description= button_options[8])
btn10= widgets.Button(description= button_options[9])
#The 'register_event' function is called everytime a button is clicked
btn1.on_click(register_event) 
btn2.on_click(register_event)
btn3.on_click(register_event)
btn4.on_click(register_event)
btn5.on_click(register_event)
btn6.on_click(register_event)
btn7.on_click(register_event)
btn8.on_click(register_event)
btn9.on_click(register_event)
btn10.on_click(register_event)


def send_to_google_form(data_dict, form_url):
    """
    This function Submits data to a Google Form.
    
    Parameters:
    - data_dict: Expected to have a dictionary with keys corresponding to the Google Form field names and value being data to be submitted for those fields.
    - form_url: The URL of the Google Form where data is to be submitted.
    
    This function returns: True if the form submission is successful, False otherwise.
    """

    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}
    
    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
    
    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok


def display_grid(image, clear=False):
    """
    This function displays the images stored in in the Local File System.
    If the clear parameter is set to True, the displayed image will be cleared from the output after a 20-second delay. 
    Otherwise, the function will simply wait for a short duration before proceeding.
    
    Parameters:
    -image: expected to have the string variable with the image name same as in the local file system.
    -clear (bool): A flag to indicate whether to clear the displayed image after a delay.
    """
    img = Image(image, width = 300)
    display(img)
    #All images requiring users to memorize will be given a boolean value to be True
    if clear == True:
        time.sleep(5)
        clear_output()
        time.sleep(0.5)
    #Images as a component of the question will be given a boolean value to be False
    else:
        time.sleep(0.1)# Not cleared so users do not need to memorize.
        
# A list of sentences to be displayed as an introduction to the test.
sentences = ["Welcome to a memory test for you to showoff your big brain:3",
                 "Enter your ID:",
                 "Please enter the hours of sleep you had last night:",
                 "Please indicate your gender:",
                 "In this test, you will be given a few graphs with different shapes in various colors",
                 "You will need to memorize it as much as possible to answer the following multiple choice questions",
                 "You will be given 20 seconds each time the graph appears",
                 "Be prepared for increasingly complex graphs as you progress",
                 "The total time you used and your score will be displayed at the end of the test:)",
                 "Now the test begins in:",
                 "3",
                 "2",
                 "1"]
durations = [4, 1, 1, 1, 4, 5, 4, 4, 4, 2, 1, 1, 1]

id_instructions = """

Enter your anonymised ID

To generate an anonymous 4-letter unique user identifier please enter:
- two letters based on the initials (first and last name) of a childhood friend
- two letters based on the initials (first and last name) of a favourite actor / actress

e.g. if your friend was called Charlie Brown and film star was Tom Cruise
     then your unique identifier would be CBTC
"""

def display_intro(sentences, durations):
    """
    This function displays a sequence of sentences to user, each takes a specified duration. 
    It also collect and store user's input to specific points in the sequence. 
    
    Parameters:
    - sentences (list): A list of string sentences to be displayed to the user.
    - durations (list): A list of durations (in seconds) corresponding to how long each sentence should displayed.
    """
    for idx in range(len(sentences)):
        sentence = sentences[idx]
        duration = durations[idx]
        html_output = HTML(f"<h2>{sentence}</h2>")
        display(html_output)
        if idx==1:
            print(id_instructions)
            ID= input("")
            data_dict["ID"] = ID
            clear_output(wait = True)
            html_output = HTML(f"<h2>Hi,{ID}!</h2>")
            display(html_output)
        elif idx==2:
            display(widgets.HBox([btn4, btn5, btn6]))
            wait_for_event()
            hour_sleep = event_info["description"]
            data_dict["hour_sleep"] = hour_sleep
            clear_output(wait = True)
        elif idx==3:
            display(widgets.HBox([btn7, btn8, btn9, btn10]))
            wait_for_event()
            gender = event_info["description"]
            data_dict["gender"] = gender
            clear_output(wait = True)
        else:
            time.sleep(duration)
            clear_output(wait=True)

            
q1 = {"What color was the circle?(a) orange (b) blue (c) pink": "a",
      "What color was the triangle?(a) green (b) blue (c) orange": "b",
      "Which shape was yellow? (a) rectangle (b) trapezoid (c) sqaure": "b",
      "Which shape was green? (a) square  (b) pentagon (c) circle": "a"}

q2 = {"what shape was in position A? (a) circle (b) rectangle (c) sqaure": "c",
     "what shape was in position B? (a) triangle (b) trapezoid (c) hexagon": "b",
     "what shape was in position C? (a) circle (b) triangle (c) sqaure": "b"}

q3 = {"What color was the circle?(a) red (b) blue (c) pink": "a",
      "What color was the oval?(a) yellow (b) purple (c) pink": "b",
      "What color was the triangle?(a) green (b) blue (c) orange": "a",
      "What color was the diamond?(a) red (b) green (c) purple": "c",
     "Which shape was pink? (a) oval (b) star (c) sqaure": "b",
      "Which shape was orange? (a) circle  (b) pentagon (c) rectangle": "b"}


q4 = {"what shape was in position A? (a) star (b) rectangle (c) sqaure": "a",
     "what shape was in position B? (a) circle (b) hexagon (c) oval": "b",
     "what shape was in position C? (a) pentagon (b) diamond (c) circle": "c"}

q5 = {"What color was the oval?(a) yellow (b) blue (c) green": "a",
      "What color was the circle?(a) yellow (b) purple (c) pink": "b",
      "What color was the heart?(a) red (b) green (c) purple": "b",
     "Which shape was pink? (a) triangle (b) star (c) diamond": "c",
      "Which shape was black? (a) sun  (b) parallelogram (c) plus": "b",
      "Which shape was white? (a) triangle  (b) trapezoid (c) lightning": "c",
     "What shape was below the heart? (a) circle (b) pentagon (c) sqaure": "b",
     "How many shapes maximum are in the same color? (a)2 (b)3 (c)4": "a"}

q6 = {"what shape was in position A? (a) oval (b) rectangle (c) plus": "c",
     "what shape was in position B? (a) triangle (b) heart (c) hexagon": "b",
     "what shape was in position C? (a) circle (b) arrow (c) sqaure": "b",
      "what shape was in position D? (a) lightning (b) diamond (c) sun": "c",
      "what shape was in position E? (a) triangle (b) hexagon (c) pentagon": "b"}


def analyze_graph(graph_name, questions, boolean):
    """
    This function will displays an image of a graph, asks the user a series of 
    questions related to the graph in a multiple-choice format, and calculates the user's score based on their answers. 
    
    The image will cleared from the display after the questions are asked.
    
    Parameters:
    - graph_name (str): The base name of the image file be displayed. This function assumes a '.PNG' extension for the image files.
    - questions (dict): A dictionary where each key is a string representing to a question and each value is the 
                        correct answer to that question. 
    - boolean (bool): A flag indicating whether to clear the displayed image after asking the questions. 
    Returns:
    """
    
    image = f'{graph_name}.PNG'
    
  # Ask the user a question in multiple choice format
    
    display_grid(image, clear=boolean)
    # Ask the user questions about the grid
    panel = widgets.HBox([btn1, btn2, btn3])
    
    score = 0
    for question_num, question in enumerate(questions, start=1):
        progress = widgets.IntProgress(value=question_num-1, min=0, max=len(questions), step=1, description=f"Q{question_num}/{len(questions)}")
        display(progress)
        html_out = HTML(f"<span>{question}</span>")
        display(html_out, panel)
        wait_for_event()
        answer = event_info["description"]
        data_dict["user_answer"].append(answer)
        if answer == questions[question]:
            score += 1
        clear_output()
        if boolean == False:
            display_grid(image)
    return score, len(questions)



#compare to class data
def visual(user_score):
    """
    This function provide a comparison to participants their performance with data collected before.
    To made more obviously, a boxplot displayed user's result as red dots to achieve easier comparison.
    
    Parameters:
    - user_score (int): The participant's score to be highlighted on the plot. This represents the number of
                        correct answers participant achieved in the test.
    """
    memory= pd.read_csv("memory_test.csv")
    df = memory[["ID", "n_correct_answers"]].set_index("ID")
    df.boxplot(column = ["n_correct_answers"])
    plt.scatter(x=[1], y=[user_score], color='red', label='Your Score')
    plt.title("View Your Performance Against Class Data")
    plt.legend()
    plt.show()
    return

data_dict= {"ID": [],
            "duration": [],
            "n_correct_answers": [],
            "hour_sleep": [],
            "gender": [],
            "user_answer": []}
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdIXdOiQSkp4EdwuNLYw7547Wtg5NVYTpvWh6YQPNYvyGstqw/viewform?usp=sf_link"

def main():
    """
    This function combined upper functions to giveout the main part of Memory Test.
    By accept participan't permit, introduction displayed and the test start.
    Graphs presented by level, followed with related questions.
    User's response collected and scored.
    Conclusion and boxplot shows for user to do comparison.
    Information be collected and send to Google Form for analysis.
    """

    data_consent_info = """DATA CONSENT INFORMATION:

    Please read:

    We wish to record your response data
    to an anonymised public data repository. 
    Your data will be used for educational teaching purposes
    practising data analysis and visualisation.

    Please type   yes   in the box below if you consent to the upload."""

    print(data_consent_info)
    
    text_input = input("")
    if text_input == "yes":
        #show introduction
        display_intro(sentences, durations)
        #timing start
        start_time = time.time()
        # Analyze the first graph
        score1, len1 = analyze_graph('Picture1', q1, True)

        clear_output(wait=True)
        #question with the picture
        score2, len2 = analyze_graph('Picture2', q2, False)

        clear_output(wait=True)

        # Analyze the second graph
        score3, len3 = analyze_graph('Picture3', q3, True)

        clear_output(wait=True)

        score4, len4 = analyze_graph('Picture4', q4, False)

        clear_output(wait=True)

        score5, len5 = analyze_graph('Picture5', q5, True)

        clear_output(wait=True)

        score6, len6 = analyze_graph('Picture6', q6, False)

        clear_output(wait=True)
        #timing ends
        end_time = time.time()

        #calculate time taken
        time_taken = end_time - start_time
        rounded_time = round(time_taken, 2)
        data_dict["duration"] = rounded_time

        total_score = score1 + score2 + score3 + score4 + score5 + score6
        data_dict["n_correct_answers"] = total_score
        total_questions = len1 + len2 + len3 + len4 + len5 + len6

        conclusion_1 = (f"You got {total_score}/{total_questions} correct.\n",
                      f"You used {rounded_time} seconds to complete the test. Very good job!\n",
                      "End of the game! Thanks for your participation.")

        html_output = HTML(f"""<h2>{conclusion_1[0]}</h2>
                           <h2>{conclusion_1[1]}</h2>
                           <h2>{conclusion_1[2]}</h2>""")
        display(html_output)
        
        visual(total_score)

        send_to_google_form(data_dict, form_url)
    else: 
        html_output = HTML("<h2>Thanks for your participation. Hope you have a nice day!</h2>")
        display(html_output)
        
if __name__ == "__main__":
    main()