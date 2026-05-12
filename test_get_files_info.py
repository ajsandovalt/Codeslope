from functions.get_files_info import get_files_info

def main():
    
    
    print("Starting tests!")

    print(f"""
Result for current directory:
          
{get_files_info("calculator", ".")}

Result for 'pkg' directory:

{get_files_info("calculator", "pkg")}

Result for '/bin' directory:

{get_files_info("calculator", "/bin")}

Result for '../' directory:

{get_files_info("calculator", "../")}

    """)

    print("Test finished!")


if __name__ == "__main__":
    main()