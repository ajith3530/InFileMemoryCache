# InFileMemoryCache

**Required Files:
reader.txt
writer.txt
item.txt
reader1.txt, reader2.txt...
writer1.txt, writer2.txt...

**No External Depencencues - Python 3.7 - Standard Library

**Assumptions and Design Considerations
1. Readers and Writers will be executed consecutively.
2. Empty spaces and non-numeric values to be be treated as blank spaces
3. Usage of cache function as a non-decorator function.
4. Since the application is written in Python, build is not required.
5. Application can run directly from LINUX terminal, if python is installed.
6. If the application is read heavy, then the cache should be based on cache through principle,
   wherein the application only interfaces with cache, and only during cache miss interacts with the items_file/database.
7. For Write heavy systems, write-back cache design system is preferred wherein the application interacts with cache with write requests,
   and the cache updates the items_file/database after some predetermined delay.
8. Corner cases such are file error, string errors are covered in unittests.


**Build Instructions for Windows:
1. Open command prompt in project directory. (cd directory)
2. Use the command below for execution
   python main.py --size 4 --reader_file "reader.txt" --writer_file "writer.txt" --items_file "item.txt"
3. Reader output files will be generated after the application completes execution
4. Optional : Use the command below for removing output files
   python delete_files.py

**Build Instrunctions for Linux:
1. Add project directory location in Terminal. (cd Directory)
2. Use the command below assigning the file as an executable. (Optional)
   chmod +x main.py
3. Use the command below for execution.
   python main.py --size 4 --reader_file "reader.txt" --writer_file "writer.txt" --items_file "item.txt"
