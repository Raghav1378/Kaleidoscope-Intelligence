import sqlite3
import random
from faker import Faker

# Initialize Faker for generating real-looking names
fake = Faker()

# Connect to database
connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# ---------------------------------------------------------
# 1. SETUP TABLES
# ---------------------------------------------------------

# Drop tables if they exist (to reset everything cleanly)
cursor.execute("DROP TABLE IF EXISTS STUDENT")
cursor.execute("DROP TABLE IF EXISTS COURSES")

# Create STUDENT Table
cursor.execute("""
CREATE TABLE STUDENT(
    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
    NAME VARCHAR(50), 
    CLASS VARCHAR(25), 
    SECTION VARCHAR(5), 
    MARKS INT,
    ATTENDANCE_PCT INT
);
""")

# Create COURSES Table (To show joins later if needed)
cursor.execute("""
CREATE TABLE COURSES(
    COURSE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    COURSE_NAME VARCHAR(50),
    INSTRUCTOR VARCHAR(50)
);
""")

# ---------------------------------------------------------
# 2. GENERATE DATA
# ---------------------------------------------------------

print("🚀 Generating data... this might take a second.")

# Define some realistic options
classes = ['Data Science', 'DevOps', 'Web Development', 'Machine Learning', 'Cyber Security']
sections = ['A', 'B', 'C']
instructors = ['Prof. Snape', 'Dr. Strange', 'Tony Stark', 'Bruce Wayne', 'Gandalf']

# Insert 5 Courses
for i, subject in enumerate(classes):
    cursor.execute("INSERT INTO COURSES (COURSE_NAME, INSTRUCTOR) VALUES (?, ?)", 
                   (subject, instructors[i]))

# Insert 100 Students (You can change 100 to 1000 if you want)
students_data = []
for _ in range(100):
    name = fake.name()
    cls = random.choice(classes)
    sec = random.choice(sections)
    marks = random.randint(30, 100) # Marks between 30 and 100
    attendance = random.randint(50, 100) # Attendance %
    
    students_data.append((name, cls, sec, marks, attendance))

cursor.executemany("""
    INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, ATTENDANCE_PCT) 
    VALUES (?, ?, ?, ?, ?)
""", students_data)

# Add your Custom Characters manually so they are always there
custom_data = [
    ('Raghav', 'Data Science', 'A', 95, 100),
    ('Itachi', 'Data Science', 'B', 100, 0), # Itachi skips class
    ('Naruto', 'DevOps', 'A', 35, 60),
    ('Sasuke', 'Data Science', 'A', 88, 90)
]
cursor.executemany("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, ATTENDANCE_PCT) VALUES (?, ?, ?, ?, ?)", custom_data)

# ---------------------------------------------------------
# 3. SAVE & CLOSE
# ---------------------------------------------------------
connection.commit()
connection.close()
print(f"✅ Database populated with {len(students_data) + len(custom_data)} students and 5 courses!")