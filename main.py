import primary 
import middle

if __name__ == "__main__":
    # Phase Reset
    print("\n ## RESET: delete and init ##")
    print("\n ## delete() ## \n")
    primary.delete()
    print("\n ## init() ## \n")
    primary.init()
    
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
    
    # The final tables
    print("\n ## show_all() ## \n")
    primary.show_all()