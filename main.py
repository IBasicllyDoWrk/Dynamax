import streamlit as st

from streamlit_option_menu import option_menu

import home, account, about

st.set_page_config(
    page_title="Dynamax",
)

class MultiApp:

    def __init__(self):
        self.app = []
    def add_app(self, title, function):
        self.app.append({
            "title": title,
            "function": function
        })

    def run():

        with st.sidebar:
            app = option_menu( 
                menu_title='Dynamax ',
                options=['Home','Account','About',],
                icons=['house-fill','person-circle','info-circle-fill'],
                menu_icon='cone',
                 default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#d62903"},
        "nav-link-selected": {"background-color": "#da4a2a"},}
                
                )
        if app == "Home":
            home.app()
        if app == "Account":
            account.app()
        if app == "About":
            about.app()

    run()