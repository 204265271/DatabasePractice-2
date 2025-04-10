import mysql.connector

# the table for Q3
def codemapping_init():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lzx25226",
            database="DBPractice02"
        )
        mycursor = mydb.cursor()

        # 创建 CodeMapping 表
        create_code_mapping_table = """
        CREATE TABLE IF NOT EXISTS CodeMapping (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(255) NOT NULL,
            value VARCHAR(255) NOT NULL,
            code VARCHAR(10) NOT NULL
        )
        """
        mycursor.execute(create_code_mapping_table)

        # 插入职位编码数据
        insert_code_mapping = """
        INSERT INTO CodeMapping (category, value, code)
        VALUES
            ('position', '教师', '01'),
            ('position', '教务', '02'),
            ('position', '会计', '03'),
            ('position', '秘书', '04')
        ON DUPLICATE KEY UPDATE code = VALUES(code)
        """
        mycursor.execute(insert_code_mapping)

        mydb.commit()
        print("对照表已成功创建")
    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")

# as for the reason why I use mySQL, see also at README
# for middle Q1
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

# for middle Q2
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
            
# for middle Q3 
def generate_smart_code(eno):
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lzx25226",
            database="DBPractice02"
        )
        mycursor = mydb.cursor()

        # 查询员工信息
        query = """
        SELECT e.eno, e.dno, YEAR(e.birthday), LPAD(e.level, 2, '0'), 
               d.manager, e.position
        FROM Emp e
        LEFT JOIN Dept d ON e.dno = d.dno
        WHERE e.eno = %s
        """
        mycursor.execute(query, (eno,))
        result = mycursor.fetchone()

        if result:
            # 提取查询结果
            eno, dno, birth_year, level, manager, position = result

            # 查询职位编码
            query_position_code = """
            SELECT code FROM CodeMapping
            WHERE category = 'position' AND value = %s
            """
            mycursor.execute(query_position_code, (position,))
            position_code_result = mycursor.fetchone()
            position_code = position_code_result[0] if position_code_result else "00"

            # 如果部门领导号为空，设置为 "0000"
            manager_code = str(manager).zfill(4) if manager else "0000"

            # 生成智能码
            smart_code = f"{str(eno).zfill(4)}{str(dno).zfill(4)}{birth_year}{level}{position_code}{manager_code}"
            return smart_code
        else:
            return f"员工号 {eno} 不存在"

    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
        return None
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")
            
def show_all_smart_code():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lzx25226",
            database="DBPractice02"
        )
        mycursor = mydb.cursor()

        # 查询所有员工号
        query_all_eno = "SELECT eno FROM Emp ORDER BY eno"
        mycursor.execute(query_all_eno)
        all_eno = mycursor.fetchall()

        if all_eno:
            print("所有员工的智能码如下：")
            for (eno,) in all_eno:
                # 调用 generate_smart_code 为每个员工生成智能码
                smart_code = generate_smart_code(eno)
                print(f"员工号 {eno}: {smart_code}")
        else:
            print("Emp 表中没有员工数据。")

    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")