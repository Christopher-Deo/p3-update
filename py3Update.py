import os
import re
import subprocess
import logging
import shutil

def get_dependencies_from_code(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        dependencies = set(re.findall(r'^\s*from\s+(\w+)', content, re.MULTILINE) +
                           re.findall(r'^\s*import\s+(\w+)', content, re.MULTILINE))
    return dependencies

def check_dependency_compatibility(dependency):
    # Run pip check command to check compatibility for a specific dependency
    process = subprocess.Popen(['pip', 'check', dependency], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error_output = process.communicate()

    # Check if there are any compatibility issues
    if error_output:
        return False, error_output.decode('utf-8').strip()
    else:
        return True, None

def update_code_to_python_3_10(directory):
    # Run 2to3 tool to update code to Python 3.10
    subprocess.call(['2to3', '-w', directory])

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def create_backup_directory(project_directory):
    backup_directory = os.path.join(project_directory, "Backups")
    os.makedirs(backup_directory, exist_ok=True)
    readme_file = os.path.join(backup_directory, "README.txt")
    with open(readme_file, "w") as readme:
        readme.write("This project has been updated from Python 2.x to Python 3.10.\n")
        readme.write("To restore the project files to their original condition:\n")
        readme.write("1. Replace the .bak extension with .py for each file.\n")
        readme.write("2. Build the project using the appropriate build command.\n")
    return backup_directory

def main():
    directory = r"c:\users\deoc\Coding-Projects\Python\python-scripts"

    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    log_file = os.path.join(directory, "compatibility_issues.log")
    setup_logging(log_file)
    logger = logging.getLogger(__name__)

    logger.info("Scanning code for dependencies and checking compatibility...")

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                dependencies = get_dependencies_from_code(file_path)

                for dependency in dependencies:
                    compatibility, error_msg = check_dependency_compatibility(dependency)
                    if not compatibility:
                        logger.warning("Compatibility issue detected:")
                        logger.warning(f"Project: {root}")
                        logger.warning(f"Dependency: {dependency}")
                        logger.warning(f"Error: {error_msg}")
                        logger.warning("")

    logger.info("Dependency compatibility check complete.")
    update_code_to_python_3_10(directory)
    logger.info("Code updated to Python 3.10 successfully.")

    for root, _, _ in os.walk(directory):
        backup_directory = create_backup_directory(root)
        for file in os.listdir(root):
            if file.endswith(".bak"):
                bak_file_path = os.path.join(root, file)
                py_file_path = os.path.join(root, file[:-4] + ".py")
                shutil.move(bak_file_path, py_file_path)

    logger.info("Backup directories created and files restored.")

if __name__ == '__main__':
    main()
