import os
import subprocess

# Step 1: Backup Your Code


def backup_code(code_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    for root, dirs, files in os.walk(code_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                backup_path = os.path.join(backup_dir, file)
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                shutil.copy2(file_path, backup_path)

# Step 2: Scan Dependencies


def scan_dependencies(code_dir):
    process = subprocess.Popen(
        ['pipdeptree', '-f', code_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode())

# Step 3: Review Python 2 to 3 Changes (Manual Step)

# Step 4: Modify Your Code


def modify_code(code_dir):
    for root, dirs, files in os.walk(code_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                subprocess.run(['2to3', '-w', file_path])
                subprocess.run(['futurize', '-w', file_path])
                subprocess.run(['modernize', '-w', file_path])

# Step 5: Test Your Code (Manual Step)

# Step 6: Update Dependencies (Manual Step)


# Directory paths
code_dir = 'C://Users/deoc/Coding-Projects/Python/Python-Scripts'
backup_dir = 'C://Users/deoc/Coding-Projects/Python/Python-Scripts-Backup'

# Step 1: Backup Your Code
backup_code(code_dir, backup_dir)

# Step 2: Scan Dependencies
scan_dependencies(code_dir)

# Step 4: Modify Your Code
modify_code(code_dir)

# Step 5: Test Your Code (Manual Step)

# Step 6: Update Dependencies (Manual Step)
