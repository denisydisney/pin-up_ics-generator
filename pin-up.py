import streamlit as st
import datetime
import io
import pytz

# Временная зона UTC+3 (Киев, Вильнюс, Минск и др.)
tz_utc_plus_3 = pytz.timezone("Etc/GMT-3")  # внимание! в pytz "Etc/GMT-3" = UTC+3

st.title("📅 Generator .ics")

st.markdown("🕒 **Please indicate time according to UTC+3**")

# Ввод данных пользователем
summary = st.text_input("Event name")
description = st.text_area("Description")
location = st.text_input("Location")
event_url = st.text_input("Event Link")
start_date = st.date_input("Start date")
start_time = st.time_input("Start time (UTC+3)", value=datetime.time(11, 45))
end_date = st.date_input("End date")
end_time = st.time_input("End time (UTC+3)", value=datetime.time(23, 59))
alarm_minutes = st.number_input("How many minutes in advance to remind?", min_value=0, step=5, value=60)

# Проверка корректности введённых дат и времени
if datetime.datetime.combine(end_date, end_time) <= datetime.datetime.combine(start_date, start_time):
    st.error("❌ The end time must be later than the start time.")
else:
    def generate_ics_content():
        dtstamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        # Локальные даты и времена по UTC+3
        local_start = tz_utc_plus_3.localize(datetime.datetime.combine(start_date, start_time))
        local_end = tz_utc_plus_3.localize(datetime.datetime.combine(end_date, end_time))

        # Конвертируем в UTC
        start_utc = local_start.astimezone(datetime.timezone.utc)
        end_utc = local_end.astimezone(datetime.timezone.utc)

        # Форматируем как строки для .ics
        dtstart = start_utc.strftime("%Y%m%dT%H%M%SZ")
        dtend = end_utc.strftime("%Y%m%dT%H%M%SZ")

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

    if st.button("Create and download .ics file"):
        ics_content = generate_ics_content()
        buf = io.BytesIO()
        buf.write(ics_content.encode())
        buf.seek(0)

        st.download_button(
            label="📥 Download event.ics",
            data=buf,
            file_name="event.ics",
            mime="text/calendar"
        )
