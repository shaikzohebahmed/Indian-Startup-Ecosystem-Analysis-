import streamlit as st
from analysis import Startup as StartupAnalysis

class Startup:

    def __init__(self):
        self.startup_analysis = StartupAnalysis()

    def similar_startups(self, startup_name):
        
        similar_startups = self.startup_analysis.similar_startups(startup_name)

        # Display the header for similar startups section
        st.subheader(
            'Similar Startups',
            help=f"These startups belong to the same sector as {startup_name}."
        )
        st.write('')

        # Create columns for displaying similar startups
        col0, col1, col2, col3 = st.columns(4)

        # Display the first similar startup in column 0
        with col0:
            try:
                st.write(similar_startups[0])
            except IndexError:
                st.write('')

        # Display the second similar startup in column 1
        with col1:
            try:
                st.write(similar_startups[1])
            except IndexError:
                st.write('')

        # Display the third similar startup in column 2
        with col2:
            try:
                st.write(similar_startups[2])
            except IndexError:
                st.write('')

        # Display the fourth similar startup in column 3
        with col3:
            try:
                st.write(similar_startups[3])
            except IndexError:
                st.write('')
