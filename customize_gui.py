##################################################
# Brian Lesko  12/3/2023
# This code implements some some gui shortcuts that are used to customize the UI of the app.py file - using the low code streamlit library.

import streamlit as st

class gui:
    def __init__(self):
        pass

    def setup(self,wide=False, text="In this code we ... "):
        self.clean_format(wide=wide)
        self.about(text=text)

    def about(self, photo_path = 'docs/bl.png', author = "Brian", text = "In this code we ... "):
        with st.sidebar:
            col1, col2, = st.columns([1,5], gap="medium")
            with col1:
                self.add_custom_css()
                st.image(photo_path)
            with col2:
                st.write(f"Hey it's {author},   \n  \n  {text}")
            # Socials
            self.add_custom_css_socials()  # Call the function to add the CSS
            col1, col2, col3, col4, col5, col6 = st.columns([1.1,1,1,1,1,1.5], gap="medium")
            with col2:  # Twitter
                st.markdown("<a href='https://twitter.com/BrianJosephLeko' class='social-img'><img src='https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/x-logo-blue.svg'></a>", unsafe_allow_html=True)
            with col3:  # GitHub
                st.markdown("<a href='https://github.com/BrianLesko' class='social-img'><img src='https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/github-mark-blue.svg'></a>", unsafe_allow_html=True)
            with col4:  # LinkedIn
                st.markdown("<a href='https://www.linkedin.com/in/brianlesko/' class='social-img'><img src='https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/linkedin-icon-blue.svg'></a>", unsafe_allow_html=True)
            #with col5:  # YouTube (assuming you have a correct link and image)
                #st.markdown("<a href='https://www.youtube.com/user/YourChannel' class='social-img'><img src='https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/yt-logo-blue.svg'></a>", unsafe_allow_html=True)
            #with col6:  # Placeholder for Blog Visual Study Code
                #st.markdown("<a href='https://www.visualstudycode.com/' class='social-img'>Blog Visual Study Code</a>", unsafe_allow_html=True)  # Replace with your actual image and link if needed
            
    def clean_format(self, wide=False):
        if wide == True: st.set_page_config(layout='wide')
        hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
                </style>
                """
        st.markdown(hide_st_style, unsafe_allow_html=True)

    def display_existing_messages(self,state):
        for msg in state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    def add_custom_css_socials(self):
        st.markdown("""
            <style>
            .social-img img {
                filter: grayscale(100%); /* Converts images to grayscale */
                transition: filter 0.3s; /* Smooth transition for the filter effect */
            }
            .social-img img:hover {
                filter: grayscale(0%) brightness(110%) saturate(140%); /* Blue tint on hover */
            }
            </style>
            """, unsafe_allow_html=True)
        
    def add_custom_css(self):
        st.markdown("""
            <style>
            .social-img img {
                filter: grayscale(100%); /* Converts images to grayscale */
                transition: filter 0.3s; /* Smooth transition for the filter effect */
            }
            .social-img img:hover {
                filter: grayscale(0%) sepia(100%) hue-rotate(200deg) brightness(90%) saturate(100%); /* Blue tint on hover */
            }
            </style>
            """, unsafe_allow_html=True)