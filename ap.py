import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ----------------- Encoding Functions -----------------
def unipolar(binary):
    return [1 if b == '1' else 0 for b in binary]

def nrz_l(binary):
    return [1 if b == '1' else -1 for b in binary]

def nrz_i(binary):
    signal = []
    last = 1
    for b in binary:
        if b == '1':
            last *= -1
        signal.append(last)
    return signal

def rz(binary):
    signal = []
    for b in binary:
        if b == '1':
            signal.extend([1, 0])
        else:
            signal.extend([-1, 0])
    return signal

def manchester(binary):
    signal = []
    for b in binary:
        if b == '1':
            signal.extend([1, -1])
        else:
            signal.extend([-1, 1])
    return signal

def diff_manchester(binary):
    signal = []
    last = 1
    for b in binary:
        if b == '0':
            last *= -1
        signal.extend([last, -last])
    return signal

def ami(binary):
    signal = []
    last = -1
    for b in binary:
        if b == '1':
            last *= -1
            signal.append(last)
        else:
            signal.append(0)
    return signal

def b8zs(binary):
    return ami(binary)

def hdb3(binary):
    return ami(binary)

encoding_funcs = {
    "Unipolar": unipolar,
    "NRZ-L": nrz_l,
    "NRZ-I": nrz_i,
    "RZ": rz,
    "Manchester": manchester,
    "Differential Manchester": diff_manchester,
    "AMI": ami,
    "B8ZS": b8zs,
    "HDB3": hdb3
}

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Binary Signal Visualizer", layout="wide")

# Hide Streamlit top header & footer
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# Theme selection
theme = st.radio("Select Theme:", ["Dark", "Light", "Soft Gray"], horizontal=True)

# Theme colors
if theme == "Dark":
    bg_color = "#1e1e1e"
    plot_bg = "#2b2b2b"
    text_color = "white"
elif theme == "Light":
    bg_color = "white"
    plot_bg = "white"
    text_color = "black"
else:  # Soft Gray
    bg_color = "#dcdcdc"
    plot_bg = "#e6e6e6"
    text_color = "black"

# Apply background + text color to all elements
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    label, .stSelectbox label, .stTextInput label, .stRadio label {{
        color: {text_color} !important;
        font-size: 14px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Headings
st.markdown(f"<h2 style='color:{text_color};'>📊 Binary Signal Visualizer</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{text_color}; font-size:14px;'>Developed By Laiba Noor</p>", unsafe_allow_html=True)

# Inputs
binary_input = st.text_input("Enter Binary Sequence (e.g., 101010):", "")
encoding = st.selectbox("Select Encoding:", list(encoding_funcs.keys()))

# Button
if st.button("Generate Signal"):
    if not binary_input or any(b not in "01" for b in binary_input):
        st.error("⚠ Please enter a valid binary sequence!")
    else:
        signal = encoding_funcs[encoding](binary_input)

        fig, ax = plt.subplots(figsize=(7, 3))
        t = np.arange(0, len(signal))
        ax.step(t, signal, where='post', color="#ff6600", linewidth=2)

        ax.set_ylim(-2, 2)
        ax.set_title(f"{encoding} Encoding", fontsize=14, fontweight="bold", color=text_color)
        ax.grid(True, color="gray", linestyle="--", alpha=0.6)
        ax.set_facecolor(plot_bg)
        ax.tick_params(colors=text_color)
        fig.patch.set_facecolor(plot_bg)

        st.pyplot(fig)
