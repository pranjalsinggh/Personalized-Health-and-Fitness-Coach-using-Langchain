import streamlit as st
import os, warnings, time, random
warnings.filterwarnings("ignore")
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain, LLMRouterChain
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.chains.router import MultiPromptChain
from dotenv import load_dotenv

load_dotenv()

# Load OpenAI LLM
if "OPENAI_API_KEY" in st.secrets['secrets']:
    api_key = st.secrets['secrets']['OPENAI_API_KEY']
else:
    api_key = os.environ.get('OPENAI_API_KEY')

# Initialize a ChatOpenAI model
llm = ChatOpenAI(api_key=api_key)

# Define the prompt templates
mental_wellness_template = """
    You are a mental wellness coach. Provide guidance on stress management, mindfulness, and mental health techniques based on the user's query. 
    Here's the user's query: {input}
"""

supplement_guidance_template = """
    You are a certified nutritionist. Provide expert advice on supplements and nutritional intake based on the user's query.
    Here's the user's query: {input}
"""

injury_recovery_template = """
    You are a sports therapist. Provide recovery techniques, injury prevention tips, and rehabilitation exercises based on the user's query.
    Here's the user's query: {input}
"""

sleep_recovery_template = """
    You are a sleep specialist and recovery coach. Provide insights on improving sleep and optimizing recovery for fitness performance based on the user's query.
    Here's the user's query: {input}
"""

lifestyle_coaching_template = """
    You are a lifestyle coach. Provide actionable steps to build sustainable fitness habits based on the user's query.
    Here's the user's query: {input}
"""

meal_prep_template = """
    You are a meal-planning expert. Provide a budget-friendly and time-efficient meal prep strategy based on the user's dietary preference and goal.
    Here's the user's query: {input}
"""

food_substitutions_template = """
    You are a dietary expert. Suggest healthy alternatives for foods that align with the user's dietary preference and goal.
    Here's the user's query: {input}
"""

hydration_template = """
    You are a hydration specialist. Provide recommendations on daily water intake and electrolyte balance for optimal health based on the user's goal and activity level.
    Here's the user's query: {input}
"""

meal_timing_template = """
    You are a fitness nutritionist. Provide optimal meal timing strategies based on the user's goal and dietary preferences, including guidance on intermittent fasting if applicable.
    Here's the user's query: {input}
"""

exercise_plan_template = """
    You are a certified fitness expert. Create a personalized exercise plan tailored to the user's fitness level, goal, and preferences.
    
    Consider the following when designing the plan:
    - Workout frequency (days per week)
    - Exercise types (strength training, cardio, flexibility, etc.)
    - Intensity level (beginner, intermediate, advanced)
    - Duration of each session
    - Recovery and rest recommendations
    
    Here's the user's query: {input}
"""

prompt_info = [
    {
        "name": "mental wellness",
        "description": "Provide guidance on stress management, mindfulness, and mental health techniques based on the user's query.",
        "template": mental_wellness_template
    },
    {
        "name": "supplement guidance",
        "description": "Provide expert advice on supplements and nutritional intake based on the user's query.",
        "template": supplement_guidance_template
    },
    {
        "name": "injury recovery",
        "description": "Provide recovery techniques, injury prevention tips, and rehabilitation exercises based on the user's query.",
        "template": injury_recovery_template
    },
    {
        "name": "sleep recovery",
        "description": "Provide insights on improving sleep and optimizing recovery for fitness performance based on the user's query.",
        "template": sleep_recovery_template
    },
    {
        "name": "lifestyle coaching",
        "description": "Provide actionable steps to build sustainable fitness habits based on the user's query.",
        "template": lifestyle_coaching_template
    },
    {
        "name": "meal prep",
        "description": "Provide a budget-friendly and time-efficient meal prep strategy based on the user's dietary preference and goal.",
        "template": meal_prep_template
    },
    {
        "name": "food substitutions",
        "description": "Suggest healthy alternatives for foods that align with the user's dietary preference and goal.",
        "template": food_substitutions_template
    },
    {
        "name": "hydration",
        "description": "Provide recommendations on daily water intake and electrolyte balance for optimal health based on the user's goal and activity level.",
        "template": hydration_template
    },
    {
        "name": "meal timing",
        "description": "Provide optimal meal timing strategies based on the user's goal and dietary preferences, including guidance on intermittent fasting if applicable.",
        "template": meal_timing_template
    },
    {
        "name": "exercise plan",
        "description": "Create a personalized exercise plan tailored to the user's fitness level, goal, and preferences.",
        "template": exercise_plan_template
    }
]

destinations_chain = {}

for p_info in prompt_info:
    name = p_info['name']
    template = p_info['template']
    prompt = ChatPromptTemplate.from_template(template)
    chain = LLMChain(llm=llm,prompt=prompt)
    destinations_chain[name] = chain

default_template = "{input}"
default_prompt = ChatPromptTemplate.from_template(default_template)
default_chain = LLMChain(llm=llm, prompt=default_prompt)

destinations = "\n".join([f"{p_info['name']}: {p_info['description']}" for p_info in prompt_info])

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations)

router_prompt = PromptTemplate(template=router_template,
                               input_variables=['input'],
                               output_parser=RouterOutputParser())

router_chain = LLMRouterChain.from_llm(llm=llm, prompt=router_prompt)

chain = MultiPromptChain(router_chain=router_chain,
                                      destination_chains=destinations_chain,
                                      default_chain=default_chain,
                                      verbose=True)

# Streamlit Page Configuration
st.set_page_config(page_title="Personalized AI Health, Fitness, and Wellness Coach", page_icon="🏋️", layout="wide")

# Custom CSS for UI Styling
st.markdown("""
    <style>
        .big-font { font-size: 22px !important; }
        .stButton>button { width: 100%; }
        .stProgress > div > div > div { background-color: #FF5722; }
        .stTextInput>div>div>input { font-size: 18px; padding: 10px; }
        .stMarkdown { text-align: center; font-size: 20px; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>🏋️ Personalized AI Health, Fitness, and Wellness Coach</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Get expert-backed fitness, nutrition, and wellness insights!</h3>", unsafe_allow_html=True)

# User Input
st.markdown("<h2 style='text-align: center;'>🔍 Enter your question:</h2>", unsafe_allow_html=True)
query = st.text_area(label=' ',value="",placeholder="E.g., Best diet plan for weight loss?", height=100, key="user_query")

if st.button("🚀 Get Insights"):
    if query.strip():
        with st.spinner("⏳ Generating insights..."):
            time.sleep(random.uniform(1.5,3.0)) # Simulate processing time
            response = chain.run(query)

        # Animated Progress Bar
        progress_bar = st.progress(0)

        for percent_complete in range(1,101):
            time.sleep(0.01)
            progress_bar.progress(percent_complete)

        # Display AI Response
        st.success("✅ Insights Generated!")
        st.markdown(f"<div class='big-font'>💡 Insights: </div>", unsafe_allow_html=True)
        st.write(response)

        # Initialize session state for feedback if not present
        if 'upvote_count' not in st.session_state:
            st.session_state.upvote_count = 0
        if 'downvote_count' not in st.session_state:
            st.session_state.downvote_count = 0
        
        # Interactive Upvote / Downvote
        upvote_button = st.button("👍 Upvote")
        downvote_button = st.button("👎 Downvote")

        # Handle Upvote / Downvote logic
        if upvote_button:
            st.session_state.upvote_count += 1
            st.success(f"Thanks for your feedback! 😊")

        if downvote_button:
            st.session_state.downvote_count += 1
            st.warning(f"We'll work on improving responses! 🛠️")

    else:
        st.warning("⚠️ Please enter a query before generating insights!")

# Sidebar - About Section with Enhanced Styling
st.sidebar.markdown("""
    <div style="background-color:#f1f1f1; padding:15px; border-radius:10px;"> 
        <h2 style="color:#333333; text-align:center;">ℹ️ About This App</h2>
        <p style="color:#333333; font-size:16px; text-align:center;">
            This <b>AI-powered Personalized Health Coach</b> provides tailored insights on 
            <b>fitness, nutrition, and wellness</b>.  
            Simply enter your query to receive <b>expert-backed</b>, actionable guidance 
            for a <b>healthier lifestyle!</b>
        </p>
    </div>
""", unsafe_allow_html=True)

# Clear the cache on every execution
st.legacy_caching.clear_cache()