"""
Sample Argument :
--size 4 --reader_file "reader.txt" --writer_file "writer.txt" --items_file "item.txt"
"""
import argparse
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
class CacheClass:
    """
    CacheClass: Implements LRU Cache
    """
    def __init__(self, cache_size):
        self.storage_cache = dict()
        self.storage_limit = cache_size
        self.frequency_cache = dict()

    def search_element(self, element):
        """
        Searches for element in the cache
        :param element: cache key
        :return: cache value, cache search flag
        """
        if element in self.storage_cache.keys():
            value = self.storage_cache[element]
            # Update frequency of the element in cache
            if element in self.frequency_cache.keys():
                self.frequency_cache[element] += 1
            return value, True
        return None, False

    def add_element(self, element, value):
        """
        Adds element to cache
        :param element: cache key
        :param value: cache key value
        """
        # Evict an element if cache is full
        if not len(self.storage_cache) < self.storage_limit:
            self.__evict_element()
        self.storage_cache[element] = value
        self.frequency_cache[element] = 1

    def __evict_element(self):
        # Least Recently used(LRU)
        lru_element = min(self.frequency_cache, key=lambda key: self.frequency_cache[key])
        # Remove LRU element from cache and counter
        self.storage_cache.pop(lru_element)
        self.frequency_cache.pop(lru_element)

    def invalidate_cache(self, data):
        """
        invalidates cache data
        :param data: new data for cache invalidation
        """
        for key in self.storage_cache:
            self.storage_cache[key] = data[key]


class InMemoryFileCache:
    """
    There are multiple readers and writers of items.
    Number of readers and writers comes from Readers and Writers
    file which is passed to the program from command line.
    """
    def __init__(self, cache_size, reader, writer, item):
        self.cache_size = cache_size
        self.read_cache = CacheClass(cache_size)
        self.reader_file = reader
        self.writer_file = writer
        self.items_file = item
        self.reader_filenames = self.fetch_text_file_data(Path("reader.txt"))
        self.writer_filenames = self.fetch_text_file_data(Path("writer.txt"))
        self.reader_main()
        # self._writer_main()

    @staticmethod
    def fetch_text_file_data(filename, retun_int=False):
        """
        reads data from text file
        :param filename: text filename
        :param retun_int: True-integer, False-String
        :return: text file data as list
        """
        with open(filename) as file:
            data = file.readlines()
        data_string_list = [item.replace("\n", "") for item in data]
        if retun_int:
            data_int_list = []
            for element in data_string_list:
                element = int(element) if element != "" else None
                data_int_list.append(element)
        return data_string_list

    def reader_main(self):
        """
        spawn reader file threads
        """
        print("Start:: READER")
        for filename in self.reader_filenames:
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.submit(self._read_file, filename)
            # self._read_file(filename)
        print("END:: READER")

    def _read_file(self, reader_name):
        positions_list = self.fetch_text_file_data(reader_name)
        # positions_count = len(positions_list)
        # with ThreadPoolExecutor(max_workers= positions_count) as executor:
        #     for position in positions_list:
        #         arguments = [int(position),reader_name]
        #         print("_read_file - {}-{}".format(reader_name, position))
        #         executor.submit(self._read_position, arguments)
        for position in positions_list:
            self._read_position(int(position), reader_name)

    def _read_position(self, position, reader_name):
        value, cache_flag = self.read_cache.search_element(element=position)
        read_type = {True: "Cache", False: "Disk"}
        if not cache_flag:
            item_list = self.fetch_text_file_data(self.items_file)
            try:
                value = item_list[position]
            except IndexError:
                value = None
            # Cache miss - Add element to the cache
            self.read_cache.add_element(element=position, value=value)
        # Creating/Using reader logger
        reader_log_filename = Path(reader_name + ".out.txt")
        with open(reader_log_filename, "a+") as reader_logger:
            reader_logger.write("{} {}\n".format(value, read_type[cache_flag]))
        print("_read_position - {} - {}".format(reader_log_filename, value))

    def writer_main(self):
        """
        spawns writer file threads
        """
        print("Start::WRITER")
        for filename in self.writer_filenames:
            # self._write_file(filename)
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.submit(self._write_file, filename)

    def _write_positions_to_items(self, items_list):
        with open(self.items_file, "w") as items_file:
            for item in items_list:
                if item is None:
                    item = ""
                items_file.write("{}\n".format(str(item)))
        # Invalidate Cache
        items_data = self.fetch_text_file_data(Path(self.items_file), retun_int=True)
        self.read_cache.invalidate_cache(items_data)

        print("End::WRITER")

    def _write_file(self, writer_name):
        positions_list = self.fetch_text_file_data(writer_name)
        item_data = self.fetch_text_file_data(self.items_file, retun_int=True)
        item_data_lenght = len(item_data)
        for position_value in positions_list:
            position_string, value_string = position_value.split(" ")
            position, value = int(position_string), int(value_string)
            if position >= item_data_lenght:
                extension_lenght = position-(item_data_lenght-1)
                for _ in range(extension_lenght):
                    item_data.append(None)
                item_data_lenght = item_data_lenght + extension_lenght
            item_data[position] = value
        self._write_positions_to_items(item_data)


if __name__ == "__main__":

    ARGUMENTS_PARSER = argparse.ArgumentParser(description='In Memory File Cache System')
    ARGUMENTS_PARSER.add_argument('--size', type=int, help='Size of Cache', required=True,
                                  default=4)
    ARGUMENTS_PARSER.add_argument('--reader_file', type=str, help='Reader File', required=True)
    ARGUMENTS_PARSER.add_argument('--writer_file', type=str, help='Writer File', required=True)
    ARGUMENTS_PARSER.add_argument('--items_file', type=str, help='Items File', required=True)
    ARGUMENTS = ARGUMENTS_PARSER.parse_args()

    if (os.path.isfile(os.path.join(os.getcwd(), Path(ARGUMENTS.reader_file)))and
            os.path.isfile(os.path.join(os.getcwd(), Path(ARGUMENTS.writer_file)))and
            os.path.isfile(os.path.join(os.getcwd(), Path(ARGUMENTS.items_file)))):

        InMemoryFileCache(cache_size=ARGUMENTS.size, reader=ARGUMENTS.reader_file,
                          writer=ARGUMENTS.writer_file, item=ARGUMENTS.items_file)
    else:
        print("Check Input Command Line Parameters")
