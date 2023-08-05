# remove the personal information from the 42 header

new_header = [
    "/*                                                  +#+  +:+       +#+        */",
    "/*                                                +#+#+#+#+#+   +#+           */",
    "/*                                                     #+#    #+#             */",
    "/*                                                    ###   ########.fr       */",
]

import os
import sys

def valid_header(content):
    return (
        content[0]
        == "/******************************************************************************/\n"
        or content[1]
        == "/*                                                                            */\n"
        or content[2]
        == "/*                                                        :::      ::::::::   */\n"
        or content[6]
        == "/*                                                +#+#+#+#+#+   +#+           */\n"
        or content[9]
        == "/*                                                                            */\n"
        or content[10]
        == "/******************************************************************************/\n"
    )

def copy_file(file, output):
    print(f"Copy {file} to {output}")
    # create the output directory
    output_dir = os.path.dirname(output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # copy the file
    os.system(f"cp {file} {output}")

def remove_header(file, output):
    with open(file, 'r') as f:
        # read the file
        content = f.readlines()

    if not valid_header(content):
        print(f"Invalid header: {file} for {file}")
        copy_file(file, output)
        return

    # replace line 6-9 with new_header
    for i in range(5, 9):
        content[i] = new_header[i - 5] + '\n'

    # write the file
    with open(output, 'w') as f:
        f.write(''.join(content))

def recursive_remove_header(input_dir, output_dir):
    # keep the same structure
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.c') or file.endswith('.h'):
                # create the output directory
                output = root.replace(input_dir, output_dir)
                if not os.path.exists(output):
                    os.makedirs(output)
                # remove the header
                remove_header(os.path.join(root, file), os.path.join(output, file))
            else:
                copy_file(os.path.join(root, file), os.path.join(root.replace(input_dir, output_dir), file))

    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        recursive_remove_header(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 remove.py <input_dir> <output_dir>")
