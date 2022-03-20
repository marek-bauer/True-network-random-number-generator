from typing import Generator, List
import math


def preprocess_to_bin_file(output_file: str, data: List[int]):
    """Saves data into binary file"""
    out = open(output_file, 'wb')
    for i in range(8, len(data)+1, 8):
        byte = array_to_byte(data[i - 8:i])
        out.write(byte)
    out.close()


def preprocess_to_num_file(output_file: str, data: List[int]):
    """Saves data into txt file of 32-bits numbers"""
    out = open(output_file, 'w')
    for i in range(32, len(data)+1, 32):
        num = array_to_int(data[i - 32:i])
        out.write(str(num)+"\n")
    out.close()


def bitify(number: int, length: int) -> Generator[int, None, None]:
    """Creates generator of bits of number in specified length"""
    for _ in range(length):
        yield number % 2
        number //= 2


def convert_to_bit_vector(data: List[int], length: int) -> List[int]:
    """Converts a list of bits of number in specified length"""
    res = []
    for num in data:
        for bit in bitify(num, length):
            res.append(bit)
    return res


def get_from_generator(gen: Generator[int, None, None], num: int) -> List[int]:
    """Produces list of n number generated from generator"""
    res = []
    for n in gen:
        res.append(n)
        num -= 1
        if num == 0:
            return res
    return res


def get_vector_from_ping(file_name: str) -> List[int]:
    """Produces list of bits out of file with ping times"""
    raw = load_from_file(file_name)
    res = []
    for r in raw:
        length = math.ceil(math.log2(r))
        for _ in range(length - 13):
            res.append(r % 2)
            r //= 2
    return res


def load_from_file(file_name: str) -> List[int]:
    """Loads numbers from file and saves them into list"""
    res = []
    f = open(file_name, "r")
    for x in f:
        res.append(int(x[0:-1]))
    f.close()
    return res


def save_to_file(file_name: str, data: List[int]):
    """Saves numbers from data to file"""
    f = open(file_name, "w")
    for d in data:
        f.write(str(d) + "\n")
    f.close()


def array_to_byte(arr: List[int]) -> bytes:
    """Converts list of bits into byte"""
    base = 1
    res = 0
    for a in arr:
        if int(a) == 1:
            res += base
        base *= 2
    return res.to_bytes(1, byteorder='big', signed=False)


def array_to_int(arr: List[int]) -> int:
    """Converts list of bits into single number"""
    base = 1
    res = 0
    for a in arr:
        if int(a) == 1:
            res += base
        base *= 2
    return res
