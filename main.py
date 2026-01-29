import streamlit as st
st.header("Student information form")

st.title("enter your details")

st.subheader("Please fill out the form below:")

st.markdown("---------")

st.text("This form collects basic student information.")

st.write({"name":"noor","age":1})

st.markdown("### Thank you for your cooperation!")
st.markdown("**Bold**")
st.markdown("*Italic*")
st.markdown("-Item 1\n-Item 2\n-Item 3")
st.markdown("<h3 style=color:blue>Thank you!!</h3>",unsafe_allow_html=True)

st.caption("This is a caption for the form.")

st.code("""
        def add(a,b):
            return a+b
        """,language="python")

st.latex(r"""
a^2 + b^2 = c^2
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.write("This is column 1")

with col2:
    st.write("This is column 2")

if st.button("click me"):
    st.write("Button clicked!")
    st.success("Form submitted successfully!")
    st.balloons()
else:
    st.write("Please click the button to submit the form.")
name=st.text_input("Enter your name:")
if name =="":
    st.warning("Name cannot be empty")
elif not name.isalpha():
    st.error("Name must contain only letters")
else:
    st.success("Valid name")

feedback=st.text_area("Enter your feedback:")
st.write("You entered:",feedback)

st.checkbox("I agree to the terms and conditions")

option=st.radio("Select your grade:",["A","B","C","D","F"])
st.write(f"You selected grade: {option}")

abc=st.selectbox("Select your major:",["Computer Science","Mathematics","Physics","Chemistry"])
st.write(f"You selected major: {abc}")

select=st.multiselect("Select your hobbies:",["Reading","Sports","Music","Traveling"])
st.write(f"You selected hobbies: {select}")

age=st.slider("Select your age:",0,100,25)
st.write(f"You selected age: {age}")


pro=st.file_uploader("Upload your profile picture:",type=["jpg","png","jpeg"])
if pro is not None:
    st.image(pro)

with st.form("submission_form"):
    st.text_input("Enter your email:")
    st.number_input("Enter your student ID:",min_value=0)
    sub=st.form_submit_button("Submit")
if sub:
    st.write("Form submitted!")

c1, c2,c3=st.columns(3)
with c1:
    st.button("Column 1 Button")
with c2:
    st.button("Column 2 Button")
with c3:
    st.button("Column 3 Button")


con=st.container()
con.write("This is inside a container.")
con.button("click")

data={"Name":"Noor","Age":1,"Major":"CS"}
st.table(data)

options=st.sidebar.selectbox("Select an option:",["Option 1","Option 2","Option 3"])
st.sidebar.write(f"You selected: {options}")

@st.cache_data
def compute_square(n):
    return n*n
p=st.number_input("enter a number to compute its square:")
result=compute_square(p)
st.write(f"The square of {p} is {result}")
