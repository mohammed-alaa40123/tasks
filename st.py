from sql_connect import *
import task1,task2,task3,task4,task5,task6,task7,task8,task9,task10

Task = st.sidebar.selectbox("Select a Task", ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5",
                                           "Task 6", "Task 7", "Task 8", "Task 9", "Task 10"])


if Task == "Task 1":
    task1.task1()
elif Task == "Task 2":
    task2.task2()   
elif Task == "Task 3":
    task3.task3()
elif Task == "Task 4":
    task4.task4()
elif Task == "Task 5":
    task5.task5()
elif Task == "Task 6":
    task6.task6()
elif Task == "Task 7":
    task7.task7()
elif Task == "Task 8":
    task8.task8()
elif Task == "Task 9":
    task9.task9()
elif Task == "Task 10":
    task10.task10()