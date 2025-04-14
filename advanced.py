import mysql.connector
from primary import config_with_db

# advanced - 1
def ensure_manager_salary_constraint():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(**config_with_db)
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
        mydb = mysql.connector.connect(**config_with_db)
        mycursor = mydb.cursor()

        # 插入管理者工资低于员工的情况
        insert_emp = """
        INSERT INTO Emp (ename, birthday, level, position, salary, dno)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        emp_data = ("Henry", "1992-08-15", 5, "教师", 175000.0, 1)  # 管理者工资低于员工
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
        mydb = mysql.connector.connect(**config_with_db)
        mycursor = mydb.cursor()

        # 插入管理者工资高于员工的情况
        insert_emp = """
        INSERT INTO Emp (ename, birthday, level, position, salary, dno)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        emp_data = ("Isaac", "1992-08-15", 5, "教师", 125000.0, 1)  # 管理者工资高于员工
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
            
# advanced-2
def ensure_budget_consistency():
    try:
        # 连接到 MySQL 数据库
        mydb = mysql.connector.connect(**config_with_db)
        mycursor = mydb.cursor()

        # 删除已有的触发器（如果存在）
        mycursor.execute("DROP TRIGGER IF EXISTS deduct_budget_on_employee_insert")
        mycursor.execute("DROP TRIGGER IF EXISTS update_budget_on_employee_update")
        mycursor.execute("DROP TRIGGER IF EXISTS restore_budget_on_employee_delete")

        # 创建 BEFORE INSERT 触发器
        create_insert_trigger = """
        CREATE TRIGGER deduct_budget_on_employee_insert
        BEFORE INSERT ON Emp
        FOR EACH ROW
        BEGIN
            DECLARE dept_budget DECIMAL(10, 2);

            -- 获取部门的当前预算
            SELECT budget INTO dept_budget
            FROM Dept
            WHERE dno = NEW.dno;

            -- 如果部门预算不足以支付员工工资，抛出错误
            IF dept_budget < NEW.salary THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Department budget is insufficient to cover the new employee salary';
            END IF;

            -- 扣除员工工资
            UPDATE Dept
            SET budget = budget - NEW.salary
            WHERE dno = NEW.dno;
        END;
        """
        mycursor.execute(create_insert_trigger)

        # 创建 BEFORE UPDATE 触发器
        create_update_trigger = """
        CREATE TRIGGER update_budget_on_employee_update
        BEFORE UPDATE ON Emp
        FOR EACH ROW
        BEGIN
            DECLARE old_dept_budget DECIMAL(10, 2);
            DECLARE new_dept_budget DECIMAL(10, 2);

            -- 如果员工的工资发生变化，调整原部门的预算
            IF OLD.salary != NEW.salary THEN
                SELECT budget INTO old_dept_budget
                FROM Dept
                WHERE dno = OLD.dno;

                -- 如果原部门预算不足以支付工资变化，抛出错误
                IF old_dept_budget + OLD.salary < NEW.salary THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Department budget is insufficient to cover the updated employee salary';
                END IF;

                -- 调整原部门预算
                UPDATE Dept
                SET budget = budget + OLD.salary - NEW.salary
                WHERE dno = OLD.dno;
            END IF;

            -- 如果员工的部门发生变化，调整原部门和新部门的预算
            IF OLD.dno != NEW.dno THEN
                -- 恢复原部门预算
                UPDATE Dept
                SET budget = budget + OLD.salary
                WHERE dno = OLD.dno;

                -- 扣除新部门预算
                SELECT budget INTO new_dept_budget
                FROM Dept
                WHERE dno = NEW.dno;

                -- 如果新部门预算不足以支付员工工资，抛出错误
                IF new_dept_budget < NEW.salary THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'New department budget is insufficient to cover the employee salary';
                END IF;

                UPDATE Dept
                SET budget = budget - NEW.salary
                WHERE dno = NEW.dno;
            END IF;
            
            IF OLD.dno IS NULL and NEW.dno IS NOT NULL THEN
                -- 扣除新部门预算
                SELECT budget INTO new_dept_budget
                FROM Dept
                WHERE dno = NEW.dno;

                -- 如果新部门预算不足以支付员工工资，抛出错误
                IF new_dept_budget < NEW.salary THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'New department budget is insufficient to cover the employee salary';
                END IF;

                UPDATE Dept
                SET budget = budget - NEW.salary
                WHERE dno = NEW.dno;
            END IF;
        END;
        """
        mycursor.execute(create_update_trigger)

        # 创建 BEFORE DELETE 触发器
        create_delete_trigger = """
        CREATE TRIGGER restore_budget_on_employee_delete
        BEFORE DELETE ON Emp
        FOR EACH ROW
        BEGIN
            -- 恢复员工所在部门的预算
            UPDATE Dept
            SET budget = budget + OLD.salary
            WHERE dno = OLD.dno;
        END;
        """
        mycursor.execute(create_delete_trigger)

        print("触发器 deduct_budget_on_employee_insert, update_budget_on_employee_update 和 restore_budget_on_employee_delete 已成功创建")
    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()
            print("数据库连接已关闭")
    