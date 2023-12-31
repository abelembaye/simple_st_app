from io import BytesIO
import base64
from PIL import Image
import streamlit as st
from datetime import date
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import pandas as pd
from streamlit_drawable_canvas import st_canvas
import json
import os

st.set_page_config(layout="centered", page_icon="", page_title=" Simple App")
st.title("Simple Streaml Form App")

# Load HTML template
env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())

# here the template is directly in the main .py file which is not ideal
template = env.get_template("template.html")
st.write("Answer the following questions based on the assignment post on Blackboard:")
form = st.form("template_form")

student_name = form.text_input("Full NAME", placeholder="John Doe")
# q01 = form.text_area(label="questions 1 answered here:", height=200, max_chars=500, placeholder="No place like Economics!")
q01 = form.text_input("Your answer to question #1",
                      placeholder="one line answer", key="q01")
q02 = form.slider('How old are you?', 0, 120, 0)

submit = form.form_submit_button("Generate html file")

# this two lines are responsible for the canvas
# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

realtime_update = st.sidebar.checkbox("Update in realtime", True)

    

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=Image.open(bg_image) if bg_image else None,
    update_streamlit=realtime_update,
    height=150,
    drawing_mode=drawing_mode,
    point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas",
)

# Do something interesting with the image data and paths
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)
if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
    st.dataframe(objects)

if submit:
    # Render the HTML template
    html = template.render(
        student_name=student_name,
        q01=q01,
        q02=q02,

    )

    st.balloons()

    st.success("🎉 Your file has been generated! you can  download it by clicking the below button to save it and submit it in gradescope assignment!")
    st.download_button(
        "⬇️ Download html",
        data=html,
        file_name="HW_report.html",
        mime="application/octet-stream",
    )

# This file uses the folder and virt env below:
# directory: cd "C:\Users\aembaye\OneDrive - University of Arkansas\C2-embaye\Rh\Learn\_Python\myProjects\Streamlit_apps/simple_st_app"
# ../venv4pdfgen/Scripts/activate.ps1
# streamlit run ./main2.py
