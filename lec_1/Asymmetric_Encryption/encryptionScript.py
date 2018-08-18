#ch9_encrypt_blob.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64

from optparse import OptionParser


parser = OptionParser() 
parser.add_option("-p", "--pubkey", dest="pubkey", help="public_key.pem path")
parser.add_option("-u", "--unencrypted", dest="unencrypted", help="unencrypted file path")
parser.add_option("-e", "--encrypted", dest="encrypted", help="encrypted file path")

pubkey = "public_key.pem"
unencrypted = ""
encrypted = ""

(options, args) = parser.parse_args()
if options.pubkey is not None :
    pubkey = options.pubkey 

if options.unencrypted is not None :
    unencrypted = options.unencrypted 

if options.encrypted is not None :
    encrypted = options.encrypted 

#Our Encryption Function
def encrypt_blob(blob, public_key):
    #Import the Public Key and use for encryption using PKCS1_OAEP
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    #compress the data first
    blob = zlib.compress(blob)

    #In determining the chunk size, determine the private key length used in bytes
    #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
    #in chunks
    chunk_size = 470
    offset = 0
    end_loop = False
    encrypted =  b""

    while not end_loop:
        #The chunk
        chunk = blob[offset:offset + chunk_size]

        #If the data chunk is less then the chunk size, then we need to add
        #padding with " ". This indicates the we reached the end of the file
        #so we end loop here
        if len(chunk) % chunk_size != 0:
            end_loop = True
            chunk += b" " * (chunk_size - len(chunk))

        #Append the encrypted chunk to the overall encrypted file
        encrypted += rsa_key.encrypt(chunk)

        #Increase the offset by chunk size
        offset += chunk_size

    #Base 64 encode the encrypted file
    return base64.b64encode(encrypted)

#Use the public key for encryption
fd = open(pubkey, "rb")
public_key = fd.read()
fd.close()


#Our candidate file to be encrypted
fd = open(unencrypted, "rb")
unencrypted_blob = fd.read()
fd.close()


encrypted_blob = encrypt_blob(unencrypted_blob, public_key)
#Write the encrypted contents to a file
fd = open(encrypted, "wb")
fd.write(encrypted_blob)
fd.close()



#python encryptionScript.py -p public_key.pem -u zfile.txt -e zfile_encrypted.txt  
