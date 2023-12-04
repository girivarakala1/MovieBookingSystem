import pymongo, mongoUpdates, registrations,booking,streamlit as st


client = pymongo.MongoClient("mongodb+srv://girivarkala1:Butterfly1211@cluster0.ca6tkne.mongodb.net/?retryWrites=true&w=majority")
db = client.cinemas

record_users = db.users
records = db.theatres


def main():
    # mongoUpdates.update_all_theatres()
    tab1, tab2, tab3 = st.tabs(["HOME", "BOOKING", "EXTRA"])
    global res_name

    with tab1:
        st.write("WELCOME USER..SELECT LOGIN OR REGISTRATION")
        task = st.radio("Choose a task:", ["login", "registration"])
        if task == "registration":
            res_reg = registrations.user_registration()
            st.write(res_reg)
        elif task == "login":
            res_name = registrations.user_login()
            if res_name:
                st.write(f"Hi {res_name}")
                st.write("please go to booking page to book your tickets")
    with tab2:
        st.write(f"Hi {res_name}")
        st.write("Book your tickets and enjoy")
        booking.movie_data()



    with tab3:
        st.write("this is extra page")





res_name = ""
if __name__ == "__main__":
    main()




