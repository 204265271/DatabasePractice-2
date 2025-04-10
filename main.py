import primary 
import middle
import advanced

if __name__ == "__main__":
    # Phase Reset
    print("\n ## RESET: delete and init ##")
    print("\n ## delete() ## \n")
    primary.delete()
    print("\n ## init() ## \n")
    primary.init()
    print("\n ## advanced-2 ## setting ensure_budget_consistency() ## \n")
    advanced.ensure_budget_consistency()
    
    # Phase Primary
    print("\n ## primary ## test_foreign_key() ## \n")
    primary.test_foreign_key()
    
    # Phase Middle
    print("\n ## middle-1 ## test_deferred_constraints() ## \n")
    middle.test_deferred_constraints()
    print("\n ## middle-2 ## test_insert() ## \n")
    middle.test_insert()
    print("\n ## middle-3 ## show_all_smart_code() ## \n")
    middle.codemapping_init()
    middle.show_all_smart_code()
    
    # Phase Advanced
    print("\n ## advanced-1 ## test_manager_salary_constraint() and test_manager_salary_constraint_2() ## \n")
    advanced.test_manager_salary_constraint()
    advanced.test_manager_salary_constraint_2()
    print("\n ## advanced-2 ## after setting ensure_budget_consistency() from beginning ## show_all() ## \n")
    primary.show_all()