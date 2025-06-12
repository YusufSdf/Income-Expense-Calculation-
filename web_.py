import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import datetime # datetime modülünü ekledim, tarih çevrimi için gerekli
import os
from dotenv import load_dotenv

@st.cache_resource
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets.connections.mysql.host,
        user=st.secrets.connections.mysql.username, # Burada username olarak tanımladık
        password=st.secrets.connections.mysql.password, # Burada password olarak tanımladık
        database=st.secrets.connections.mysql.database,
        charset=st.secrets.connections.mysql.query.charset # Charset'i de buradan çekiyoruz
    )
db = get_db_connection()
cursor = db.cursor()

st.title("Income Expense Calculation")
col1, col2 , col3 = st.columns(3)
income_ = st.text_input("Write income")
expense_ = st.text_input("Write expense")
date_ = st.date_input("Select date") # Bu bir datetime.date objesi
save_button = st.button("Save")
delete_button = st.button("Delete")

with col1:
    bring = st.button("Get Information For Selected Date")
with col2:
    bring_all = st.button("Get Information For All Date")
with col3:
    show_picture = st.button("Show Data Picture")

sql_upsert_income = """
INSERT INTO income (income_, date)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE income_ = income_ + VALUES(income_);
"""

sql_add = "INSERT INTO income (income_ , date) VALUES (%s,%s)"
sql_del = "DELETE FROM income WHERE date= %s"


# Session state başlangıç değerleri
if "last_income" not in st.session_state:
    st.session_state.last_income = ""
if "last_date" not in st.session_state: # Bu kontrol de gerekli
    st.session_state.last_date = None # date_input'ın varsayılan değeri olabileceği için None uygun

if save_button == True:
    st.session_state.last_income = income_
    st.session_state.last_date = date_
    st.session_state.last_date = expense_

    if income_ and date_: # Miktar ve tarih boş değilse işlemi yap
        try:
            # Gelen string geliri sayıya çevir
            amount_in = float(income_)
            amount_ex = float(expense_)
            amount_float = amount_in - amount_ex
            # Tarih objesini 'YYYY-MM-DD' formatında string'e çevir
            date_str_formatted = date_.strftime('%Y-%m-%d')

            # UPSERT sorgusu için değerleri tuple olarak hazırla
            val_upsert = (amount_float, date_str_formatted)
            cursor.execute(sql_upsert_income, val_upsert)
            db.commit()
            st.success(f"{amount_float} TL net income was successfully added/updated as {date_str_formatted}!")

        except ValueError:
            st.error("Please enter a valid numerical amount (ex: 1000.50)")
        except mysql.connector.Error as err:
            st.error(f"An error occurred during a database operation: {err}")
    else:
        st.warning("Please fill in the income amount and date.")


if delete_button == True:
    if date_: # Tarih seçili mi kontrol et
        try:
            date_to_delete_str = date_.strftime('%Y-%m-%d')
            val_for_delete = (date_to_delete_str,)
            cursor.execute(sql_del, val_for_delete)
            db.commit()
            st.success(f" Records from date {date_to_delete_str} have been deleted!")
        except mysql.connector.Error as err:
            st.error(f"An error occurred while deleting the record: {err}")
    else:
        st.warning("You must select the date you want to delete.")

if bring == True:
    date_str_formatted = date_.strftime('%Y-%m-%d')
    sql_select_by_date = "SELECT income_, date FROM income WHERE date = %s" 
    val_select = (date_str_formatted,)
    cursor.execute(sql_select_by_date, val_select)
    result = cursor.fetchone()
    st.write(result)

elif bring_all == True:
    cursor.execute("SELECT income_, date FROM income WHERE date")
    result = cursor.fetchall()
    res = pd.DataFrame(result,columns=["net income","date"])
    st.dataframe(res)

elif show_picture == True:
    cursor.execute("SELECT income_, date FROM income WHERE date")
    result = cursor.fetchall()
    res = pd.DataFrame(result,columns=["Net income","Date"])
# >>> BURADA ÇUBUK GRAFİĞİNİ OLUŞTURUYORUZ <<<
    fig, ax = plt.subplots() # Bir figure ve axes objesi oluştur
    ax.bar(res['Date'], res['Net income']) # Çubuk grafiği çiz
    ax.set_xlabel("Date") # X ekseni etiketi
    ax.set_ylabel("Totel income (TL)") # Y ekseni etiketi
    ax.set_title("Daily Total Revenues") # Grafik başlığı
    plt.xticks(rotation=45, ha='right') # Tarih etiketlerini döndür
    plt.tight_layout() # Etiketlerin kesilmesini engeller
# >>> Streamlit'te GRAFİĞİ GÖSTERİYORUZ <<<
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig) #figure objesini st.pyplot() içine ver



db.close()