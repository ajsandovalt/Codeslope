from functions.get_file_content import get_file_content

def main():
    print(f'''

====== Results lorem.txt
{get_file_content("calculator", "lorem.txt")}

====== Results main.py
{get_file_content("calculator", "main.py")}

====== Results pkg/calculator.py
{get_file_content("calculator", "pkg/calculator.py")}

====== Results /bin/cat
{get_file_content("calculator", "/bin/cat") }

====== Results pkg/does_not_exist.py
{get_file_content("calculator", "pkg/does_not_exist.py")}

''')
    pass

if __name__ == "__main__":
    main()