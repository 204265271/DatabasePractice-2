import mysql.connector

# advanced - 1
def ensure_manager_salary_constraint():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lzx25226",
            database="DBPractice02"
        )
        mycursor = mydb.cursor()

        # 删除已有的触发器（如果存在）
        mycursor.execute("DROP TRIGGER IF EXISTS ensure_manager_salary")

        # 创建触发器
        create_trigger = """
        CREATE TRIGGER ensure_manager_salary
        BEFORE INSERT ON Emp
        FOR EACH ROW
        BEGIN
            DECLARE manager_salary DECIMAL(10, 2);

            -- 获取管理者的工资
            SELECT e.salary INTO manager_salary
            FROM Emp e, Dept d
            WHERE e.eno = d.manager
            and e.dno = NEW.dno
            and e.dno = d.dno;

            -- 如果管理者的工资不高于其管理的员工，抛出错误
            IF manager_salary <= NEW.salary THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Manager salary must be higher than any employee they manage';
            END IF;
        END;
        """
        mycursor.execute(create_trigger)

        print("触发器 ensure_manager_salary 已成功创建")
    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")
            
def test_manager_salary_constraint():
    ensure_manager_salary_constraint()

    # 测试插入数据
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lzx25226",
            database="DBPractice02"
        )
        mycursor = mydb.cursor()

        # 插入管理者工资低于员工的情况
        insert_emp = """
        INSERT INTO Emp (ename, birthday, level, position, salary, dno)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        emp_data = ("赵六", "1992-08-15", 5, "教师", 175000.0, 1)  # 管理者工资低于员工
        mycursor.execute(insert_emp, emp_data)
        mydb.commit()
        
        print("插入成功, 不符合预期")
    except mysql.connector.Error as err:
        print(f"插入失败, 符合预期: {err}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            
def test_manager_salary_constraint_2():
    ensure_manager_salary_constraint()

    # 测试插入数据
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lzx25226",
            database="DBPractice02"
        )
        mycursor = mydb.cursor()

        # 插入管理者工资高于员工的情况
        insert_emp = """
        INSERT INTO Emp (ename, birthday, level, position, salary, dno)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        emp_data = ("赵七", "1992-08-15", 5, "教师", 125000.0, 1)  # 管理者工资高于员工
        mycursor.execute(insert_emp, emp_data)
        mydb.commit()
        
        print("插入成功, 符合预期")
    except mysql.connector.Error as err:
        print(f"插入失败, 不符合预期: {err}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()