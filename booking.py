
import main, mongoUpdates, qrcode, streamlit as st
from datetime import datetime
from io import BytesIO

def qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    return img

def movie_data():
    movies = set()
    movies_list = main.records.find({}, {"movie": True})
    for x in movies_list:
        movies.add(x["movie"])
    movies = list(movies)

    movie = st.radio("select movie name:", movies, index=0)
    theatre_data = main.records.find({"movie": movie})
    data = [x["theatre"] for x in theatre_data]
    theatre = st.radio("select: theatre name:", data, index=0)

    data_date = main.records.find_one({"theatre": theatre})
    dates = [x for x in data_date["dates"]]

    min_date = datetime.strptime(dates[0], '%Y-%m-%d')
    max_date = datetime.strptime(dates[-1], '%Y-%m-%d')

    date_data = st.date_input('Select booking date', value=min_date, min_value=min_date, max_value=max_date)

    date_object = date_data
    date = date_object.strftime('%Y-%m-%d')

    shows = []
    data_date = main.records.find_one({"theatre": theatre})
    shows.extend(data_date["dates"][date]["timings"].keys())
    show = st.radio("select show timings:", shows, index=0)

    seats = data_date["dates"][date]["timings"][show]['seat availability']
    st.write("Avaialable seats for this show is {}".format(seats))
    if seats == 0:
        st.write("OOPS HOUSEFULL TRY WITH DIFFERENT COMBINATION")
    elif seats < 4:
        selected_value = st.slider('Select numbers of seats', 1, seats)
    else:
        selected_value = st.slider('Select numbers of seats', 1, 4)

    do = st.button("BOOK NOW")
    if do:
        seat_nums = [str(x) for x in range(seats, seats - selected_value, -1)]
        seat_nums.sort()
        num = int(seat_nums[0]) - 1
        seat_numbers = ",".join(seat_nums)
        ticket = "movie : {}\ntheatre : {}\ndate : {}\nshow time : {}\nseat numbers = {}".format(data_date["movie"],
                                                                                                 theatre, date, show,
                                                                                                 seat_numbers)
        mongoUpdates.booking_update(theatre, date, show, num)






        qr_img = qr_code(ticket)

        # Convert PIL Image to bytes and display in Streamlit
        img_bytes = BytesIO()
        qr_img.save(img_bytes, format='PNG')
        st.image(img_bytes.getvalue())
        st.download_button(label='Download QR Code', data=img_bytes.getvalue(), file_name='qr_code.png',
                           mime='image/png')
















































