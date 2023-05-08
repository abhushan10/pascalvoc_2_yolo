import os
import glob
import xml.etree.ElementTree as ET

# Set path to the folder containing the xml files
xml_folder_path = "Path/to/XML/annotation"   # --> YOU HAVE TO DEFINE THE PATH

# Set the output path for the YOLO format text files
output_folder_path = "output/path/for/yolo/converted"   # --> YOU HAVE TO DEFINE THE PATH

# Loop through all the xml files in the folder
for xml_file in glob.glob(xml_folder_path + "*.xml"):
    
    # Parse the xml file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Get the image dimensions
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)
    
    # Get the class name
    class_name = root.find("object").find("name").text
    
    # Open the output text file
    output_file = open(output_folder_path + os.path.splitext(os.path.basename(xml_file))[0] + ".txt", "w")
    
    # Loop through all the objects in the xml file
    for obj in root.findall("object"):
        
        # Get the class label
        if obj.find("name").text == class_name:
            class_id = 0
        else:
            continue
        
        # Get the bounding box coordinates
        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)
        
        # Calculate the normalized coordinates
        x_center = float(xmin + xmax) / (2 * width)
        y_center = float(ymin + ymax) / (2 * height)
        bbox_width = float(xmax - xmin) / width
        bbox_height = float(ymax - ymin) / height
        
        # Write the YOLO format string to the output file
        output_file.write("{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(class_id, x_center, y_center, bbox_width, bbox_height))
    
    # Close the output file
    output_file.close()
