import matplotlib.pyplot as plt
import numpy as np
from IPython import display
import time
from matplotlib.patches import Ellipse
import requests
from bs4 import BeautifulSoup
import os
import json 
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from jupyter_ui_poll import ui_events

#This part is to define the size and color for the dots generate in ellipse. Also define the color of the ellipse
dot_size = 100
blue_color = 'blue'
yellow_color = 'orange'
black_color = 'black'

#Define file path
QUESTIONS_FILE = "questions.json"
RESPONSES_FILE = "responses.json"

#Adding the button to coding, made the chose of answer been clicked with "left" or "right" bottum instead of typing in words
event_info = {
    'type': '',
    'description': '',
    'time': -1
}

def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):   
    
    """
    Wait for a user event to occur within a time interval
    
    Parameters:
       - timeout (float): Maximum waiting time for event.
       - interval (float): Time interval between checks for occurrence. 
       - max_rate (int): Maximum number of processing operations.
       - allow_interupt (bool): If True, the function return early if an event is detected.
    Returns:
       - dict: Updated of `event_info` dictionary containing details of the event that occurred.
    """
    start_wait = time.time()

    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:

            # end loop if we have waited more than the timeout period
            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False
                
            # end loop if event has occured
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                
            time.sleep(interval)
    
    return event_info

# this function lets buttons register events when clicked
def register_event(btn):
    
    """
    display button description in output area
    
    Parameters:
       - btn (widgets.Button): generate left and right button
    Returns:
        None
    """
    
    event_info['type'] = "click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return
    
btn1 = widgets.Button(description="Left")
btn2 = widgets.Button(description="Right")

btn1.on_click(register_event) 
btn2.on_click(register_event) 

#Send the user's answer to google form for later data analysis
def send_to_google_form(data_dict, form_url):
    
    """
    Send response to Google form
    
    Parameters:
       - data_dict (dict): dictionary contain keys form user's id.
       - form_url (str): URL of Google Form.
    Returns:
       - bool: True if submission successful, False failed.
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

#to generate dots in ellipse
def generate_dots_in_ellipse(num_dots, width=1, height=1, center=(0,0)):
    
    """
    Generate randon number of dots in ellipse
    
    Parameters:
       - num_dots (int): The number of dots to generate within the ellipse.
       - width (float): The width of the ellipse. 
       - height (float): The height of the ellipse. 
       - center (tuple): (x, y) give central coordination of ellipse.
    Returns:
       - (np.ndarray, np.ndarray): Two arrays containing the x and y coordinates of the dots generated.
    """
    angles = np.random.rand(num_dots)*2*np.pi
    radii = np.sqrt(np.random.rand(num_dots))
    x=center[0]+(width/2)*radii*np.cos(angles)
    y = center[1]+(height/2)*radii*np.sin(angles)
    return x,y

#to generate dots in circle
def generate_dots_in_circle(num_dots):
    
    """
    Generate dots within a circle that radius is 0.5
    
    Parameters:
       - num_dots (int): Number of dots generated within circle.
    Returns:
       - (np.ndarray, np.ndarray): Two arrays containing the x and y coordinates of the dots generated.
    """
    angles = np.random.rand(num_dots)*2*np.pi
    radii = np.sqrt(np.random.rand(num_dots))
    x=0.5*radii*np.cos(angles)
    y=0.5*radii*np.sin(angles)
    return x,y

#make sure the dots are all displayed in two ellipse
def display_dots(num_dots_left,num_dots_right,display_time=0.75,ellipse_scale=1.5):
    
    """
    Displays two sets of dots within ellipses on a matplotlib plot.
    
    Parameters:
       - num_dots_left (int): Number of dots generated in the left ellipse.
       - num_dots_right (int): Number of dots generated in the right ellipse.
       - display_time (float): Duration in for which dots displayed before the plot is cleared.           
       - ellipse_scale (float): width and height of the size of the ellipses.
    Returns:
        None
    """
    ellipse_width = 1*ellipse_scale
    ellipse_height = 1*ellipse_scale
    fig = plt.figure(figsize=(6,3))
    #for generate the dots coordination in left ellipse
    x_left,y_left=generate_dots_in_ellipse(num_dots_left,ellipse_width,ellipse_height)
    #generate the left dots, minus given offset to achieve left coordination
    plt.scatter(x_left-0.75*ellipse_scale,y_left,s=dot_size,c=blue_color)
    #for generate the gots coordination in right ellipse
    x_right,y_right= generate_dots_in_ellipse(num_dots_right,ellipse_width,ellipse_height)
    plt.scatter(x_right+0.75*ellipse_scale,y_right,s=dot_size,c=yellow_color)
    #Ellipse used to draw the ellipse, seoerated to left and right
    ellipse_left = Ellipse((-0.75*ellipse_scale,0),ellipse_width,ellipse_height,edgecolor=black_color,facecolor='none',lw=2)
    ellipse_right = Ellipse((0.75*ellipse_scale,0),ellipse_width,ellipse_height,edgecolor=black_color,facecolor='none',lw=2)
    plt.gca().add_patch(ellipse_left)
    plt.gca().add_patch(ellipse_right)

    plt.xlim(-1.5*ellipse_scale,1.5*ellipse_scale)
    plt.ylim(-0.5*ellipse_scale,0.5*ellipse_scale)
    plt.axis('off')

    plt.show()
    # plt.close(fig)
    #pulse a time for the participants able to see the dots
    time.sleep(display_time)
    # display.clear_output(wait=True)
    #clear.output prepare for next round 
    clear_output()
    time.sleep(0.5)
    
#giving the instrucion of ANS, explaining which ability we test in this test
def instruction_ANS_test():
    
    """ 
    Display instructions for the Approximate Number System (ANS) Test, collects user response,
    and gathers basic information from the user. Including: gender, anonymized ID, and time sleep
    last night.
    
    Parameters:
        None
        
    Returns:
        None
    """
    
    global user_id, user_gender, user_hoursleep 
    print("""This is an ANS test to test your number estimati skill. 
             Try you best to recognized which side ellipse contain more dots.
             The time will be recorded and try best to give a correct answer.
             There will be four level in this test and each test contain 10 question.
             PLEASE give some patients to the question come out then input your answer.
             Good luck and enjoy:)""")
    print("Please read:")
    print("")
    print("we wish to record your response data")
    print("to an anonymised public data repository. ")
    print("Your data will be used for educational teaching purposes")
    print("practising data analysis and visualisation.")
    print("")
    print("Please type   yes   in the box below if you consent to the upload.")
    result = input("> ")
    if result == "yes":
        print("Thanks - your data will be uploaded.")
    else:
        raise(Exception("User did not consent to continue test."))

    clear_output(wait=True)
    
#collecting the user's id  
    id_instructions = """

    Enter your anonymised ID

    To generate an anonymous 4-letter unique user identifier please enter:
    - two letters based on the initials (first and last name) of a childhood friend
    - two letters based on the initials (first and last name) of a favourite actor / actress

    e.g. if your friend was called Charlie Brown and film star was Tom Cruise
         then your unique identifier would be CBTC
    """

    print(id_instructions)
    time.sleep(3)
    user_id = input("> ")  # Now this assigns to the global variable
    clear_output(wait=True)

#collecting user's gender
    gender_instructions = """

    Enter your gender from: "m", "f", or " have not to say"

    
    """

    print(gender_instructions)
    
    time.sleep(3)
    user_gender = input("> ")
    clear_output(wait=True)
    
#collecting user's sleep hour last night
    hoursleep_instructions = """

    Enter how many hours you sleep last night 
    
    """

    print(hoursleep_instructions)
    
    time.sleep(3)
    user_hoursleep = input("> ")
    clear_output(wait=True)

#give user a sense of test start
    start_enter = """
    
    press enter to start the test
    
    """
    
    print(start_enter)
    
    time.sleep(3)
    start_enter = input(">")
    clear_output(wait=True)
    
#To generate questions and save to file for next run. This part corrected by ChatGPT
def generate_questions():
    
    """
    Generate the set question randomly but follow the dots ratio and save questions to 
    json file.
    
    Parameters:
        None
        
    Returns:
        None
    """
    possible_images = {
        1: [(12, 9), (16, 12), (15, 20)],
        2: [(18, 16), (18, 21)],
        3: [(10, 9), (20, 18), (12, 14)]
    }
    questions = {}
    for level in possible_images:
        questions[level] = []
        for image in possible_images[level]:
            questions[level].append({"num_dots_left": image[0], "num_dots_right": image[1]})
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(questions, f)
    
#Load questions from file. This part corrected by ChatGPT
def load_questions():
    
    """
    Load pre-generated question from json file.
    
    Parameters:
        None
        
    Returns:
        None
    """
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r") as f:
            questions = json.load(f)
        return questions
    else:
        return None
    
#Save result to file. This part corrected by ChatGPT.
def save_response(response):
    
    """
    Saves single response from the ANS test to a json file. If the file already exists, then new response
    is appended to the list of existing responses. If the file does not exist, it creates a file and
    initializes it with the response.
    
    Parameters:
       - response (dict): A dictionary containing the details of a single response from the ANS test. 
        
    Returns:
        None
    """
    if os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "r") as f:
            responses = json.load(f)
        responses.append(response)
    else:
        responses = [response]
    with open(RESPONSES_FILE, "w") as f:
        json.dump(responses, f)
        
#load previous results from google form to do the compare between user response to mean correct response 
def load_previous_responses():
    
    """
    Take out and calculates the mean correct response rate from a publicly available Google Sheets document.
    Function targets specific elements within the HTML structure of the Google Sheets page, relying on
    class names and tags to locate and take out the relevant data. It tailored by the structure of a
    particular Google Sheets document and may require adjustments if the document's structure changes.
    
    Parameters:
        None
    Returns:
       - float: The mean correct response rate calculated by the total number of correct responses divided
               by the total number of users.
    """
    url = "https://docs.google.com/spreadsheets/u/0/d/16FCeBKOtY31CUfJok5bZZf5wE0fXHt_OVQngGayv1Sk/htmlview"
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    num_of_users = 0
    total_correct_response = 0
    for tr in soup.find_all(name='tr'):
        th_ = tr.select('th')[0]
        td_lst = tr.select('td')
        td_lst_screened = list()
        if th_.attrs['class'][0] == 'row-headers-background':
            num_of_users += 1
            id_ = th_.attrs['id']
            if id_ != '1974098279R21' and id_ != '1974098279R50':  
                if td_lst:
                    for single_td in td_lst:
                        class_name = single_td.attrs['class']
                        if class_name[0] == 's1':
                            td_lst_screened.append(single_td)
                if td_lst_screened:
                    correct_response = td_lst_screened[3].string
                    total_correct_response += int(correct_response)

            else:
                if td_lst:
                    for single_td in td_lst:
                        class_name = single_td.attrs['class']
                        if class_name[0] == 's1':
                            td_lst_screened.append(single_td)
                if td_lst_screened:
                    correct_response = td_lst_screened[4].string
                    total_correct_response += int(correct_response)
    mean_correctness = total_correct_response / num_of_users
    
    return mean_correctness
    
    
#run the whole ANS test which dividd in to three level with progressing dots ratio generated
def run_ANS_test(num_trials_per_level=16): 
    
    """
    Conducts the ANS test across 3 levels of difficulty, tracking the participant's response times and correctness. 
    Upon initiation, the function loads or generates a set of questions for the test. It then proceeds through
    the levels of difficulty, presenting each question to the participant and collecting their responses.
    Numbers of correction are compared to the gain score number, which is different in each level, to calculate final score.
    Also, the user's correct response will compare with mean correctness number.
    
    Parameters:
        - num_trials_per_level (int): The number of trials (questions) to run for each level of difficulty. In this case is 16.
    Returns:
        None
    """
    questions = load_questions()
    if questions is None:
        generate_questions()
        questions = load_questions()
        
    global user_id, user_gender, user_hoursleep
    np.random.seed(1)
    
    responses = []
    answers = []
    correct_answers = []
    
    # Track total time
    total_time = 0 
    correct_responses = 0
    level = 1
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfjd12tCic-30j2tahCDBnKLg1H2BogrJluGV9dEZAOHrAlMQ/viewform?usp=sf_link"

    # Define the possible ratios and corresponding images for each level
    ratios_by_level = {
        1: 5,
        2: 4,
        3: 3
    }

    possible_images = {
        1: [(12, 9), (16, 12), (15, 20)],
        2: [(18, 16), (18, 21)],
        3: [(10, 9), (20, 18), (12, 14)]
    }

    level = 1
    correct_responses = 0
    total_score = 0
    total_correct_responses = 0
    
    # Load previously collected responses from the Google Form
    previous_responses = load_previous_responses()
    
    while level <= 3: 
        print(f'Level {level}')
        for i in range(num_trials_per_level):
            try:
                # Randomly choose an image for the selected ratio
                num_dots_left, num_dots_right = possible_images[level][np.random.randint(0, len(possible_images[level]))]
                
                # Start timing for this question
                start_time = time.time()  
                display_dots(num_dots_left, num_dots_right)
                display_time = time.time() - start_time 
                total_time += display_time
                panel = widgets.HBox([btn1, btn2])
                display(panel)
                wait_for_event()
                answer = event_info["description"]
                answers.append(answer)
                
                correct_answer = 'Left' if num_dots_left > num_dots_right else 'Right'
                
                # Store the correct answer for each question
                correct_answers.append(correct_answer)

                if answer == correct_answer:
                    correct_responses += 1

                responses.append({
                    'level': level,
                    'trial': i + 1,
                    'num_left': num_dots_left,
                    'num_right': num_dots_right,
                    'user_answer': answer,
                    'correct': answer == correct_answer,
                    "correct_responses":correct_responses
                })

                time.sleep(1)
                clear_output(wait=True)
                time.sleep(1)

            except Exception as e:
                print(f"Error occurred in round {i + 1}: {e}")
                break
                
        if responses != []:
            if correct_responses >= ratios_by_level[level]:
                print(f"Level {level} completed. You answered correctly {correct_responses} out of {num_trials_per_level} times.")
                total_correct_responses += responses[-1]["correct_responses"]
                correct_responses = 0  
                level += 1
                total_score += 1
                print(f"total score : {total_score}")
                print(f"total_correct_responses : {total_correct_responses}")
                time.sleep(5)
                clear_output()
            else:
                print(f"Stay in Level {level} as the required correct responses haven't been achieved.")
                total_correct_responses += responses[-1]["correct_responses"]
                correct_responses = 0  
                level += 1
                print(f"total_correct_responses : {total_correct_responses}")
                print(f"total score : {total_score}")
                time.sleep(5)
                clear_output()

    # Calculate mean correctness from previous responses
    if previous_responses:
        mean_correctness = previous_responses
    else:
        mean_correctness = None
    
    # Display correct answers for each question
    print("Correct Answers:")
    for idx, answer in enumerate(correct_answers, start=1):
        print(f"Question {idx}: {answer}")
    print("\n")
    mean_correctness = round(mean_correctness)
    if mean_correctness > total_correct_responses:
        # Print out the results of the test
        print(f"""  Well done! The test completed. 
                    Total time taken: {total_time} seconds. 
                    Total score you got: {total_score}.
                    Total correct response you got: {total_correct_responses}.
                    Mean correctness based on previous responses: {mean_correctness}
                    Mean correctness is {mean_correctness-total_correct_responses} more than total correct responses you got.
                    """)
    elif mean_correctness == total_correct_responses:
        print(f"""  Well done! The test completed. 
                    Total time taken: {total_time} seconds. 
                    Total score you got: {total_score}.
                    Total correct response you got: {total_correct_responses}.
                    Mean correctness based on previous responses: {mean_correctness}
                    Mean correctness is equal to total correct response you got.
                    """)
    else:
        print(f"""  Well done! The test completed. 
                    Total time taken: {total_time} seconds. 
                    Total score you got: {total_score}.
                    Total correct response you got: {total_correct_responses}.
                    Mean correctness based on previous responses: {mean_correctness}.
                    Total correct responses you got is {total_correct_responses-mean_correctness} more than mean correctness.
                    """)
        
                
    data_dict = {
        "User id" : user_id,
        "Score" : total_score, 
        "Total time" : total_time,
        "Correct response" : total_correct_responses,
        "Mean correctness": mean_correctness,
        "gender" : user_gender,
        "Time sleep" : user_hoursleep,
        "user response" : answers,
        "Correct": correct_answers
    }
                
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfjd12tCic-30j2tahCDBnKLg1H2BogrJluGV9dEZAOHrAlMQ/viewform?usp=sf_link"
    send_to_google_form(data_dict, form_url)


if __name__ == "__main__":    
    instruction = instruction_ANS_test()
    test_responses = run_ANS_test()
    print(instruction)
    print(test_responses)