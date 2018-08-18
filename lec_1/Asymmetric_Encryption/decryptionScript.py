#ch9_decrypt_blob.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import zlib

from optparse import OptionParser

parser = OptionParser() 
parser.add_option("-p", "--prvkey", dest="prvkey", help="private_key.pem path")
parser.add_option("-e", "--encrypted", dest="encrypted", help="encrypted file path")
parser.add_option("-d", "--decrypted", dest="decrypted", help="decrypted file path")

prvkey = "private_key.pem"
encrypted = ""
decrypted = ""

(options, args) = parser.parse_args()
if options.prvkey is not None :
    prvkey = options.prvkey 

if options.encrypted is not None :
    encrypted = options.encrypted 

if options.decrypted is not None :
    decrypted = options.decrypted 



#Our Decryption Function
def decrypt_blob(encrypted_blob, private_key):

    #Import the Private Key and use for decryption using PKCS1_OAEP
    rsakey = RSA.importKey(private_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    #Base 64 decode the data
    encrypted_blob = base64.b64decode(encrypted_blob)

    #In determining the chunk size, determine the private key length used in bytes.
    #The data will be in decrypted in chunks
    chunk_size = 512
    offset = 0
    decrypted = b""

    #keep loop going as long as we have chunks to decrypt
    while offset < len(encrypted_blob):
        #The chunk
        chunk = encrypted_blob[offset: offset + chunk_size]

        #Append the decrypted chunk to the overall decrypted file
        decrypted += rsakey.decrypt(chunk)

        #Increase the offset by chunk size
        offset += chunk_size

    #return the decompressed decrypted data
    return zlib.decompress(decrypted)


#Use the private key for decryption
fd = open(prvkey, "rb")
private_key = fd.read()
fd.close() 

#Our candidate file to be decrypted
fd = open(encrypted, "rb")
encrypted_blob = fd.read()
fd.close()

#Write the decrypted contents to a file
fd = open(decrypted, "wb")
fd.write(decrypt_blob(encrypted_blob, private_key))
fd.close()


#python decryptionScript.py -p private_key.pem -e   zfile_encrypted.txt  -d zfile_decrypted.txt 

 

