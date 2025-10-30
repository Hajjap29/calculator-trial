import streamlit as st
import math

st.set_page_config(page_title="Text-based Calculator", layout="centered")

st.title("🧮 Text-based Calculator")

st.write("Type any mathematical expression below and press **Calculate**. You can use functions like `sqrt(9)`, `sin(30)`, `log(10)` etc.")

# Create a secure environment for eval
safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
safe_dict.update({"abs": abs, "round": round})

expr = st.text_input("Enter your expression:", placeholder="e.g., 5*6 + sqrt(9) - 2**3")

if st.button("Calculate"):
    try:
        # Evaluate safely using only math functions
        result = eval(expr, {"__builtins__": None}, safe_dict)
        st.success(f"✅ Result: {result}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

st.markdown("""
### Examples:
- `2 + 3 * 4`
- `sqrt(16) + 10`
- `sin(45) + cos(60)`
- `log(100, 10)`
""")