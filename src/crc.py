import numpy as np


# refered
# https://edom18.hateblo.jp/entry/2022/02/14/082055#CRC%E3%81%AE%E8%A8%88%E7%AE%97
class CRC:
	def __init__(self) -> None:
		self.__table = CRC.__make_table()

	def hash(self, chunk_type: list[np.uint8], chunk_data: list[np.uint8]) -> bytes:
		crc = self.__hash(0, chunk_type)
		crc = self.__hash(crc, chunk_data)
		return int(crc).to_bytes(4, 'big')

	def __hash(self, crc: np.uint32, buffer: list[np.uint8]) -> np.uint32:
		crc = crc ^ 0xffffffff
		return self.__calculate(crc, buffer) ^ 0xffffffff

	def __calculate(self, crc: np.uint32, buffer: list[np.uint8]) -> np.uint32:
		c = crc
		for i in range(len(buffer)):
			c = self.__table[(c ^ buffer[i]) & 0xff] ^ (c >> 8)

		return c

	@staticmethod
	def __make_table():
		table = np.zeros([256], dtype=np.uint32)

		for i in range(len(table)):
			c = i

			for j in range(8):
				c = (0xedb88320 ^ (c >> 1)) if ((c & 1) != 0) else c >> 1

			table[i] = c

		return table
