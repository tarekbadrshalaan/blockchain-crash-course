#generate_keys.py
from Crypto.PublicKey import RSA
from optparse import OptionParser

parser = OptionParser() 
parser.add_option("-d", "--dir", dest="dir", help="directory save public private keys")

dir = ""
(options, args) = parser.parse_args()
if options.dir is not None :
    dir = options.dir + "/"

#Generate a public/ private key pair using 4096 bits key length (512 bytes)
new_key = RSA.generate(4096, e=65537)

#The private key in PEM format
private_key = new_key.exportKey("PEM")

#The public key in PEM Format
public_key = new_key.publickey().exportKey("PEM")

fd = open(dir+"private_key.pem", "wb")
fd.write(private_key)
fd.close()

fd = open(dir+"public_key.pem", "wb")
fd.write(public_key)
fd.close()

#python GenerateRSA.py 