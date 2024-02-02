import os,subprocess,shutil,time,sys

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
modsDir = (os.getenv('APPDATA') + "/.minecraft/mods").replace("\\","/")
REPO_URL = "https://github.com/Techmokid/Minecraft-Mods.git"

def exclude_py_files(dirname, filenames):
    return [filename for filename in filenames if filename.endswith('.py')]

def clone_git_repo(repo_url, target_dir):
    print("Cloning repo: " + REPO_URL + " into directory: " + target_dir)
    
    try:
        subprocess.run(["git", "clone", repo_url, target_dir], shell=True, check=True)
        print("Repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to clone repository: {e}")

if os.path.join(os.path.expanduser('~'), "Documents", "GitHub") not in os.getcwd():
    print("Executing File Safe Variant")

    #See if Git is installed
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        #Git isn't callable. Try to install chocolatey and git
        print("Error: Git not installed. Attempting to install")

        failure = False
        result = None
        try:
            result = subprocess.run(["choco", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0 and result.stdout.strip():
                #Chocolatey is already installed
                print("Chocolatey is already installed with version: " + str(result.stdout.strip()))
            else:
                failure = True
        except:
            failure = True

        if failure == True:
            #Chocolatey is not installed. Install now
            print("Chocolatey is not installed. Installing now...")
            if os.path.exists("C:/ProgramData/chocolatey"):
                shutil.rmtree("C:/ProgramData/chocolatey")
            
            try:
                subprocess.run(["powershell", "-Command", r"Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"], shell=True, check=True)
                print("Successfully installed Chocolatey")
                
                subprocess.Popen("python \"C:/Temp/UpdateMinecraftMods.py\"", shell=True, close_fds=True, cwd=desktop_path)
                sys.exit()
            except subprocess.CalledProcessError as e:
                print("ERROR: Failed to install Chocolatey. Perhaps you didn't run as administrator?")
                time.sleep(5)
                sys.exit(1)

        try:
            subprocess.run("choco upgrade chocolatey -y", shell=True, check=True)
            print("Successfully Upgraded Chocolatey")
        except:
            print("ERROR: Failed to upgrade Chocolatey. Perhaps you didn't run as administrator?")
            time.sleep(5)
            sys.exit(1)

        # We now have Chocolatey installed. Now install Git
        try:
            subprocess.run(["choco", "install", "git.install", "-y", "--force"], shell=True, check=True)
            print("Successfully installed Git")
        except subprocess.CalledProcessError as e:
            print("Failed to install Git")
            time.sleep(5)
            sys.exit(1)

    #Git is found and functional! Now just clone the repo
    print("Git discovered. Cloning repo...")
    GH_MC_Mods_Dir = os.path.join(os.path.expanduser('~'), "Documents", "GitHub","Minecraft-Mods")
    if os.path.exists(GH_MC_Mods_Dir):
        potDir = "C:/Users/aj200/Documents/GitHub/Minecraft-Mods/.git"
        if os.path.exists(potDir):
            subprocess.run(['attrib', '-r', '/s', '/d', '*'], shell=True, cwd=potDir, check=True)
        time.sleep(1)
        shutil.rmtree(GH_MC_Mods_Dir)
    
    try:
        clone_git_repo(REPO_URL,GH_MC_Mods_Dir)
    except Exception as e:
        print("Error cloning Git repository: " + str(e))
        time.sleep(5)
        sys.exit(1)
    
    print("Cloned successfully. Updating mods")
    if (os.path.exists(modsDir)):
        shutil.rmtree(modsDir)
    shutil.copytree(os.path.join(GH_MC_Mods_Dir, "Braydon-Andrey 1.19.2 Zoo"), modsDir, ignore=exclude_py_files)
    sys.exit()
else:
    if os.path.exists("C:/Temp/"):
        shutil.rmtree("C:/Temp/")
    os.mkdir("C:/Temp/")
    shutil.copy(__file__, "C:/Temp/UpdateMinecraftMods.py")
    subprocess.Popen("python \"C:/Temp/UpdateMinecraftMods.py\"", shell=True, close_fds=True, cwd=desktop_path)
    time.sleep(5)
    sys.exit()









