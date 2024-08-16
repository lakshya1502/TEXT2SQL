from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from deep_translator import GoogleTranslator
from googletrans import Translator

# Load all the environment variables
load_dotenv()

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide queries as a response
def get_gemini_response(question, prompt):
    try:
        # Generating the response from the model
        response = genai.generate_text(prompt=f"{prompt}\nQuestion: {question}")
        
        # Accessing the text from the first candidate
        if response.candidates:
            return response.candidates[0]['output'].strip()
        else:
            return "No response generated."
    except Exception as e:
        return f"Error in generating response: {str(e)}"

# Function to retrieve query from the database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except sqlite3.Error as e:
        return [f"Database error: {str(e)}"]

# Define Your Prompt
prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.

For example,
Example 1 - How many entries of records are present? 
    SQL: SELECT COUNT(*) FROM STUDENT;
Example 2 - Tell me all the students studying in Data Science class? 
    SQL: SELECT * FROM STUDENT WHERE CLASS="Data Science";
"""

# Streamlit App
# Set the page configuration with a custom title and layout
st.set_page_config(page_title="Gemini SQL Query App", page_icon=":gemini:", layout="wide")

# Add a stylish header with a custom font and color
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>Gemini App To Retrieve SQL Data</h1>", unsafe_allow_html=True)

# Add a subheader with a description
st.markdown("<p style='text-align: center; color: #6A737D;'>Easily retrieve and execute any SQL query in seconds.</p>", unsafe_allow_html=True)

# Create an input text box for the SQL query
question = st.text_input(
    label="Type your SQL query below:",
    key="input",
    placeholder="Enter your  query here...",
    label_visibility="collapsed"
)

# Add a submit button with a custom style
submit = st.button(
    "Run SQL Query",
    key="submit",
    help="Click to execute your SQL query.",
    use_container_width=True,
    type="primary"
)

# Add an empty line for spacing
st.markdown("<br>", unsafe_allow_html=True)

# Add a footer or additional notes
st.markdown(
    """
    <hr>
    <p style='text-align: center; color: #6A737D; font-size: 0.9em;'></p>
    """,
    unsafe_allow_html=True
)

# If submit is clicked
if submit:
    try:
        translator = Translator()
        
        # Detect the language of the input question
        detected_lang = translator.detect(question).lang
        
        # If the detected language is not English, translate it to English
        if detected_lang != 'en':
            question = GoogleTranslator(source='auto', target='en').translate(question)

        response = get_gemini_response(question, prompt)

        if "Error" not in response:
            sql_result = read_sql_query(response, "student.db")
        else:
            sql_result = [response]

        # Translate the response back to the original language if necessary
        if detected_lang != 'en':
            sql_result = [GoogleTranslator(source='en', target=detected_lang).translate(str(row)) for row in sql_result]

        st.subheader("The Response is")
        for row in sql_result:
            st.write(row)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
