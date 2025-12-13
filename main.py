import random
from faker import Faker
import pandas as pd
import sqlite3
import re

# ========================================== #
# -------------- จำลองข้อมูลดิบ -------------- #
# ========================================== #

def generate_bad_data():
    random.seed(67)
    fake = Faker()
    data = []

    for i in range(300):
        studentID = 1000 + i
        f_name = fake.first_name()
        l_name = fake.last_name()
        email = f"{studentID}@student.chulaherb.ac.th"
        phone = f"0{random.randint(60,99)}{random.randint(1000000,9999999)}"
        dob = fake.date_of_birth(minimum_age=18, maximum_age=40)
        is_verified = 'Unverified'
        
        # จงใจใส่ข้อมูลเสีย
        if random.random() < 0.2: f_name = f" {f_name}" 
        if random.random() < 0.1: email = email.replace('@student.chulaherb.ac.th' , '@gmail.com')
        if random.random() < 0.3: phone = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        if random.random() < 0.05: dob = dob.replace(year=2099)

        data.append({
            'studentID' : studentID , 
            'f_name' : f_name , 
            'l_name' : l_name , 
            'email' : email , 
            'phone' : phone , 
            'dob' : dob , 
            'status' : is_verified
        })

        # จำลองข้อมูลซ้ำ 
        if random.random() < 0.1: 
          data.append({
            'studentID' : studentID , 
            'f_name' : f_name , 
            'l_name' : l_name , 
            'email' : email , 
            'phone' : phone , 
            'dob' : dob , 
            'status' : is_verified
           })
          
    return pd.DataFrame(data)

# เชื่อมต่อ Database
conn = sqlite3.connect('data_pipeline.db')

df_bad_data = generate_bad_data()

df_bad_data.to_sql('bad_data_table' , conn , if_exists = 'replace' , index = False)

# ==========================================#
# ---------------- การล้างข้อมูล ------------- #
# ==========================================#

# ใช้ .copy() เพื่อไม่ให้ค่าใน df_bad_data เปลี่ยนตาม
df_bronze_data = df_bad_data.copy()

df_bronze_data['f_name'] = df_bronze_data['f_name'].str.strip().str.capitalize()
df_bronze_data['l_name'] = df_bronze_data['l_name'].str.strip().str.capitalize()
df_bronze_data['phone'] = df_bronze_data['phone'].apply(lambda x: re.sub(r'\D', '', str(x)))

df_bronze_data.to_sql('bronze_table' , conn , if_exists='replace' , index = False)

sql_silver = """
CREATE TABLE IF NOT EXISTS silver_table AS
WITH deduplicated AS (
    -- 1. จัดการคนสมัครซ้ำ
    SELECT *, 
           ROW_NUMBER() OVER(PARTITION BY studentID ORDER BY studentID) as row_num
    FROM bronze_table
)
-- 2. ใช้ Logic ตัดสินว่าใครจะได้สถานะอะไร
SELECT 
    studentID, 
    f_name, 
    l_name, 
    email, 
    phone, 
    dob, 
    CASE 
        WHEN dob < '2025-01-01' 
             AND email LIKE '%@student.chulaherb.ac.th' 
             THEN 'Verified'  -- ถ้าผ่านทุกเงื่อนไข ให้เป็น Verified
        ELSE 'Unverified'     -- ถ้าไม่ผ่านอย่างใดอย่างหนึ่ง ให้เป็น Unverified
    END as status
FROM deduplicated
WHERE row_num = 1; -- เรายังคัดคนซ้ำออก (เพราะ 1 ID ควรมีแค่ 1 แถว) แต่เก็บคนข้อมูลเสียไว้
"""

# รันคำสั่ง SQL
conn.execute("DROP TABLE IF EXISTS silver_table")
conn.execute(sql_silver)

# --- สรุปผล---
print('-' * 50)
df_res = pd.read_sql("SELECT status, COUNT(*) as count FROM silver_table GROUP BY status", conn)
print(df_res)