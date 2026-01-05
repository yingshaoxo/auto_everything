import os
import sys

# Get flash information
flash_info = os.statvfs('/')

# Calculate flash space in bytes
block_size = flash_info[0]    # Filesystem block size
total_blocks = flash_info[2]  # Total blocks
free_blocks = flash_info[3]   # Free blocks

total_flash = block_size * total_blocks
free_flash = block_size * free_blocks

print("Total flash space: %d bytes (%.1f KB)" % (total_flash, total_flash / 1024))
print("Available space: %d bytes (%.1f KB)" % (free_flash, free_flash / 1024))
