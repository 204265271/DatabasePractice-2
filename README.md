# DatabasePractice-2
- This is the Database Practice 02 for PKU 2025 spring-semester lesson Basis for Database.
- See also at 204265271@github. 

# Some Explanation for the Middle Phase
- In fact, MySQL does not have a delay constraint, but ***primary.py*** has already been written in MySQL, so I am too lazy to use PGSQL instead.
- So, let's simulate the delay constraint in MySQL: the method is to disable the foreign key constraint first, then insert the cross-referenced data, and finally restore the foreign key constraint.
- If it was PGSQL, you can use the standard BEGIN-COMMIT statement to write it.
- MySQL does not support CHECK between columns! God D**n it. So we need to use a trigger instead.