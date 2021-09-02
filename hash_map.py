
# Description: Hash Map Implementation with the following methods:
# empty_buckets(), table_load(), clear(), put(), contains_key(), get(), remove(),
# resize_table() and get_keys().


# Import pre-written DynamicArray and LinkedList classes
from include_support import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """Clears the content of the hash map. It does not change the underlying hash table
        capacity."""

        index = 0
        # for each element in the dynamic array replace linked list with empty list
        while index < self.capacity:
            self.buckets.set_at_index(index, LinkedList())
            index += 1

        self.size = 0

        pass

    def get(self, key: str) -> object:
        """Returns the value associated with the given key. If the key is not in the hash
        map, the method returns None."""

        index = 0
        # loop through the full array
        while index < self.buckets.length():
            link_list = self.buckets.get_at_index(index)
            # when a linked list contains the key, traverse the list until the correct
            # node is found and return the node's value
            if link_list.contains(key):
                for node in link_list:
                    if node.key == key:
                        return node.value
            index += 1
        return None

    def put(self, key: object, value: object) -> object:
        """Updates the key/value pair in the hash map. If a given key already exists in
        the hash map, its associated value should be replaced with the new value. If
        the key is not in the hash map, a key/value pair should be added."""

        hash_key = self.hash_function(key)
        index = hash_key % self.capacity
        link_list = self.buckets.get_at_index(index)
        key_exists = link_list.contains(key)

        # when the key does not exist in the linked list, insert key/value pair
        if not key_exists:
            link_list.insert(key, value)
            self.size += 1
        # when the key already exists in the linked list, search the list for the key,
        # once the key is found update node's value with provided value argument
        else:
            for node in link_list:
                if node.key == key:
                    node.value = value
                    break
                node = node.next
        pass

    def remove(self, key: str) -> None:
        """Removes the given key and its associated value from the hash map. If a given
        key is not in the hash map, the method does nothing (no exception is raised)."""

        index = 0
        # loop through the dynamic array
        while index < self.capacity:
            # search each linked list for the provided key
            link_list = self.buckets.get_at_index(index)
            # remove key if found and decrement size by 1
            if link_list.contains(key):
                link_list.remove(key)
                self.size -= 1
                return
            index += 1

        pass

    def contains_key(self, key: str) -> bool:
        """Returns True if the given key is in the map, otherwise it returns False. An
        empty hash map does not contain any keys."""

        index = 0
        # loop through the dynamic array
        while index < self.capacity:
            # search each linked list for the provided key
            link_list = self.buckets.get_at_index(index)
            if link_list.contains(key):
                return True
            index += 1

        return False

    def empty_buckets(self) -> int:
        """Returns a number of empty buckets in the hash table."""

        index, counter = 0, 0
        # loop based on capacity on DynamicArray
        while index < self.capacity:
            # get linked list object from index and if size is 0 increment empty counter
            link_list = self.buckets.get_at_index(index)
            if link_list.length() == 0:
                counter += 1
            index += 1
        return counter

    def table_load(self) -> float:
        """This method returns the current hash table load factor."""

        index, num_elements = 0, 0
        # for each linked_list in the array, add the length of the list to num_elements
        while index < self.capacity:
            link_list = self.buckets.get_at_index(index)
            num_elements += link_list.length()
            index += 1

        # load factor calculation
        num_buckets = self.capacity
        load_factor = num_elements / num_buckets

        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """Changes the capacity of the internal hash table. All existing key/value pairs
        must remain in the new hash map and all hash table links must be rehashed. If
        new_capacity is less than 1, this method does nothing."""

        # get keys and values for all existing key/value pairs
        index, counter, num_nodes = 0, 0, 0
        keys, values = DynamicArray(), DynamicArray()
        # loop through the full dynamic array
        while index < self.buckets.length():
            link_list = self.buckets.get_at_index(index)
            for node in link_list:
                keys.append(node.key)
                values.append(node.value)
                num_nodes += 1
            index += 1

        # all key/value pairs have been saved, now clear the hash table, establish a
        # new dynamic array and add requested capacity
        self.clear()
        self.buckets = DynamicArray()
        for _ in range(new_capacity):
            self.buckets.append(LinkedList())
        self.capacity = new_capacity

        # put the key/value pairs back into the bucket and rehash
        num = 0
        while num < num_nodes:
            self.put(keys.get_at_index(num), values.get_at_index(num))
            num += 1

        pass

    def get_keys(self) -> DynamicArray:
        """Returns a DynamicArray that contains all keys stored in your hash map. The
        order of the keys in the DynamicArray does not matter."""

        index, counter = 0, 0
        key_array = DynamicArray()
        # loop through the full array
        while index < self.buckets.length():
            # loop through the list adding keys to key_array
            link_list = self.buckets.get_at_index(index)
            for node in link_list:
                key_array.append(node.key)
            index += 1

        return key_array


# BASIC TESTING
if __name__ == "__main__":
    """
    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    
    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    
    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)
    
    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)
    
    
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    
    # Put testing identical key value replacement
    m = HashMap(10, hash_function_1)
    m.put("001", "A")
    m.put("002", "B")
    m.put("003", "C")
    m.put("004", "Error")
    m.put("005", "E")
    m.put("006", "Error")
    m.put("007", "G")
    m.put("004", "D")
    m.put("006", "F")
    m.put("008", "H")
    m.put("009", "I")
    m.put("010", "J")
    m.put("011", "K")
    print(m)
    
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('largest_key', 1001)
    m.put('key1', 10)
    m.put('smallest_key', .001)
    print(m)
    print(m.get('key1'))
    m.remove('key1')
    m.remove('smallest_key')
    print(m.get('key1'))
    print(m)
    m.remove('key4')
    

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    
    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys()) 
    """