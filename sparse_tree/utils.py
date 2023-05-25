"""
 utils.py
 
 EPCC, The University of Edinburgh
 
 (c) 2023 The University of Edinburgh
 
 Contributing Authors:
 Christodoulos Stylianou (c.stylianou@ed.ac.uk)
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
 	http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import numpy as np
import io


def extract_array(writer, array, size, comment=None):
    if comment:
        writer.write("# " + comment + "\n")
    for i, entry in enumerate(array):
        writer.write(str(entry) + ("\t" if i < size - 1 else "\n"))


def write_array_to_bytes(file_handler, array, dtype=np.int32):
    if not isinstance(file_handler, io.BufferedWriter):
        raise TypeError("file handler must be of type io.BufferedWriter")

    if type(array) is np.ndarray:
        # write to bytes
        file_handler.write(np.array(array, dtype=dtype).tobytes())
    elif isinstance(array, list):
        for entry in array:
            write_to_bytes(file_handler, entry)
    else:
        raise TypeError("Array type not supported for BinaryIO!")


def write_to_bytes(file_handler, entry):
    if not isinstance(file_handler, io.BufferedWriter):
        raise TypeError("file handler must be of type io.BufferedWriter!")

    if isinstance(entry, (int, np.int32, np.int64)):
        # write as int to bytes
        file_handler.write(int(entry).to_bytes(4, byteorder="little", signed=True))
    elif isinstance(entry, str):
        # write as str with encoding
        file_handler.write(entry.encode("utf-8"))
    else:
        raise TypeError("Type of entry not supported for BinaryIO!")


def build_str_sizelist(lstr):
    if not isinstance(lstr, list):
        raise TypeError("lstr must be a list!")

    lsize = np.zeros(len(lstr), dtype=np.int32)
    for i, entry in enumerate(lstr):
        lsize[i] = len(entry)

    return lsize
