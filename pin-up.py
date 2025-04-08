import streamlit as st
import datetime

st.title("📅 Генератор .ics")

# Ввод данных пользователем
summary = st.text_input("Название события")
description = st.text_area("Описание")
location = st.text_input("Локация")
event_url = st.text_input("Ссылка на событие")
start_date = st.date_input("Дата начала")
start_time = st.time_input("Время начала", value=datetime.time(14, 0))
end_date = st.date_input("Дата окончания")
end_time = st.time_input("Время окончания", value=datetime.time(23, 59))
alarm_minutes = st.number_input("За сколько минут напомнить", min_value=0, step=5, value=60)

# Проверка корректности введенных дат и времени
if datetime.datetime.combine(end_date, end_time) <= datetime.datetime.combine(start_date, start_time):
    st.error("❌ Время окончания должно быть позже времени начала.")
else:
    # Генерация содержимого .ics файла
    dtstamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
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

    # Кнопка для скачивания .ics файла
    st.download_button(
        label="📥 Скачать .ics файл",
        data=ics_content,
        file_name="event.ics",
        mime="text/calendar"
    )
