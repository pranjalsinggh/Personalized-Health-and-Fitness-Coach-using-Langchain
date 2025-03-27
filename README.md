# Personalized AI Health, Fitness, and Wellness Coach

This project is an AI-powered application that provides personalized health, fitness, and wellness guidance. Using OpenAI's ChatGPT, the app delivers expert-backed insights on various topics such as nutrition, exercise plans, meal prep, hydration, sleep recovery, and mental wellness. Users can input their specific queries and receive tailored advice to improve their health and fitness journey.

## Features
- **Personalized Health Coaching**: Get guidance on mental wellness, supplements, injury recovery, sleep, fitness, and lifestyle coaching.
- **Meal and Nutrition Insights**: Receive suggestions for meal prep, food substitutions, meal timing, and hydration based on your goals.
- **Interactive and Engaging UI**: A user-friendly interface built with Streamlit, allowing users to interact with the AI to generate customized insights.

## Key Components
- **OpenAI API**: The application utilizes OpenAI's GPT model for generating responses based on user input.
- **Langchain**: The app uses Langchain to route different queries to specialized models for tailored insights.
- **Multi-Prompt Chain**: Routes different queries to specific templates for mental wellness, exercise planning, nutrition advice, and more.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-health-fitness-wellness-coach.git
   cd ai-health-fitness-wellness-coach
   ```

2. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Set up your OpenAI API key:

    Create a .env file in the project root and add your OpenAI API key:

    ```bash
    OPENAI_API_KEY=your-api-key-here
    ```

4. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

## How It Works

The application utilizes a set of pre-defined templates that provide personalized advice based on the user’s query. These templates cover topics like mental wellness, fitness plans, meal prep, and more.

The MultiPromptChain in Langchain processes the query and directs it to the appropriate expert (fitness expert, nutritionist, therapist, etc.).

Responses are dynamically generated and displayed to the user, along with interactive features like upvoting and downvoting feedback.

## Technologies Used

<ul>
    <li>Streamlit: Framework for building the frontend.</li>
    <li>Langchain: For chaining and routing different prompts based on the user's query.</li>
    <li>OpenAI's ChatOpenAI: For generating AI-driven responses.</li>
    <li>Python: Backend language for the application.</li>
</ul>

## Contributions

Feel free to fork this repository and make your own contributions! You can submit issues and pull requests to help improve the project.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.