import streamlit as st
import pandas as pd
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os
import traceback
from dotenv import load_dotenv

# --- Configuration ---
st.set_page_config(layout="wide", page_title="Gemini CSV Visualizer")
st.title("📊 Visualize your CSV with Gemini")

# Load API Key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Gemini Model Configuration ---
try:
    if not GEMINI_API_KEY:
        st.error("🔴 Error: GEMINI_API_KEY not found. Please set it in your .env file.")
        st.stop()

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    st.sidebar.success("✅ Gemini API Key Configured")

except Exception as e:
    st.error(f"🔴 Error configuring Gemini API: {e}")
    st.stop()

# --- Helper Function to Generate Code ---
def generate_visualization_code(user_prompt, dataframe):
    """Sends prompt to Gemini, returns generated Python code string or None."""
    if dataframe is None:
        st.warning("⚠️ Please upload a CSV file first.")
        return None

    columns_info = "\n".join([f"- '{col}' (dtype: {dtype})" for col, dtype in dataframe.dtypes.items()])
    data_head_string = dataframe.head().to_string()

    system_instruction = """
        You are a data visualization expert specializing in Python's matplotlib and seaborn libraries. Your task is to generate precise, efficient visualization code.

        CONTEXT:
        - Working with a pandas DataFrame named `df`
        - Using pre-imported libraries: pandas (pd), matplotlib.pyplot (plt), seaborn (sns)
        - A matplotlib axis object `ax` is already created

        REQUIREMENTS:
        1. Plot Customization:
        - Always set appropriate labels for axes using `ax.set_xlabel()` and `ax.set_ylabel()`
        - Include a descriptive title using `ax.set_title()`
        - For numeric data, consider adding grid lines using `ax.grid(True, alpha=0.3)`
        - Use appropriate color palettes (prefer colorblind-friendly options)

        2. Data Handling:
        - Handle missing values appropriately (drop or fill)
        - For large datasets, consider using sample or aggregation
        - Check and handle data types correctly

        3. Plot Type Selection:
        - For categorical vs numeric: prefer boxplots, violin plots, or bar plots
        - For numeric vs numeric: prefer scatter plots with regression lines
        - For distributions: prefer KDE plots or histograms with density curves
        - For time series: use line plots with proper date formatting

        4. Code Style:
        - Use only `ax` for plotting (e.g., `ax.plot()`, `sns.scatterplot(ax=ax)`)
        - Set figure style using `sns.set_style('whitegrid')`
        - Use readable font sizes (minimum 10pt)

        FORBIDDEN:
        - No import statements
        - No DataFrame creation
        - No plt.show()
        - No comments or markdown
        - No print statements

        OUTPUT:
        Return ONLY the executable Python code, nothing else.
        """

    prompt = f"""
        Available Data Information:
        1. DataFrame Shape: {dataframe.shape}
        2. Columns and Types:
        {columns_info}
        3. Sample Data:
        {data_head_string}
        4. Numeric Columns: {', '.join(dataframe.select_dtypes(include=['int64', 'float64']).columns)}
        5. Categorical Columns: {', '.join(dataframe.select_dtypes(include=['object', 'category']).columns)}

        User Request: {user_prompt}

        Generate visualization code that best addresses this request while following all system requirements.
        """
    try:
        response = model.generate_content(
            [system_instruction, prompt],
            generation_config=genai.types.GenerationConfig(temperature=0)
        )
        generated_code = response.text.strip()

        if generated_code.startswith("```python"):
            generated_code = generated_code[len("```python"):].strip()
        if generated_code.endswith("```"):
            generated_code = generated_code[:-len("```")].strip()

        return generated_code

    except Exception as e:
        st.error(f"🔴 Gemini API Error: {e}")
        return None

# --- Streamlit UI Elements ---

# 1. File Uploader
st.sidebar.header("1. Upload CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Initialize session state for dataframe
if 'df' not in st.session_state:
    st.session_state.df = None

if uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()
        st.session_state.df = pd.read_csv(io.BytesIO(bytes_data))
        st.sidebar.success(f"✅ Loaded '{uploaded_file.name}'")
    except Exception as e:
        st.sidebar.error(f"🔴 Error reading CSV: {e}")
        st.session_state.df = None
else:
    if st.session_state.df is not None:
        st.session_state.df = None

# Display DataFrame Info if loaded
if st.session_state.df is not None:
    st.header("📄 Data Preview & Info")
    # Display DataFrame head as HTML to avoid PyArrow issues
    st.markdown(st.session_state.df.head().to_html(), unsafe_allow_html=True)

    with st.expander("Show Column Names and Data Types"):
        buffer = io.StringIO()
        st.session_state.df.info(buf=buffer)
        info_output = buffer.getvalue()
        st.markdown(f"```\n{info_output}\n```")

    with st.expander("Show Basic Statistics"):
        st.markdown(st.session_state.df.describe(include='all').to_html(), unsafe_allow_html=True)

    st.divider()

    # 2. User Prompt Input
    st.header("💬 Describe the Plot You Want")
    prompt_request = st.text_area("Example: Create a histogram of the 'Age' column", height=100,
                                  placeholder="Enter your plot description here...")

    # 3. Generate & Display Button
    if st.button("✨ Generate & Display Plot", type="primary"):
        if not prompt_request:
            st.warning("⚠️ Please enter a description for the plot.")
        else:
            df = st.session_state.df
            with st.spinner("🧠 Asking Gemini to generate code..."):
                generated_code = generate_visualization_code(prompt_request, df)

            if generated_code:
                st.subheader("🐍 Generated Code by Gemini:")
                st.code(generated_code, language="python")

                st.subheader("📊 Executed Plot:")
                try:
                    print(df.head())
                    exec_globals = {'pd': pd, 'plt': plt, 'sns': sns, 'df': df}
                    fig, ax = plt.subplots()
                    exec_globals['ax'] = ax
                    exec(generated_code, exec_globals)
                    print(fig)
                    st.pyplot(fig)
                    plt.close(fig)
                except Exception as e:
                    st.error(f"🔴 Error executing generated code:")
                    st.code(generated_code, language="python")
                    st.code(traceback.format_exc())
            else:
                if prompt_request:
                    st.error("🔴 Failed to generate code. Check Gemini API status or your prompt.")
else:
    st.info("☝️ Upload a CSV file using the sidebar to get started.")

# --- Footer/Info ---
st.sidebar.markdown("---")
st.sidebar.markdown("Built with Streamlit & Gemini")
