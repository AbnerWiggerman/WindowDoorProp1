import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in Streamlit Cloud secrets

st.set_page_config(page_title="Window & Door Proposal Generator", layout="centered")

st.title("🏠 Residential Window & Door Proposal Generator")

# Customer Information
st.header("Customer Information")
customer_name = st.text_input("Customer Name")
job_details = st.text_area("Job Details")

# Window/Door Units
st.header("Window/Door Units")

if "units" not in st.session_state:
    st.session_state.units = []

# Function to add a new unit
def add_unit():
    st.session_state.units.append({"size": "", "price": "", "brand": "", "description": ""})

# Add unit button
if st.button("➕ Add Window/Door Unit"):
    add_unit()

# Display input fields for each unit
for i, unit in enumerate(st.session_state.units):
    st.subheader(f"Unit {i+1}")
    size = st.text_input(f"Size for Unit {i+1}", value=unit["size"], key=f"size_{i}")
    price = st.text_input(f"Price for Unit {i+1}", value=unit["price"], key=f"price_{i}")
    brand = st.text_input(f"Brand for Unit {i+1}", value=unit["brand"], key=f"brand_{i}")
    description = st.text_input(f"Description for Unit {i+1}", value=unit["description"], key=f"description_{i}")
    st.session_state.units[i] = {"size": size, "price": price, "brand": brand, "description": description}

# Create proposal button
if st.button("📄 Create Proposal"):
    if not openai.api_key:
        st.error("Please set your OpenAI API key in Streamlit secrets.")
    elif not customer_name or not job_details or not st.session_state.units:
        st.warning("Please fill in all required fields and add at least one unit.")
    else:
        # Build the prompt
        prompt = f"""
        Write a professional, persuasive sales proposal for a residential window/door project.

        Customer Name: {customer_name}
        Job Details: {job_details}

        Items in Proposal:
        """
        for u in st.session_state.units:
            prompt += f"\n- {u['brand']} {u['description']} ({u['size']}) at ${u['price']}"

        prompt += "\nFocus on clarity, professionalism, and highlighting quality."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional proposal writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            proposal_text = response.choices[0].message.content
            st.subheader("Generated Proposal")
            st.write(proposal_text)

        except Exception as e:
            st.error(f"Error generating proposal: {e}")
