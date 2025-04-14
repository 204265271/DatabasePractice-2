import mysql.connector

# change it to your own database config
config = {
    "username": "root", 
    "password": "Lzx25226",
    "host":     "localhost", 
}

config_with_db = {
    "username": "root", 
    "password": "Lzx25226",
    "host":     "localhost", 
    "database": "DBPractice02"
}

def init():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(**config)
        mycursor = mydb.cursor()

        # 创建数据库
        mycursor.execute("CREATE DATABASE IF NOT EXISTS DBPractice02")
        mycursor.execute("USE DBPractice02")

        # 创建 Dept 表
        create_dept_table = """
        CREATE TABLE IF NOT EXISTS Dept (
            dno INT(4) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
            dname ENUM('数学学院', '计算机学院', '智能学院', '电子学院', '元培学院'),
            budget DECIMAL(10, 2),
            manager INT(4) ZEROFILL DEFAULT NULL
        )
        """
        mycursor.execute(create_dept_table)

        # 创建 Emp 表（不使用 CHECK 约束）
        create_emp_table = """
        CREATE TABLE IF NOT EXISTS Emp (
            eno INT(4) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
            ename VARCHAR(255),
            birthday DATE,
            level INT DEFAULT 3,
            position ENUM('教师', '教务', '会计', '秘书'),
            salary DECIMAL(10, 2),
            dno INT(4) ZEROFILL,
            FOREIGN KEY (dno) REFERENCES Dept(dno)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
        """
        mycursor.execute(create_emp_table)

        # 创建触发器，验证 salary 和 level 的对应关系
        create_trigger = """
        CREATE TRIGGER validate_salary_level
        BEFORE INSERT ON Emp
        FOR EACH ROW
        BEGIN
            IF (NEW.level = 1 AND (NEW.salary < 2000 OR NEW.salary > 5000)) OR
               (NEW.level = 2 AND (NEW.salary < 5001 OR NEW.salary > 10000)) OR
               (NEW.level = 3 AND (NEW.salary < 10001 OR NEW.salary > 20000)) OR
               (NEW.level = 4 AND (NEW.salary < 20001 OR NEW.salary > 50000)) OR
               (NEW.level = 5 AND (NEW.salary < 50001 OR NEW.salary > 200000)) THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Salary does not match the level constraint';
            END IF;
        END;
        """
        mycursor.execute("DROP TRIGGER IF EXISTS validate_salary_level")
        mycursor.execute(create_trigger)

        # 添加外键约束到 Dept 表
        add_foreign_key = """
        ALTER TABLE Dept
        ADD CONSTRAINT fk_manager
        FOREIGN KEY (manager) REFERENCES Emp(eno)
            ON DELETE SET NULL
            ON UPDATE CASCADE
        """
        mycursor.execute(add_foreign_key)
        
    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")
    

def test_foreign_key():
    mydb = mysql.connector.connect(**config_with_db)
    mycursor = mydb.cursor()
    
    # 插入数据
    try:
        # 插入 Dept 数据
        insert_dept = "INSERT INTO Dept (dname, budget) VALUES (%s, %s)"
        dept_data = ("计算机学院", 1000000.00)
        mycursor.execute(insert_dept, dept_data)
        dno = mycursor.lastrowid

        # 插入 Emp 数据
        insert_emp = "INSERT INTO Emp (ename, birthday, level, position, salary, dno) VALUES (%s, %s, %s, %s, %s, %s)"
        emp_data = ("Adam", "2000-01-01", 1, "教师", 5000.00, dno)
        mycursor.execute(insert_emp, emp_data)
        insert_emp = "INSERT INTO Emp (ename, birthday, level, position, salary, dno) VALUES (%s, %s, %s, %s, %s, %s)"
        emp_data = ("Benjamin", "1977-05-10", 5, "教师", 150000.00, dno)
        mycursor.execute(insert_emp, emp_data)
        eno = mycursor.lastrowid

        # 更新 Dept 的 manager 字段
        update_dept_manager = "UPDATE Dept SET manager = %s WHERE dno = %s"
        mycursor.execute(update_dept_manager, (eno, dno))

        mydb.commit()
        print("插入有效数据成功")
    except mysql.connector.Error as err:
        print(f"插入数据失败: {err}")
        mydb.rollback()

    # 测试无效外键数据
    try:
        insert_emp = "INSERT INTO Emp (ename, birthday, level, position, salary, dno) VALUES (%s, %s, %s, %s, %s, %s)"
        invalid_emp_data = ("Christopher", "2001-02-02", 2, "教务", 6000.00, 9999)
        mycursor.execute(insert_emp, invalid_emp_data)
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"插入无效外键数据失败，符合预期: {err}")

    # 更新外键数据
    try:
        insert_new_dept = "INSERT INTO Dept (dname, budget) VALUES (%s, %s)"
        new_dept_data = ("数学学院", 500000.00)
        mycursor.execute(insert_new_dept, new_dept_data)
        new_dno = mycursor.lastrowid

        update_emp = "UPDATE Emp SET dno = %s WHERE eno = %s"
        update_data = (new_dno, 1)
        mycursor.execute(update_emp, update_data)
        
        # 更新 Dept 的 manager 字段
        update_dept_manager = "UPDATE Dept SET manager = %s WHERE dno = %s"
        mycursor.execute(update_dept_manager, (eno, new_dno))
        mydb.commit()
        print("更新外键数据成功")
    except mysql.connector.Error as err:
        print(f"更新外键数据失败: {err}")
        mydb.rollback()

    # 关闭数据库连接
    finally:
        mycursor.close()
        mydb.close()
        
def delete():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(**config)
        mycursor = mydb.cursor()

        # 切换到目标数据库
        mycursor.execute("CREATE DATABASE IF NOT EXISTS DBPractice02")
        mycursor.execute("USE DBPractice02")

        # 删除外键约束
        try:
            drop_foreign_key = "ALTER TABLE Dept DROP FOREIGN KEY fk_manager"
            mycursor.execute(drop_foreign_key)
            print("外键约束 fk_manager 删除成功")
        except mysql.connector.Error as err:
            print(f"删除外键约束失败: {err}")

        # 删除表的顺序：先删除 Emp 表，再删除 Dept 表, 最后删除 CodeMapping 表
        try:
            drop_emp_table = "DROP TABLE IF EXISTS Emp"
            mycursor.execute(drop_emp_table)
            print("Emp 表删除成功")
        except mysql.connector.Error as err:
            print(f"删除 Emp 表失败: {err}")

        try:
            drop_dept_table = "DROP TABLE IF EXISTS Dept"
            mycursor.execute(drop_dept_table)
            print("Dept 表删除成功")
        except mysql.connector.Error as err:
            print(f"删除 Dept 表失败: {err}")
            
        try:
            drop_CodeMapping_table = "DROP TABLE IF EXISTS CodeMapping"
            mycursor.execute(drop_CodeMapping_table)
            print("CodeMapping 表删除成功")
        except mysql.connector.Error as err:
            print(f"删除 CodeMapping 表失败: {err}")

        # 提交更改
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
        mydb.rollback()
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")
            
def show_all():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(**config_with_db)
        mycursor = mydb.cursor()

        # 查询 Dept 表中的所有数据
        print("Dept 表中的数据:")
        mycursor.execute("SELECT * FROM Dept")
        dept_results = mycursor.fetchall()
        for row in dept_results:
            print(row)

        print("\nEmp 表中的数据:")
        # 查询 Emp 表中的所有数据
        mycursor.execute("SELECT * FROM Emp")
        emp_results = mycursor.fetchall()
        for row in emp_results:
            print(row)

    except mysql.connector.Error as err:
        print(f"查询数据失败: {err}")
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")