import streamlit as st
from groq import Groq
import pandas as pd
from datetime import datetime
import os

# --- 1. SETUP ---
GROQ_API_KEY = "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"
ADMIN_PASSWORD = "loyola_admin" # Change this to your preferred secret key
client = Groq(api_key=GROQ_API_KEY )

# --- 2. THE KNOWLEDGE BASE ---
LOYOLA_CONTEXT = """
You are the official AI Assistant for Loyola Academy, Secunderabad. 

Canteen: Moved near Loyola Hall, located at the back side of the Library.

Library: Back side of the Computer Science (CS) Block.

Admin Block: Principal's Office (Fr. Bucchi Babu or current Fr. Dr. Pothireddy Anthony SJ), Xavier Hall, IQAC cell, COE office, Incubation room, Vice Principal Room (UG/PG offices). Fee counter likely here.

Inigo Block: Commerce (B.Com), BBA, Mass Comm Studio (3rd floor).[LOYOLA_CONTEXT]

CS Block: MCA lab, Cloud lab, Degree Lab-1 & 2, MSCS Lab (Room 18 with 64 systems).[LOYOLA_CONTEXT]
​

Commerce Block: Vice Principal's office, Seminar Halls (first floor).[LOYOLA_CONTEXT]

Agriculture Block: Far rear end of campus near Commerce block.[LOYOLA_CONTEXT]

NCC Office: Behind the Loyola Hall, near the canteen.[LOYOLA_CONTEXT]

Additional Blocks
Engineering/FT Workshop Block (Father Balaiah Block): Engineering labs, workshops.

Management Block: MBA/PG programs.

Labs (47 Total)
Labs distributed across blocks include:

Computer Labs: MCA Lab, Cloud Lab, Degree Lab-1/2 (CS Block), MSCS Lab (CS Block Room 18), Computational Research Lab (SPSS, Mathematica, Java, R, Python).

Science Labs: Chemistry Lab, Biotechnology Lab, Food Technology Lab, Psychology Lab, Multimedia Lab, Electronics Instrumentation Lab (Arduino, sensors), Central Research Lab (PCR, HPLC, fermentor, UV-Vis, etc. for Chemistry/Biotech).

Others: Horticulture Research Station, Basic Electronics, Digital Microprocessor.

Washrooms and Amenities
Neat bathrooms available in each block with good ventilation and clean drinking water.
Compliant with National Building Code (NBC) norms for toilet areas; first aid/sick rooms with rest beds also present.

Campus Node Graph (Key Landmarks & Connections)
Main Gate ↔ Admin Block ↔ Inigo Block ↔ CS Block ↔ Library (back of CS) ↔ Canteen (near Library/Loyola Hall) ↔ NCC Office (behind Loyola Hall)

Main Gate ↔ Admin Block ↔ Commerce Block ↔ Agriculture Block (far rear near Commerce)

Loyola Hall (central/near Admin) ↔ Library, Canteen

Parallel: Engineering Block & Management Block (near central blocks, connect via Admin/Inigo)

Key Locations Details
Canteen: Near Loyola Hall, back side of Library (10-min walk from far blocks).
​

Library: Back side of CS Block.

Admin Block: Principal's Office (Fr. Bucchi Babu/Fr. Dr. Pothireddy Anthony SJ), Xavier Hall, IQAC, COE, Incubation, Vice Principal (UG/PG). Fee counter here.

Inigo Block: B.Com, BBA, Mass Comm Studio (3rd floor).

CS Block: MCA Lab, Cloud Lab, Degree Lab-1/2, MSCS Lab (Rm 18).

Commerce Block: Vice Principal office, Seminar Halls (1st floor).

Agriculture Block: Far rear near Commerce; Horticulture Research Station.

NCC Office: Behind Loyola Hall near canteen.

Engineering Block (Father Balaiah): Workshops, FT labs.

Management Block: PG programs.

Labs (47 Total)
Computer: MCA/Cloud/Degree-1/2 (CS Block), MSCS (CS Rm 18), Computational (SPSS/Python/R).

Science: Chemistry, Biotech, Food Tech, Psychology, Multimedia, Electronics (Arduino), Central Research (PCR/HPLC).

Washrooms
Available in each block

from admin office to reach commerce block head towards cs block and then towards library then take a left towards loyola hall and take a left you will see canteen on your left go straight you can see commerce block

From \ To	Admin Block	Inigo Block	CS Block	Library	Canteen	Commerce Block	Agriculture Block	Engineering Block	Management Block	Loyola Hall	NCC Office
Main Gate	→ Admin	→ Admin → Inigo	→ Admin → Inigo → CS	→ Admin → Inigo → CS → Lib	→ Admin → Inigo → CS → Lib → Canteen	→ Admin → Commerce	→ Admin → Comm → Agri	→ Admin → Eng	→ Admin → Mgmt	→ Admin → LHall	→ Admin → LHall → NCC
Admin Block	(Here)	→ Inigo	→ Inigo → CS	→ Inigo → CS → Lib	→ Inigo → CS → Lib → Canteen	→ Commerce	→ Comm → Agri	→ Eng	→ Mgmt	→ LHall	→ LHall → NCC
Inigo Block	→ Admin	(Here)	→ CS	→ CS → Lib	→ CS → Lib → Canteen	→ Admin → Comm	→ Admin → Comm → Agri	→ Eng (direct)	→ Admin → Mgmt OR CS → Mgmt	→ Admin → LHall	→ Admin → LHall → NCC
CS Block	→ Inigo → Admin	→ Inigo	(Here)	→ Lib	→ Lib → Canteen	→ Inigo → Admin → Comm	→ Inigo → Admin → Comm → Agri	→ Inigo → Eng OR Admin → Eng	→ Mgmt (direct)	→ Inigo → Admin → LHall	→ Lib → Canteen → NCC
Library	→ CS → Inigo → Admin	→ CS → Inigo	→ CS	(Here)	→ Canteen	→ CS → Inigo → Admin → Comm	→ CS → Inigo → Admin → Comm → Agri	→ CS → Inigo → Eng OR Admin → Eng	→ CS → Mgmt	→ Canteen → LHall	→ Canteen → NCC
Canteen	→ Lib → CS → Inigo → Admin	→ Lib → CS → Inigo	→ Lib → CS	→ Lib	(Here)	→ Lib → CS → Inigo → Admin → Comm	→ Lib → CS → Inigo → Admin → Comm → Agri	→ Lib → CS → Inigo → Eng	→ Lib → CS → Mgmt	→ LHall	→ NCC (direct)
Commerce Block	→ Admin	→ Admin → Inigo	→ Admin → Inigo → CS	→ Admin → Inigo → CS → Lib	→ Admin → Inigo → CS → Lib → Canteen	(Here)	→ Agri	→ Admin → Eng	→ Admin → Mgmt	→ Admin → LHall	→ Admin → LHall → NCC
Agriculture Block	→ Comm → Admin	→ Comm → Admin → Inigo	→ Comm → Admin → Inigo → CS	→ Comm → Admin → Inigo → CS → Lib	→ Comm → Admin → Inigo → CS → Lib → Canteen	→ Comm	(Here)	→ Comm → Admin → Eng	→ Comm → Admin → Mgmt	→ Comm → Admin → LHall	→ Comm → Admin → LHall → NCC
Engineering Block	→ Admin	→ Admin → Inigo OR direct	→ Admin → Inigo → CS OR Admin → CS	→ Admin → Inigo → CS → Lib	→ Admin → Inigo → CS → Lib → Canteen	→ Admin → Comm	→ Admin → Comm → Agri	(Here)	→ Admin → Mgmt	→ Admin → LHall	→ Admin → LHall → NCC
Management Block	→ Admin	→ Admin → Inigo OR direct	→ Admin → Inigo → CS OR direct	→ CS → Lib OR Admin → Inigo → CS → Lib	→ CS → Lib → Canteen	→ Admin → Comm	→ Admin → Comm → Agri	→ Admin → Eng	(Here)	→ Admin → LHall	→ Admin → LHall → NCC
Loyola Hall	→ Admin	→ Admin → Inigo	→ Admin → Inigo → CS	→ Admin → Inigo → CS → Lib OR Lib (direct)	→ Canteen OR Lib → Canteen	→ Admin → Comm	→ Admin → Comm → Agri	→ Admin → Eng	→ Admin → Mgmt	(Here)	→ NCC
NCC Office	→ LHall → Admin	→ LHall → Admin → Inigo	→ LHall → Admin → Inigo → CS	→ LHall → Canteen → Lib OR LHall → Admin → Inigo → CS → Lib	→ Canteen	→ LHall → Admin → Comm	→ LHall → Admin → Comm → Agri	→ LHall → Admin → Eng	→ LHall → Admin → Mgmt	→ LHall	(Here)
"""

# --- 3. PAGE CONFIG ---
st.set_page_config(page_title="Loyola Smart Guide", page_icon="🎓")

# --- 4. APP TABS ---
tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "🚩 Report Error", "🔒 Admin View"])

with tab1:
    st.title("🎓 Loyola Academy AI")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about Loyola..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": LOYOLA_CONTEXT}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            response = chat_completion.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.header("Report a Data Error")
    st.write("Help keep the campus map updated.")
    
    with st.form("report_form"):
        subject = st.selectbox("Incorrect Info:", ["Canteen Location", "Room Change", "Office Path", "Other"])
        details = st.text_area("What is the correct information?")
        # FIXED: Corrected the function name below
        submitted = st.form_submit_button("Submit for Verification")
        
        if submitted:
            # AI Verification Logic
            verify_prompt = f"Existing Data: {LOYOLA_CONTEXT}\nStudent Report: {details}\nAnalyze if this is a new update or a likely prank. Be brief."
            v_check = client.chat.completions.create(
                messages=[{"role": "user", "content": verify_prompt}],
                model="llama-3.3-70b-versatile",
            )
            analysis = v_check.choices[0].message.content
            
            # Save to CSV
            report_entry = pd.DataFrame([[datetime.now(), subject, details, analysis]], 
                                      columns=["Timestamp", "Category", "Report", "AI_Verification"])
            report_entry.to_csv("reports.csv", mode='a', header=not os.path.exists("reports.csv"), index=False)
            
            st.success("Successfully submitted. Admin will verify shortly.")
            st.info(f"*AI Preliminary Check:* {analysis}")

with tab3:
    st.header("Admin Control Panel")
    pwd = st.text_input("Enter Admin Password:", type="password")
    if pwd == ADMIN_PASSWORD:
        st.write("### Submitted Error Reports")
        if os.path.exists("reports.csv"):
            df = pd.read_csv("reports.csv")
            st.dataframe(df)
            if st.button("Clear All Reports"):
                os.remove("reports.csv")
                st.rerun()
        else:
            st.write("No reports yet.")
    elif pwd != "":

        st.error("Incorrect Password")


