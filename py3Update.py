import os
import re
import subprocess


def get_dependencies_from_code(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        dependencies = set(re.findall(r'^\s*from\s+(\w+)', content, re.MULTILINE) +
                           re.findall(r'^\s*import\s+(\w+)', content, re.MULTILINE))
    return dependencies


def check_dependency_compatibility(dependency):
    # Run pip check command to check compatibility for a specific dependency
    process = subprocess.Popen(
        ['pip', 'check', dependency], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error_output = process.communicate()

    # Check if there are any compatibility issues
    if error_output:
        return False, error_output.decode('utf-8').strip()
    else:
        return True, None


def update_code_to_python_3_10(directory):
    # Run 2to3 tool to update code to Python 3.10
    subprocess.call(['2to3', '-w', directory])


def main():
    directory = input("Enter directory path: ")

    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    log_file = os.path.join(directory, "compatibility_issues.log")
    with open(log_file, "w") as log:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    dependencies = get_dependencies_from_code(file_path)

                    for dependency in dependencies:
                        compatibility, error_msg = check_dependency_compatibility(
                            dependency)
                        if not compatibility:
                            log.write(
                                f"Project: {root}\nDependency: {dependency}\nError: {error_msg}\n\n")

    print("Dependency compatibility check complete.")
    update_code_to_python_3_10(directory)
    print("Code updated to Python 3.10 successfully.")


if __name__ == '__main__':
    main()
