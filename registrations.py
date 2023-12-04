import main, re
import streamlit as st


def verify_password(password):
    if (len(password) <= 8):
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[_@$]", password):
        return False
    elif re.search("\s", password):
        return False
    else:
        return True



def validate_number(number):

    # return num.isdigit() and len(num) == 10
    return bool(re.match(r'^\d{10}$', number))


def validate_mail(mail):

    '''
    data = mail.split("@")
    return mail.count("@") == 1 and data[1] in ("gmail.com", "yahoo.com", "outlook.com") and bool(
        re.match(r'[A-Za-z0-9._-]+', data[0]))
    '''

    return bool(re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', mail))


def user_registration():
    user_name = st.text_input("enter name: ")
    user_mail = st.text_input("enter mail: ")
    user_password = st.text_input("enter password: ", type="password")
    user_number = st.text_input("enter number: ")
    do = st.button("submit")
    if do:
        if not validate_number(user_number):
            st.write("Invalid phone number ")
        if not validate_mail(user_mail):
            st.write("Invalid mail id")
        if not verify_password(user_password):
            st.write("Invalid password - password contains at least 8 letters, at least 1 upper, 1 lower, 1 digit, 1 special symbol")

        else:
            result = main.record_users.find_one({"$or": [{"email": user_mail}, {"number": user_number}]})
            if result:
                return "mail_id or phone number exist"
            else:
                data = {"name": user_name, "number": user_number, "email": user_mail, "password": user_password,
                        "image": "image"}
            main.record_users.insert_one(data)
            return "registration successful..please login to continue"




def user_login():
    user_mail = st.text_input("enter mail: ")
    user_password = st.text_input("enter password: ", type="password")
    do = st.button("submit")
    if do:
        res = main.record_users.find_one({"$and": [{"email": user_mail}, {"password": user_password}]},
                                         {"_id": False, "name": True})
        if res:
            return res["name"]
        else:
            st.write("Invalid credential.. try again")








