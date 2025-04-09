import mysql.connector

# as for the reason why I use mySQL, see also at README
def test_deferred_constraints():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lzx25226",
            database="DBPractice02"
        )
        mycursor = mydb.cursor()

        # 禁用外键约束
        mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        print("外键约束已禁用")

        # 插入互相参照的数据
        try:
            # 插入 Emp 数据，暂时将 dno 设置为 NULL
            insert_emp = """
                INSERT INTO Emp (ename, birthday, level, position, salary, dno)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            emp_data = ("李四", "1995-05-05", 2, "教师", 8000.00, None)
            mycursor.execute(insert_emp, emp_data)
            eno = mycursor.lastrowid

            # 插入 Dept 数据，manager 设置为刚插入的 Emp 的 eno
            insert_dept = """
                INSERT INTO Dept (dname, budget, manager)
                VALUES (%s, %s, %s)
            """
            dept_data = ("智能学院", 150000.00, eno)
            mycursor.execute(insert_dept, dept_data)
            dno = mycursor.lastrowid

            # 更新 Emp 的 dno 字段为刚插入的 Dept 的 dno
            update_emp = """
                UPDATE Emp
                SET dno = %s
                WHERE eno = %s
            """
            mycursor.execute(update_emp, (dno, eno))

            mydb.commit()
            print("互相参照的数据插入成功")
        except mysql.connector.Error as err:
            print(f"插入数据失败: {err}")
            mydb.rollback()

        # 启用外键约束
        mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        print("外键约束已启用")

    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")

def test_insert():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lzx25226",
            database="DBPractice02"
        )
        mycursor = mydb.cursor()

        # 插入符合约束的数据
        insert_emp = """
        INSERT INTO Emp (ename, birthday, level, position, salary, dno)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valid_emp_data = ("王五", "1990-01-01", 3, "教师", 15000.00, 1)
        mycursor.execute(insert_emp, valid_emp_data)
        print("插入符合约束的数据成功")

        # 插入不符合约束的数据
        invalid_emp_data = ("刘六", "1995-05-05", 2, "教师", 15000.00, 1)
        try:
            mycursor.execute(insert_emp, invalid_emp_data)
            print("插入不符合约束的数据成功")
        except mysql.connector.Error as err:
            print(f"插入不符合约束的数据失败: {err}")

        mydb.commit()
    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")