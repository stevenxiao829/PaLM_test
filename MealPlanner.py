import pprint
import streamlit as st
import google.generativeai as palm
palm.configure(api_key='AIzaSyAz-zB8gld3zLUDKOLKYE06aYwpXYgdnLY')

st.title("Meal Planner :fork_and_knife:")

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

# Dropdown options for goal, fitLevel, time, and place
goal_options = ['Weight Loss', 'Muscle Gain', 'Maintenance']
experience = ['Beginner', 'Intermediate', 'Advanced']
DietType = ['Regular', 'Vegan', 'Vegetarian', "Pescatarian", "Keto", "Paleo", "Intermittent Fasting"]
restrictions = ["None", "Gluten-Free", "Lactose Intolerance", "Other"]
physical_activity_options = ['Very Light', 'Light', 'Moderate', 'Heavy', 'Very Heavy']

time_options = list(range(1, 5))

age = st.text_input('Enter Your Age:')
height = st.text_input('Enter Your height:')
weight = st.text_input('Enter Your Weight:')

# Dropdown menus for goal, fitLevel, time, and place
goal = st.selectbox('Choose Your Goal:', goal_options)
skillLevel = st.selectbox('Choose Your Cooking Skill Level:', experience)
time = st.selectbox('Choose Your Availability (hours per day):', time_options)

# Dropdown menu for restrictions
restriction_option = restrictions + ["Other"]
restriction = st.selectbox('Choose Any Dietary Restrictions:', restriction_option)

# Text input for restrictions if "Other" is selected
if restriction == "Other":
    restriction = st.text_input("Enter Any Other Dietary Restrictions:")

# Dropdown menu for physical activity
physical_activity = st.selectbox('Choose Your Physical Activity Level:', physical_activity_options)

# Check if all inputs have been filled
if age and weight and goal and skillLevel and time:
    prompt = (
        "Pretend you are an expert nutritionist and chef. "
        "Output a detailed personalized weekly meal plan with calorie information in bullet points for someone who is "
        + str(age)
        + " years old, is " + height + "feet tall and weighs "
        + str(weight)
        + " pounds, and aims to achieve "
        + goal
        + ". They consider their cooking ability as "
        + skillLevel
        + ", and they can dedicate "
        + str(time)
        + " hours per day for meal preparation." 
        + ". Their physical activity level is "
        + physical_activity
        + "."
    )

    if restriction != "None":
        prompt += " They have the following dietary restrictions: " + restriction + "."

    # Create an empty output container
    output_container = st.empty()

    # Start generating the text
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=1000,
    )

    # Update the output container with the generated text
    output_container.text(completion.result)

else:
    st.write("Please fill in all the inputs to generate the meal plan.")
