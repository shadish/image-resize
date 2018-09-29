import os, sys
import shutil, errno

from PIL import Image

# --- functions
def copystuff(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def resize(insize, infile, outfile):
	size = insize, insize
	try:
		im = Image.open(infile)
		im = im.resize(size, Image.ANTIALIAS)
		im.save(outfile)
	except IOError:
		print "Error resizing image %s" % infile

# --- logic
configfile = "config.txt"

if not os.path.isfile(configfile):
	print 'File does not exist.'
else:
	with open(configfile) as f:
		content = f.read().splitlines()

	for line in content:
		key = line.split('=')[0]
		val = line.split('=')[1]
		if(key == 'inpath'):
			print('found inpath')
			inpath = val
		if(key == 'outpath'):
			outpath = val
		if(key == 'size'):
			insize = val

in_dirs = os.listdir(inpath)

for i in in_dirs:
	print(" *************** processing: %s" % i)
	srcpath = inpath+i+"/full"
	dest = outpath+i+"/full"
	dest_resized = outpath+i+"/"+insize

	if(os.path.exists(dest)):
		print(i+"/full already exists, skipping.")
	else:
		print('copying originals: %s' % i)
		copystuff(inpath+i, outpath+i)

	if(os.path.exists(dest_resized)):
		print(i+"/"+insize+" already exists, skipping.")
	else:
		for f in os.listdir(srcpath):
			src_file = srcpath+"/"+f
			dest_file = dest_resized+"/"+f.replace('.png','_'+insize+".png")
			print('Resizing '+ i + " to "+ insize)
			ensure_dir(dest_file)
			resize(int(insize), src_file, dest_file)

