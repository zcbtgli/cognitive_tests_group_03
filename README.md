# Cognitive Group 3

This is a BIOS0030 project, aiming to qualified Approximate Number Sense (ANS) by using Python coding. Two other cognitive tests also included to compare ANS with other abilities.

## Test included

1. **ANS Test**: Written by Guanzhong Li, this test is aim to investigate the suddent number estimation ability

2. **Memory Test**: Written by Bella Zhu, testing for the capacity to recall and recognize specific details about color and spatial relationships between shapes after a brief exposure period.

3. **Math Ability Test**: Written by Jan Tao, testing for the capacity to quickly perform and remember sequential calculations under time constraints, with increasing difficulty levels.

## Test Details

### ANS Test

The ANS test asks participants to identify the side with the most dots after the image blinks. Two groups of dots will be displayed for 0.75 seconds, followed by “left” and “right” buttons appearing on screens for participants to click on. There are 48 questions separated into three levels with increasing complexity since the dot ratio between the two sides in higher levels is smaller. All questions were randomized in a reproducible manner to minimize potential bias associated with question order, contributing to the fairness and reliability of the assessment outcomes. 

### Memory Test

The memory test asks participants to answer MCQs after an image is displayed for 20 seconds. To avoid distributional bias in scoring due to oversimplified questions, participants are expected to memorize a grid of multicoloured shapes. This approach encompasses both visual and spatial memorization, facilitating a comprehensive evaluation of memory ability. Additionally, this test deliberately removes the time limit to exclude the stress-induced impairment of memory ability due to time pressure. Therefore, the test length was adjusted mainly based on user feedback. Furthermore, user input is facilitated through clickable buttons to preclude data inaccuracy raised from misspellings.

### Math Ability Test

The maths test asks participants to input answers for basic calculations involving addition, subtraction, multiplication, and division. To control for the effect of memory capacity on calculation performance, each number is displayed for two seconds, with no sum of digits exceeding 7, which was indicated as the limit of memory span. The number of correct answers is collected, and faster responses will be assigned a higher score through a different metric that will not be investigated in this report. 

## Data collected

In each test, correct response done by participants and total time spend during test are recorded. Also recording some personal informations including, User id, gender, and time sleep last night. All data collected will used for educational teaching purposes practising data analysis and visualisation.

## Code Update in final version

- Adding "press 'enter' to start test" provide a prepare time for participants.
- Comment each function to explain there usage.
- Boxplot shows to compare participant's correct response with average correct response.