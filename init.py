
# This script installs and updates all the dependencies needed to start a new VELOCE service.
# It requires Python3, which sadly can't install itself.

# You need to have access to the repo specified below, in GIT_BASE_REPO in order for this script to work.

# ============= USAGE ==============
# > python3 init.py
# ==================================

# Configuration options : 
GIT_SELF_REPO = "https://github.com/matthieuv-chabe/Bootstrap_Veloce"
GIT_BASE_REPO = "https://github.com/matthieuv-chabe/Service_Client"
NODE_MIN_MAJOR = 20

import os
import sys
import subprocess
import platform
import shutil

def main():
    
    # First check if we are not from "script" directory
    if os.path.basename(os.getcwd()) == "script":
        print("Warning: You are running this script from the script directory.")
        print("\tChanging directory to the root of the project.")
        os.chdir("..")
    
    # If the project is still bound to its own github repository (matthieuv/veloce), remove it
    command = "git remote -v"
    output  = ""
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8")
    except:
        pass
    if GIT_SELF_REPO in output:
        print("Warning: You are running this script from a cloned repository.")
        print("\tRemoving the remote origin.")
        command = "git remote remove origin"
        subprocess.call(command, shell=True)
        # delete the .git folder
        shutil.rmtree(".git")
    
    # Check if we are running on a supported platform (Linux, MacOS, Windows)
    if not platform.system() in ["Linux", "Darwin", "Windows"]:
        print("Error: Unsupported platform.")
        print("\tOnly Linux, MacOS and Windows are supported.")
        sys.exit(1)
    
    # Check if Node and NPM are installed, and with the correct version
    print("Checking Node and NPM...")
    command = "node --version"
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8")
    except:
        print("Error: Node is not installed.")
        sys.exit(1)
    
    if int(output.split(".")[0][1:]) < NODE_MIN_MAJOR:
        
        # If windows, open the download page
        if platform.system() == "Windows":
            print("Error: Node version is too old.")
            print("\tPlease download and install the latest version from https://nodejs.org/en/download/")
            # If the user press Y open the download page
            if input("Open download page? [y/N] ").lower() == "y":
                import webbrowser
                webbrowser.open("https://nodejs.org/en/download/")
        
        # If linux or mac, try to install it with the package manager
        else:
            print("Error: Node version is too old.")
            print("\tPlease install the latest version using your package manager.")

        sys.exit(1)

    # Check if yarn is installed
    print("Checking Yarn...")
    command = "yarn --version"
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8")
    except:
        print("Error: Yarn is not installed.")
        # Install yarn
        print("Installing Yarn...")
        if platform.system() == "Windows":
            command = "npm install -g yarn"
        else:
            command = "sudo npm install -g yarn"
        subprocess.call(command, shell=True)
        # Check if yarn is installed
        command = "yarn --version"
        try:
            output = subprocess.check_output(command, shell=True).decode("utf-8")
        except:
            print("Error: Yarn has not been installed correctly.")
            sys.exit(1)

    # Clone the base repository (warning, the directory is not empty !)
    # We first clone in the "base" directory, then move the files to the root
    print("Cloning the base repository...")
    command = "git clone " + GIT_BASE_REPO + " base --recursive"
    subprocess.call(command, shell=True)

    # Move the files to the root
    print("Moving files to the root...")
    for filename in os.listdir("base"):
        shutil.move("base/" + filename, filename)
    shutil.rmtree("base")

    # Ensure the submodules are activated and up to date
    print("Updating submodules...")
    command = "git submodule update --init --recursive"
    subprocess.call(command, shell=True)
    
    # Install the dependencies
    print("Installing dependencies...")
    command = "yarn install"
    subprocess.call(command, shell=True)

    # Ask if the user wants to start the project (with yarn dev)
    if input("Start the project? [Y/n] ").lower() != "n":
        command = "yarn dev"
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()
