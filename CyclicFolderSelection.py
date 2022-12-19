import os
import sys


def cyclicfoldername(cwd = os.getcwd(), idx_path = os.getcwd()):
    # define the file name for the last index
    index_file_name = "last_folder_index.txt"
    index_file_path = os.path.join(idx_path, index_file_name)

    if not os.path.exists(index_file_path):
        # create the file if it does not exist
        index_file = open(index_file_path, "w+")
        index_file.write("0")
        last_index = 0
        index_file.close()
    else:
        # read in the file if it does exist
        index_file = open(index_file_path, "r")
        last_index = int(index_file.read())
        index_file.close()

    # get all directories in the current folder
    dirs = [os.path.join(cwd, o) for o in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, o))]
    if last_index > len(dirs):
        last_index = 0

    # write the used index to the file
    index_file = open(index_file_path, "w")
    index_file.write(str((last_index+1) % len(dirs)))
    index_file.close()

    # return the used folder name
    return dirs[last_index]


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(cyclicfoldername(sys.argv[1], sys.argv[2]))
    elif len(sys.argv) > 1:
        print(cyclicfoldername(sys.argv[1]))
    else:
        print(cyclicfoldername())

