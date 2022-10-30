import os
import sys
from argparse import ArgumentParser

import cv2
import numpy as np

from crc import CRC


def parse_arg(args: list[str]):
	parser = ArgumentParser('FatPng')

	parser.add_argument('--input', required=False, type=str, default=None, help='the path of input base image file.')
	parser.add_argument('--width', required=False, type=int, default=None, help='the width of output image.')
	parser.add_argument('--height', required=False, type=int, default=None, help='the height of output image.')
	parser.add_argument('--size', required=True, type=int, help='expected filesize of output image.')
	parser.add_argument('--output', required=False, type=str, default="image.png", help='the path of output file.')

	def validate_args(args):
		if args.input is not None:
			if not os.path.isfile(args.input):
				raise FileNotFoundError(args.input)
		else:
			if (args.width is None) or (args.height is None):
				raise RuntimeError(f'Arguments width and height is required if not set argument input.')
			if (args.width <= 0) or (args.height <= 0):
				raise RuntimeError(f'Arguments width and height must be greater than 0.')

		ext = os.path.splitext(args.output)[-1].lower()
		if ext != '.png':
			raise RuntimeError(f'Output image file must be png.')
		
		return args

	return validate_args(parser.parse_args(args))

def main(args):
	image = np.full([args.height, args.width, 3], [0, 0, 0], dtype=np.uint8)\
		if args.input is None else cv2.imread(args.input, cv2.IMREAD_UNCHANGED)

	intermediate_filepath = f"{args.output}.im.png"
	cv2.imwrite(intermediate_filepath, image)

	with open(intermediate_filepath, 'rb') as f:
		b = f.read()
		if len(b) > args.size:
			raise RuntimeError('Filesize of intermediate generated image is already greater than expected size.')
		if len(b) == args.size:
			if os.path.isfile(intermediate_filepath):
				os.remove(intermediate_filepath)
			with open(args.output, 'wb') as wf:
				wf.write(b)
				return 0
		if (len(b) + 4 + 4 + 4) > args.size:
			raise RuntimeError('Failed to increase failed due to insufficient size for additional chunks.')

		# find start of IEND chunk type
		keyword = b'IEND'
		keyword_len = len(keyword)
		index = None
		for i in range(len(b) - keyword_len, -1, -1):
			if np.all(b[i:i+keyword_len] == keyword):
				index = i
				break

		if index is None:
			raise RuntimeError('Not found "IEND" chunk in intermediate file.')
		# move to head of IEND chunk
		index = index - 4

		post_chunk = b[index:]

	fat_chunk_data = np.zeros([args.size - (len(b) + 4 + 4 + 4)], dtype=np.uint8)
	fat_chunk_type = b'efAT'
	fat_chunk_crc = CRC().hash(fat_chunk_type, fat_chunk_data)
	fat = bytearray(len(fat_chunk_data).to_bytes(4, 'big'))
	fat.extend(fat_chunk_type)
	fat.extend(fat_chunk_data)
	fat.extend(fat_chunk_crc)

	new_output = bytearray(b[:index])
	new_output.extend(fat)
	new_output.extend(post_chunk)
	with open(args.output, 'wb') as f:
		f.write(new_output)

	if os.path.isfile(intermediate_filepath):
		os.remove(intermediate_filepath)

	return 0

if __name__ == '__main__':
	exit(main(parse_arg(sys.argv[1:])))
