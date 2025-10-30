import streamlit as st
from math import sqrt

st.set_page_config(page_title="iPhone-style Calculator", layout="wide")

# --- Styles to make buttons look like a phone calculator (light theme) ---
st.markdown(
    """
    <style>
    .calc-display {
        background: #ffffff;
        color: #000000;
        font-size:48px;
        text-align: right;
        padding: 18px 16px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        margin-bottom: 12px;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    div.stButton > button {
        height: 72px;
        width: 72px;
        margin: 6px 6px;
        border-radius: 36px;
        font-size: 22px;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    /* operators (right column) */
    .op-button {
        background: #ff9500 !important;
        color: white !important;
    }
    /* special buttons (AC, +/-, %) */
    .spec-button {
        background: #d4d4d2 !important;
        color: black !important;
    }
    /* zero button double width */
    .zero-space { display:flex; gap: 8px; align-items: center; }
    .zero-button {
        width: 156px !important;
        text-align: left;
        padding-left: 28px;
        border-radius: 36px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session state ---
if "display" not in st.session_state:
    st.session_state.display = "0"
if "operand" not in st.session_state:
    st.session_state.operand = None
if "operator" not in st.session_state:
    st.session_state.operator = None
if "reset_next" not in st.session_state:
    st.session_state.reset_next = False

def update_display(text):
    st.session_state.display = text

def press_digit(d):
    if st.session_state.reset_next:
        st.session_state.display = d
        st.session_state.reset_next = False
    else:
        # avoid multiple leading zeros
        if st.session_state.display == "0" and d != ".":
            st.session_state.display = d
        else:
            st.session_state.display += d

def press_decimal():
    if st.session_state.reset_next:
        st.session_state.display = "0."
        st.session_state.reset_next = False
    elif "." not in st.session_state.display:
        st.session_state.display += "."

def press_clear():
    st.session_state.display = "0"
    st.session_state.operand = None
    st.session_state.operator = None
    st.session_state.reset_next = False

def press_plus_minus():
    if st.session_state.display.startswith("-"):
        st.session_state.display = st.session_state.display[1:]
    else:
        if st.session_state.display != "0":
            st.session_state.display = "-" + st.session_state.display

def press_percent():
    try:
        val = float(st.session_state.display)
        st.session_state.display = str(val / 100.0)
    except:
        st.session_state.display = "Error"

def set_operator(op):
    try:
        st.session_state.operand = float(st.session_state.display)
    except:
        st.session_state.operand = 0.0
    st.session_state.operator = op
    st.session_state.reset_next = True

def press_equals():
    if st.session_state.operator is None:
        return
    try:
        a = st.session_state.operand if st.session_state.operand is not None else 0.0
        b = float(st.session_state.display)
        result = None
        if st.session_state.operator == "+":
            result = a + b
        elif st.session_state.operator == "-":
            result = a - b
        elif st.session_state.operator == "*":
            result = a * b
        elif st.session_state.operator == "/":
            if b == 0:
                st.session_state.display = "Error"
                st.session_state.operator = None
                st.session_state.reset_next = True
                return
            result = a / b
        elif st.session_state.operator == "^":
            result = a ** b
        # format result to avoid long floats
        if result is not None:
            # trim .0 if integer
            if abs(result - int(result)) < 1e-12:
                result = int(result)
            st.session_state.display = str(result)
    except Exception as e:
        st.session_state.display = "Error"
    st.session_state.operator = None
    st.session_state.operand = None
    st.session_state.reset_next = True

# --- Layout ---
st.title("iPhone-style Calculator (Light)")
st.write("")

# Display area
st.markdown(f"<div class='calc-display'>{st.session_state.display}</div>", unsafe_allow_html=True)

# Buttons grid
col1, col2, col3, col4 = st.columns([1,1,1,1], gap="small")

with col1:
    if st.button("AC", key="ac"):
        press_clear()
    if st.button("7", key="7"):
        press_digit("7")
    if st.button("4", key="4"):
        press_digit("4")
    if st.button("1", key="1"):
        press_digit("1")
with col2:
    if st.button("+/-", key="pm"):
        press_plus_minus()
    if st.button("8", key="8"):
        press_digit("8")
    if st.button("5", key="5"):
        press_digit("5")
    if st.button("2", key="2"):
        press_digit("2")
with col3:
    if st.button("%", key="pct"):
        press_percent()
    if st.button("9", key="9"):
        press_digit("9")
    if st.button("6", key="6"):
        press_digit("6")
    if st.button("3", key="3"):
        press_digit("3")
with col4:
    # operator column: ÷ × − +
    if st.button("÷", key="div"):
        set_operator("/")
    if st.button("×", key="mul"):
        set_operator("*")
    if st.button("−", key="sub"):
        set_operator("-")
    if st.button("+", key="add"):
        set_operator("+")

# Last row: 0 . =
col1, col2, col3 = st.columns([2,1,1], gap="small")
with col1:
    if st.button("0", key="zero"):
        press_digit("0")
with col2:
    if st.button(".", key="dot"):
        press_decimal()
with col3:
    if st.button("=", key="eq"):
        press_equals()

st.write("")

st.caption("Made with Streamlit — iPhone-like layout and basic calculator behavior.")