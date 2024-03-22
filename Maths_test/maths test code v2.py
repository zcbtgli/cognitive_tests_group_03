from IPython.display import display, Image, clear_output, HTML
from jupyter_ui_poll import ui_events
from bs4 import BeautifulSoup
import time
import numpy as np
import requests
import json
import ipywidgets as widgets
import pandas as pd
    
def buttons():
    """
    This function generates the 3 panels of buttons required throughout the test.

    Returns:
    gender_panel= The set of buttons that contain the genders the user can identify as.
    next_panel= It only contains the continue button so the user can proceed to the next section of the test, as well as giving them a short pause if required.
    end_panel= It offers the user a choice to pick whether to have their data saved in the Google Form.
    button_messages= A list that contains all the text in all the buttons.
    """

    button_messages= ["Yes", "No", "Continue", "Male", "Female", "Non-binary", "Prefer not to say"]
    btn1= widgets.Button(description= button_messages[0], style= {"button_color": "green"})
    btn2= widgets.Button(description= button_messages[1], style= {"button_color": "red"})
    btn3= widgets.Button(description= button_messages[2])
    btn4= widgets.Button(description= button_messages[3])
    btn5= widgets.Button(description= button_messages[4])
    btn6= widgets.Button(description= button_messages[5])
    btn7= widgets.Button(description= button_messages[6])
    btn1.on_click(register_btn_event) 
    btn2.on_click(register_btn_event)
    btn3.on_click(register_btn_event)
    btn4.on_click(register_btn_event) 
    btn5.on_click(register_btn_event)
    btn6.on_click(register_btn_event)
    btn7.on_click(register_btn_event)
    next_panel= widgets.HBox([btn3]) # 3 sets of buttons.
    end_panel= widgets.HBox([btn1, btn2])
    gender_panel= widgets.HBox([btn4, btn5, btn6, btn7])
    
    return gender_panel, next_panel, end_panel, button_messages # Now they can be used in other functions.
    
event_info = {'type': '',
              'description': '',
              'time': -1}

def wait_for_event(interval=0.001, max_rate=20, allow_interupt=True): # I removed timeout because I didn't think it was helpful.

    start_wait = time.time()
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1
    n_proc = int(max_rate*interval)+1

    with ui_events() as ui_poll:
        keep_looping = True
    
        while keep_looping==True:
            ui_poll(n_proc)
            
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
            
            time.sleep(interval)

    return event_info
    
def register_btn_event(btn):

    event_info['type'] = "button click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    
    return

def register_text_input_event(text_input):
    
    event_info['type'] = "text_entry"
    event_info['description'] = text_input.value
    event_info['time'] = time.time()
    
    return

def text_input(prompt=None):
    
    text_input = widgets.Text(description=prompt, style= {'description_width': 'initial'})
    
    import warnings    
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    text_input.on_submit(register_text_input_event)
    display(text_input)
    event = wait_for_event()
    text_input.disabled = True
    
    return event['description']
    
def send_to_google_form(data_dict, form_url):

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
    
def messages(correct_answers, level_number, final_score, average_correct_time, average_time, name, style, user_id, gender, sleep, ia_json): # These variables get changed many times throughout messages() and maths_ability_test(), and so here I make sure they can be used in messages().
    """
    This function can be split into two halves: displaying text at the start and at the end of the test. At the start of the test, some user information is also collected, such as their name, user_id, gender and sleep, for data analysis.
    
    Arguments
    correct_answers: Defined in the main function. Depending on how many questions the user gets right, different messages are displayed at the end of the test.
    level_number: Also defined in the main function. This determines which set of messages are displayed. If level_number== 0, start_messages are displayed, if it is 3, end_messages are displayed instead.
    final_score, average_correct_time, ia_json, average_time: These are all test results collected from the main function and are sent to the Google Form through this function.
    name, user_id, gender, sleep: These are the user's personal information that are collected by this function when level_number== 0 and the start_messages are being printed. Since these are defined before returning back to the main function, they must be passed between the two functions.
    style: The style of the operations displayed, and is defined in the main function. Passed here because it is still needed in the main function after messages are displayed at the start of the test.

    Returns
    name, user_id, gender, sleep: The variables defined at the start of this function, before leaving the function and returning at the end of the test to be sent to the Google Form.
    """

    
    data_dict= { # Information that get sent to the Google form.
    "user_id": user_id,
    "correct_answers": correct_answers,
    "final_score": final_score,
    "average_correct_time": average_correct_time,
    "average_time": average_time,
    "gender": gender,
    "sleep": sleep,
    "ia_json": ia_json
    }
    form_url= "https://docs.google.com/forms/d/e/1FAIpQLSfXDFoeFVyEsiVTw2wqDfnQMhSFxVLy79u4hBBGUSV-aFdsaA/viewform?usp=sf_link"
    start_messages= [
        "Welcome to the Maths Ability Test!",
        "What is your name? (NOT YOUR ID)",
        "Please enter your anonymised ID.",
        "What is your gender?",
        "How many hours of sleep did you have last night?",
        "You will be shown some arithmetic questions. However, each question will be split into different parts and each part will be shown seperately for a short amount of time.",
        "Enter the answer when prompted, as fast as possible. You will be scored according to your accuracy and speed.",
        "Please DO NOT type numbers unprompted, as this would exit the code.",
        "There are 3 levels, and 5 questions in each level.",
        "3",
        "2",
        "1"
    ]   
    end_messages= [
        f"Well done, {name}!",
        f"Not bad, {name}.",
        "You should carry a calculator at all times.",
        "You did not answer any questions correctly.",
        f"You answered {correct_answers}/ 15 questions correctly, {correct_answers- 11} more than the average, 11!",
        f"You answered {correct_answers}/ 15 questions correctly, the same as the average person!",
        f"You answered {correct_answers}/ 15 questions correctly, {11- correct_answers} fewer than the average, 11.",
        f"You scored: {final_score:.1f}/ 100,{49.6- final_score: .1f} lower than the average score, 49.6.",
        f"You scored: {final_score:.1f}/ 100,{final_score- 49.6: .1f} higher than the average score, 49.6!",
        f"You scored: {final_score:.1f}/ 100, exactly the same as the average person!",
        f"You spent on average {average_correct_time:.2f}s for each question you answered correctly,{average_correct_time- 3.98: .2f}s slower than the average, 3.98s.",
        f"You spent on average {average_correct_time:.2f}s for each question you answered correctly,{3.98- average_correct_time: .2f}s faster than the average, 3.98s!",
        f"You spent on average {average_correct_time:.2f}s for each question you answered correctly, exactly the same as the average person!",
        "We wish to record your response data to an anonymised public data repository.",
        "Your data will be used for educational teaching purposes, specifically for practicing and teaching data analysis and visualisation.",
        "Please click Yes if you consent to the upload.",
        "Thanks- your data will be uploaded.",
        "Please contact a.fedorec@ucl.ac.uk if you have any questions or concerns regarding the stored results.",
        "No problem, we hope you enjoyed the test.",
        "Thank you for your time!"
    ]
    gender_panel, next_panel, end_panel, button_messages= buttons()

    if level_number== 0:

        for message in start_messages: # Rather than typing print(the message) then time.sleep(x) for every message, I placed all the messages meant to be displayed in lists, then had a for loop display it one by one.
            print(message) # Then I created an if-elif-else block as the function that follows varies between messages.
    
            if message== start_messages[1]: # Name is collected for a greeting here and a comment at the end of the test.
                name= text_input("")
                clear_output()
                print(f"Hi {name}!")
                time.sleep(2)

            elif message== start_messages[2]:
                id_instructions= """
                Enter your anonymised ID
                To generate an anonymous 4-letter unique user identifier please enter:
                -two letters based on the initials(first and last name) of a childhood friend
                -two letters based on the initials(first and last name) of a favourite actor/ actress
                e.g. if your friend was called Charlie Brown and film star was Tom Cruise
                then your unique identifier would be CBTC
                """
                print(id_instructions)
                user_id= text_input(">")
                clear_output()
                print("User entered id:", user_id)
                display(next_panel)
                event_info= wait_for_event()
                clear_output()

            elif message== start_messages[3]:
                display(gender_panel)
                event_info= wait_for_event()
                
                if event_info['description']== button_messages[3]: # Gender information is collected.
                    gender= "m"

                elif event_info['description']== button_messages[4]:           
                    gender= "f"

                elif event_info['description']== button_messages[5]:
                    gender= "non-binary"

                else:
                    gender= "Prefer not to say"
                    
                clear_output()

            elif message== start_messages[4]:
                
                while sleep== "" or type(sleep)!= float: # This block ensures that a number, rather than text is recorded. See the other try except block for more comments.
                    sleep= text_input("Enter number:")
                    
                    try:
                        sleep= float(sleep)
                        
                    except ValueError:
                        print("Please try again.")
                        
                clear_output()
                        
            elif message== start_messages[5]:
                time.sleep(4)
        
            elif message== start_messages[8]:
                time.sleep(2)
                display(next_panel)
                event_info= wait_for_event()
                clear_output()
                print(f"Good luck, {name}!")
                time.sleep(2)
        
            elif message== "3" or "2" or "1":
                time.sleep(1)
        
            else:
                time.sleep(2)

    elif level_number== 3: # message() only runs this part at the end of the test.

        if correct_answers>= 1: # This if block is important because if none of the questions are answered correctly, final_score and average_correct_time will not be printed, and not a single time_taken has been recorded.
    
            if correct_answers>= 12: # Different number of correct_answers gets a different comment.
                print(end_messages[0])
                time.sleep(2)
                print(end_messages[4])
    
            elif correct_answers>= 8:
                print(end_messages[1])
                time.sleep(2)
                
                if correct_answers== 11:
                    print(end_messages[5])
                    
                elif correct_answers<= 10:
                    print(end_messages[6])
    
            else:
                print(end_messages[2])
                time.sleep(2)
                print(end_messages[6])

            time.sleep(2)
            
            if float(f"{final_score: .1f}")< 49.6: # User results are compared to those of the collected data. Means are calculated within Google Sheets and copied here.
                print(end_messages[7])
                
            elif float(f"{final_score: .1f}")> 49.6:
                print(end_messages[8])
                
            else:
                print(end_messages[9])

            time.sleep(2)
            
            if float(f"{average_correct_time: .2f}")> 3.98:
                print(end_messages[10])
                
            elif float(f"{average_correct_time: .2f}")< 3.98:
                print(end_messages[11])
                
            else:
                print(end_messages[12])
                
        else: # See comment next to the respective if line. Different messages are printed if none of the questions are answered correctly.
            print(end_messages[3])

        display(next_panel)
        event_info= wait_for_event()
        clear_output()

        for message in end_messages[13:16]: # A slice and for loop for some different messages to be printed.
            print(message)
            time.sleep(2)

        display(end_panel)
        event_info= wait_for_event()
        clear_output()
    
        if event_info['description']== button_messages[0]: # Consent for data collection is requested.
            print(end_messages[16], end_messages[17])
            send_to_google_form(data_dict, form_url)

        else:           
            print(end_messages[18])

        time.sleep(2)
        print(end_messages[-1])

    return name, user_id, gender, sleep # This ensures that the hours slept, gender, name and username that were input would be saved.
        
def maths_ability_test():

    """
    The main function. It executes the test and collects the user's perfomance data. In order to keep it argument-free, many variables are defined with no value, before being changed within the function, or passed to messages(). There aren't any returns either, since the last line runs the second half of messages() with all variables passsed to it.
    """
    level_1= np.array([[9, "x9", -4], # A question is laid out in a row of each matrix. Each matrix is a level.
                       [4, "x2", "x5"],
                       [8, "+9", -4],
                       [1, "x8", "+9"],
                       [4, -2, -3]])
    level_2= np.array([[12, -3, "x12"],
                       [10, "+5", "x13"],
                       [5, "x6", "x11"],
                       [7, "+13", "x12"],
                       [8, "+1", "x15"]])
    level_3= np.array([[4, "x14", "÷8"],
                       [18, "x18", "÷4"],
                       [132, "÷11", -20],
                       [196, "÷7", "+20"],
                       [144, "+18", "÷9"]])
    all_levels= [level_1, level_2, level_3]
    lvl1_answers= [77, 40, 13, 17, -1]
    lvl2_answers= [108, 195, 330, 240, 135]
    lvl3_answers= [7, 81, -8, 48, 18]
    all_answers= [lvl1_answers, lvl2_answers, lvl3_answers]
    row_number= 0
    level_number= 0
    correct_answers= 0
    final_score= 0
    average_correct_time= 0
    average_time= 0
    all_scores= []
    all_times= []
    all_correct_times= []
    name= ""
    style= f"font-size: 50px;"
    user_id= ""
    gender= ""
    sleep= ""
    individual_answers= []
    ia_json= ""
    gender_panel, next_panel, end_panel, button_messages= buttons() # This allows buttons to be used in this function.
    name, user_id, gender, sleep= messages(correct_answers, level_number, final_score, average_correct_time, average_time, name, style, user_id, gender, sleep, ia_json) # Introduction to the test, some user info is collected.

    for level in all_levels: # This for loop repeats itself after a level is completed.
    
        for row in level: # This for loop repeats itself after a question is completed.
            clear_output()
    
            for operation in row: # This for loop displays an element of a level matrix and repeats until all elements of the row have been printed.
                number_out= HTML(f"<span style='{style}'>{operation}</span>")
                display(number_out)
                time.sleep(2)
                clear_output(wait= False)   
    
            start_time= time.time() # Time starts when the whole question has been printed and an input box is created.
            ans= text_input("Enter answer:")

            try: # I had to look this up- try and except are to ensure that if output were something other than numbers, the code still runs.
            
                if ans== "stop": # This is just for me to stop the code prematurely if I encounter any issues when writing and running the code.
                    print("Maths Ability Test stopped.")
                    return
        
                elif int(ans)== all_answers[level_number][row_number]: # This condition runs if the input matches with the component (row_number) of the answer list. Each answer list is placed in another list called all_answers for identification.
                    end_time= time.time()
                    time_taken= end_time- start_time # Timer is only stopped, and the time recorded, when the question is answered correctly. This is because of the scoring system, which takes into account of both accuracy and speed.
                    correct_answers= correct_answers+ 1 # Total number of questions answered correctly will be displayed at the end.
                    all_correct_times.append(time_taken) # All the times taken to answer correctly are added to a list, as the average time taken for each correct answer will be displayed at the end as well.
                    individual_answers.append(1) # If answered correctly, the question is assigned a value of 1 in order to keep track of correct and wrong answers in Google Forms.
                    print("Correct!")
                    print(f"You took {time_taken:.2f} seconds.")
                
                    for i in range(10): # This is the scoring system.
            
                        if time_taken>= 8.2: # If they take more than 8.2s to answer the question correctly, they score 5/ 100 regardless of how much time is taken.
                            score= 5
                            break
            
                        elif time_taken<= 1: # If they take less than a second to answer the question correctly, they score 100/ 100.
                            score= 100
                            break
            
                        elif time_taken>= 0.8*i+ 1: # This is the case for if they take between 1s and 8.2s. For every additional 0.8s from 1s they take, 10 points are deducted, e.g. 1-1.79s scores 90, 1.8-2.59s scores 80. The for loop is to ensure that the correct score is given when time_taken is between 1 and 8.2s.
                            score= 100- 10*(i+ 1)
            
                        else: # This is crucial. When a score is established from the elif block immediately above, the for loop is repeated once again. Now none of the other if and elif blocks return true, and so this else block provides a way out with the correct score.
                            break
        
                else:
                    end_time= time.time()
                    time_taken= end_time- start_time
                    print("Incorrect")
                    individual_answers.append(0) # If answered incorrectly, the question is assigned a value of 0.
                    score= 0
            
            except ValueError: # See the comment in the try row.
                end_time= time.time()
                time_taken= end_time- start_time
                print("Incorrect")
                individual_answers.append(0)
                score= 0
        
            display(next_panel)
            event_info= wait_for_event()
            row_number= row_number+ 1 # This moves on to the next question of the level.
            all_scores.append(score) # Like time_taken, all scores are placed in a list.
            all_times.append(time_taken) # This list is used to collect the time taken for each question, regardless of whether it is answered correctly or not, for data analysis.
            clear_output()
        
        level_number= level_number+ 1 # This changes the level counter when a level is completed.
        row_number= 0 # This ensures that the next output would be the question 1 of the next level, after a level is completed.

        if level_number<= len(all_levels)- 1: # The level counter from 2 lines above serves its purpose here. After levels 1 and 2, this if block would run to print 'Level x'. After Level 3, this if statement would return false, so 'Level 4', which does not exist, isn't printed.
            print(f"Level {level_number+ 1}") # +1 because I defined level_number, near the top of the code, as 0.
            time.sleep(2)
            display(next_panel)
            event_info= wait_for_event()
            
    clear_output()
    final_score= sum(all_scores)/ (len(all_scores)) # Here the scores and times are averaged.
    average_time= sum(all_times)/ (len(all_times))
    
    if (len(all_correct_times))== 0: # If every answer was incorrect, there would be no times in all_correct_times, and a division by zero error will appear, hence this line is required.
        average_correct_time= 0
    else:
        average_correct_time= sum(all_correct_times)/ (len(all_correct_times))
        
    ia_dataframe= pd.DataFrame(individual_answers, columns= ["correct_answer"]) # The outcome of each reply is placed in a dataframe then converted to a different format to be sent to the Google Form.
    ia_json= ia_dataframe.to_json()
    messages(correct_answers, level_number, final_score, average_correct_time, average_time, name, style, user_id, gender, sleep, ia_json) # messages() is run again to display end_messages.
    
if __name__ == "__main__":
    maths_ability_test()