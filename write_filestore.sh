#!/bin/bash

while true
do
    # Generate a unique filename using the current timestamp
    filename=/path/to/filestore/$(date +"%Y%m%d%H%M%S").txt
    
    # Create the file
    touch "$filename"
    echo "file '$filename' has succesfully been created"
    
    # Wait for one second before looping again
    sleep 1
done

