# DatabasePractice-2
- This is the Database Practice 02 for PKU 2025 spring-semester lesson Basis for Database.
- See also at 204265271@github. 

# DO NOT FORGET
- Remember to replace my database info with yours.

# Some Explanation for the Middle Phase
- In fact, MySQL does not have a delay constraint, but ***primary.py*** has already been written in MySQL, so I am too lazy to use PGSQL instead.
- So, let's simulate the delay constraint in MySQL: the method is to disable the foreign key constraint first, then insert the cross-referenced data, and finally restore the foreign key constraint.
- If it was PGSQL, you can use the standard BEGIN-COMMIT statement to write it.
- MySQL does not support CHECK between columns! God D**n it. So we need to use a trigger instead.

# Discovery 
- If an insertion is banned by the MySQL system, the primary key will get increased.
- Else it's discovered by myself, not. (Because I kill the inserting operation.)

# Some Explanation for Primary Phase with Middle Phase 
- Honestly speaking, I need to set ***dno INT(4) ZEROFILL*** in the Emp table to be ***NOT NULL***,
    however, due the the d**n feature of MySQL, I cannot set this otherwise the middle-1 test will never be finished!