import subprocess
import os

def run_2to3(directory):
    #Walk through the directory and it's subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)

                #Perform the conversion using 2to3
                subprocess.run(["2to3", "-w","-W", "-o", root, file_path])
                print(f"Updated: {file_path}")


def main():
    # Path to the local Git directory
    git_directory = "Macintosh HD/Users/christpherdeo/Coding Projects py-test"

    # Run 2to3 on the Git directory
    run_2to3(git_directory)


if __name__ == "__main__":
    main()
