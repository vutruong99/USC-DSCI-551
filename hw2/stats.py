from lxml import etree
import json
import sys

from numpy import byte

def to_string(object):
    return ''.join([str(char) for char in object])

def status(input_file, output_file):
    tree = etree.parse(input_file)

    # Compute the number of files and number of directories
    file_path = "/fsimage/INodeSection/inode[type = 'FILE']"
    dir_path =  "/fsimage/INodeSection/inode[type = 'DIRECTORY']"
    numfile = len(tree.xpath(file_path)) # Count files
    numdir = len(tree.xpath(dir_path)) # Count directories

    # Compute maximum depth
    directories_ids = []

    # List of all directory ids
    id_path = "/fsimage/INodeSection/inode/id/text()"
    for elem in tree.xpath(id_path):
        directories_ids.append(to_string(elem))

    maxdepth = 0
    queue = []
    queue.append(directories_ids[0])

    depths_dict = dict()
    depths_dict[directories_ids[0]] = 1

    # Breadth First Search
    while (queue):
        current_node = queue.pop(0)

        # Append all the children of the current node to the queue
        path = "/fsimage/INodeDirectorySection/directory[parent/text() =" + current_node + "]/child/text()"
        for child in tree.xpath(path):
            child_node = to_string(child)
            queue.append(child_node)
            depths_dict[child_node] = depths_dict[current_node] + 1 # Depth of child node = depth of parent node + 1
    
    # Max depth = max value of depth dictionary
    for depth in depths_dict.values():
        if depth >= maxdepth:
            maxdepth = depth

    # Compute the maximum and minimum size of the files
    maxsize = 0 
    minsize = sys.maxsize

    for elem in tree.xpath(file_path):
        currentsize = 0

        # Go through all the blocks in a file and add the bytes together
        byte_path = "/inode/blocks/block/numBytes/text()"
        for size in etree.ElementTree(elem).xpath(byte_path):
            size = int(to_string(size))
            currentsize += int(size)

        if currentsize >= maxsize:
            maxsize = currentsize
        
        if currentsize <= minsize:
            minsize = currentsize

    # If there is no file, show no info about file size
    if numfile == 0: 
        results = {"number of files": numfile, "number of directories": numdir, 
        "maximum depth of directory tree": maxdepth}
    else:
        results = {"number of files": numfile, "number of directories": numdir, 
        "maximum depth of directory tree": maxdepth, "file size": {"max": maxsize, "min": minsize}}

    # Writing results
    result_file = open(output_file, "w")
    json.dump(results, result_file)
    result_file.close()

if __name__ == "__main__":
    try:
        status(sys.argv[1], sys.argv[2])
    except:
        print("Please provide the correct arguments")
else:
    print("Please run this program from the command line")