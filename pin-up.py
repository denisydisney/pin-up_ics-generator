import streamlit as st
import datetime
import io

st.title("📅 Generator .ics")

# Ввод данных пользователем
summary = st.text_input("Event name")
description = st.text_area("Description")
location = st.text_input("Location")
event_url = st.text_input("Event Link")
start_date = st.date_input("Start date")
start_time = st.time_input("Start time", value=datetime.time(23, 59))
end_date = st.date_input("End date")
end_time = st.time_input("End time", value=datetime.time(23, 59))
alarm_minutes = st.number_input("How many minutes in advance to remind?", min_value=0, step=5, value=60)

# Проверка корректности введенных дат и времени
if datetime.datetime.combine(end_date, end_time) <= datetime.datetime.combine(start_date, start_time):
    st.error("❌ The end time must be later than the start time.")
else:
    # Функция для генерации содержимого .ics файла
    def generate_ics_content():
        dtstamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dtstart = f"{start_date.strftime('%Y%m%d')}T{start_time.strftime('%H%M')}00Z"
        dtend = f"{end_date.strftime('%Y%m%d')}T{end_time.strftime('%H%M')}00Z"

        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Custom Event Generator//EN
BEGIN:VEVENT
UID:event-{dtstamp}@yourdomain.com
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{summary}
DESCRIPTION:{description}\\nСсылка: {event_url}
LOCATION:{location}
URL:{event_url}
BEGIN:VALARM
TRIGGER:-PT{alarm_minutes}M
ACTION:DISPLAY
DESCRIPTION:Напоминание: {summary} - {event_url}
END:VALARM
END:VEVENT
END:VCALENDAR"""
        return ics_content

    # Кнопка для скачивания .ics файла
    if st.button("Create and download .ics file"):
        ics_content = generate_ics_content()
        # Создание буфера в памяти и запись содержимого .ics
        buf = io.BytesIO()
        buf.write(ics_content.encode())
        buf.seek(0)

        # Предоставление кнопки для скачивания файла
        st.download_button(
            label="📥 Download event.ics",
            data=buf,
            file_name="event.ics",
            mime="text/calendar"
        )
