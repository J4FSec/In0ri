import base64
import hashlib
from OpenSSL import (
    crypto,
)  # requires at least version 0.15.2 (or the latest version from GitHub, as this one is not yet released as of 2015/11/11)

# Creates a source string to generate the registration code with.
# A source string the contains product code domain and the user's registration domain,
# separated by a comma.
with open("../keys/privkey.pem") as keyfile:
    private_key_string = keyfile.read()
with open("../keys/pubkey.pem") as keyfile:
    public_key_string = keyfile.read()
product_code = "HoangNguyen-Defacement"


def make_license_source(domain):
    return (product_code + "," + domain).encode("utf8")


# This method generates a registration code. It receives your private key,
# a product code string and a registration domain.
def make_license(domain):
    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key_string)
    signature = crypto.sign(private_key, make_license_source(domain), "sha1")
    # Use sha1 instead of dss1 to avoid 'ValueError("No such digest method")'
    encoded_signature = base64.b32encode(signature)
    encoded_signature = hashlib.sha1(encoded_signature).hexdigest()
    encoded_signature = "-".join(
        [encoded_signature[i : i + 5] for i in range(0, len(encoded_signature), 5)]
    )
    return encoded_signature.upper()
