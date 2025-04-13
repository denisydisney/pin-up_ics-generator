import streamlit as st
import datetime
import urllib.parse
import pytz

# Временная зона UTC+3
tz_utc_plus_3 = pytz.timezone("Etc/GMT-3")  # UTC+3

st.title("🔗 Google Calendar Link Generator")

st.markdown("🕒 **Please specify time in UTC+3**")

# Ввод данных от пользователя
summary = st.text_input("Event name")
description = st.text_area("Description")
location = st.text_input("Location")
event_url = st.text_input("Event Link")

start_date = st.date_input("Start date")
start_time = st.time_input("Start time (UTC+3)", value=datetime.time(10, 0))
end_date = st.date_input("End date")
end_time = st.time_input("End time (UTC+3)", value=datetime.time(11, 0))

# Проверка на корректность дат
if datetime.datetime.combine(end_date, end_time) <= datetime.datetime.combine(start_date, start_time):
    st.error("❌ The end time must be later than the start time")
else:
    def generate_google_calendar_link():
        # Переводим в UTC
        local_start = tz_utc_plus_3.localize(datetime.datetime.combine(start_date, start_time))
        local_end = tz_utc_plus_3.localize(datetime.datetime.combine(end_date, end_time))

        start_utc = local_start.astimezone(datetime.timezone.utc)
        end_utc = local_end.astimezone(datetime.timezone.utc)

        start_str = start_utc.strftime("%Y%m%dT%H%M%SZ")
        end_str = end_utc.strftime("%Y%m%dT%H%M%SZ")

        # Формируем ссылку
        base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
        params = {
            "text": summary,
            "details": f"{description}",
            "location": location,
            "dates": f"{start_str}/{end_str}"
        }
        url = base_url + "&" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return url

    if st.button("🔗 Generate link"):
        link = generate_google_calendar_link()
        st.success("✅ The link is ready!")
        st.markdown(f"[👉 Proceed to create an event in Google Calendar]({link})")
        st.code(link, language="text")
