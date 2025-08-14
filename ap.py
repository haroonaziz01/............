import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io

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

# Hide Streamlit menu & footer
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# Single Dark Theme
bg_color = "#1e1e1e"
plot_bg = "#2b2b2b"
text_color = "white"
button_bg = "#444"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    label, .stSelectbox label, .stTextInput label, .stRadio label, .stCheckbox label {{
        color: {text_color} !important;
        font-size: 14px !important;
    }}
    div.stButton > button {{
        background-color: {button_bg};
        color: {text_color} !important;
        border: 1px solid white;
        border-radius: 5px;
        padding: 0.4em 1em;
    }}
    div.stDownloadButton > button {{
        background-color: {button_bg};
        color: {text_color} !important;
        border: 1px solid white;
        border-radius: 5px;
        padding: 0.4em 1em;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- Main Heading -----------------
st.markdown(f"<h2 style='color:{text_color};'>📊 Binary Signal Visualizer</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{text_color}; font-size:14px;'>Developed By Laiba Noor</p>", unsafe_allow_html=True)

# ----------------- Inputs -----------------
binary_input = st.text_input("Enter Binary Sequence (e.g., 101010):", "")
encoding = st.selectbox("Select Encoding:", list(encoding_funcs.keys()))
signal_color = st.color_picker("Select Signal Color", "#2d0b8a")
show_binary_labels = st.checkbox("Show Binary Numbers Under Graph", True)
add_noise = st.checkbox("Add Noise to Signal", False)

# ----------------- Generate Signal -----------------
if st.button("Generate Signal"):
    if not binary_input or any(b not in "01" for b in binary_input):
        st.error("⚠ Please enter a valid binary sequence!")
    else:
        signal = encoding_funcs[encoding](binary_input)

        if add_noise:
            noise = np.random.normal(0, 0.2, len(signal))
            signal = list(np.array(signal) + noise)

        # Main Graph
        fig, ax = plt.subplots(figsize=(7, 3))
        t = np.arange(0, len(signal))
        ax.step(t, signal, where='post', color=signal_color, linewidth=2)

        if show_binary_labels:
            for i, b in enumerate(binary_input):
                ax.text(i + 0.4, 1.5, b, fontsize=10, ha='center', color=text_color)

        ax.set_ylim(-2, 2)
        ax.set_title(f"{encoding} Encoding", fontsize=14, fontweight="bold", color=text_color)
        ax.grid(True, color="gray", linestyle="--", alpha=0.6)
        ax.set_facecolor(plot_bg)
        ax.tick_params(colors=text_color)
        for spine in ax.spines.values():
            spine.set_color(text_color)
        fig.patch.set_facecolor(plot_bg)

        st.pyplot(fig)

        # Data Table
        df = pd.DataFrame({"Time": t, "Value": signal})
        st.dataframe(df)

        # Download PNG
        buf = io.BytesIO()
        fig.savefig(buf, format="png", facecolor=plot_bg)
        st.download_button("📥 Download Graph as PNG", data=buf.getvalue(), file_name="signal.png", mime="image/png")

        # Download CSV
        csv = df.to_csv(index=False).encode()
        st.download_button("📥 Download Data as CSV", data=csv, file_name="signal_data.csv", mime="text/csv")

        # Compare Multiple Encodings
        st.subheader("Compare Multiple Encodings")
        fig2, axes = plt.subplots(3, 3, figsize=(12, 8))
        axes = axes.flatten()
        for i, (name, func) in enumerate(encoding_funcs.items()):
            sig = func(binary_input)
            axes[i].step(np.arange(0, len(sig)), sig, where='post', color="#0080ff")
            axes[i].set_title(name, fontsize=8, color=text_color)
            axes[i].set_ylim(-2, 2)
            axes[i].grid(True, linestyle="--", alpha=0.5, color="gray")
            axes[i].tick_params(colors=text_color)
            for spine in axes[i].spines.values():
                spine.set_color(text_color)
            axes[i].set_facecolor(plot_bg)

        fig2.patch.set_facecolor(bg_color)
        plt.tight_layout()
        st.pyplot(fig2)
