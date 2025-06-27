import psycopg2
import streamlit as st
import datetime

def connect():
    return psycopg2.connect(
        dbname='to_do_list',
        user='postgres',
        password='12345',
        host='localhost',
        port='5432'
    )

def add_tasks(id,title,description,due_data):
    conn= connect()
    cursor=conn.cursor()
    cursor.execute("""
                   insert into tasks (id,title,description,due_data)
                   values (%s,%s,%s,%s)
                   """,  (id,title, description, due_data))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("sucssefuly added")

def delete_tasks(title):
    conn= connect()
    cursor=conn.cursor()
    cursor.execute("""
                   delete from tasks 
                   where title= %s """, (title, ))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Successfully deleted")

def view_tasks():
    conn= connect()
    cursor=conn.cursor()
    cursor.execute("""
          select * from tasks """)
    #conn.commit()
    tasks= cursor.fetchall()
    
    cursor.close()
    conn.close()
    return tasks

def update_tasks(title,status):
    conn= connect()
    cursor=conn.cursor()
    cursor.execute("""
          update tasks 
          set status = %s
          where title = %s""", (status,title))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Task updated successfully!")


st.title("📋 My To-Do App")
search_task= st.text_input("search a task by title")

if search_task:
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(""" select * from tasks where title ilike %s""",('%'+search_task+'%',))
    result= cursor.fetchall()
    cursor.close()
    conn.close()
    if result:
        st.subheader("search result :")
        st.table(result)
    else:
        st.warning("no found tasks")

st.expander('add new task')
with st.form('add form'):
    id=st.number_input('id task')
    title= st.text_input('task title')
    description= st.text_input("task description")
    due_data= st.date_input('due date',min_value=datetime.date.today())
    add_button= st.form_submit_button('add task')
    if add_button:
        add_tasks(id,title,description,due_data)

st.expander("delete task")
with st.form("delete form"):
    title= st.text_input('task title')
    delete_button= st.form_submit_button('delete task')
    if delete_button:
        delete_tasks(title)
        
st.expander('update task')
with st.form('update form'):
    title= st.text_input("task title")
    status = st.selectbox("select task status",['done','in_progress','not_done'])
    update_button= st.form_submit_button('update task')
    if update_button:
        update_tasks(title,status)

st.expander('view tasks')
tasks= view_tasks()
if tasks:
    st.dataframe(tasks)
else:
    st.info('no tasks found')

tasks= view_tasks()
count_done= sum(1 for task in tasks if task[4]== 'done')
count_in_progress= sum(1 for task in tasks if task[4] == 'in_progress')

col1, col2, col3 = st.columns(3)
col1.metric("✅ Done", count_done)
col2.metric("🚧 In Progress", count_in_progress)
col3.metric("📌 Total Tasks", len(tasks))
