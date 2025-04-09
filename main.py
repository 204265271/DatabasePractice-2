from primary import * 
from middle import *

if __name__ == "__main__":
    # Phase Reset
    print("\n ## RESET: delete and init ## \n")
    print("\n ## delete() ## \n")
    delete()
    print("\n ## init() ## \n")
    init()
    
    # Phase Primary
    print("\n ## test_foreign_key() ## \n")
    test_foreign_key()
    
    # Phase Middle
    print("\n ## test_deferred_constraints() ## \n")
    test_deferred_constraints()
    print("\n ## test_insert() ## \n")
    test_insert()
    
    # The final tables
    print("\n ## show_all() ## \n")
    show_all()