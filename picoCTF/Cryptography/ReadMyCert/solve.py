from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Specify the path to your CSR file
csr_file_path = './readmycert.csr'

# Read the CSR content from the file
with open(csr_file_path, 'rb') as csr_file:
    csr_data = csr_file.read()

# Load the CSR using the default backend
csr = x509.load_pem_x509_csr(csr_data, default_backend())

# Now you can work with the loaded CSR object
print(csr.subject.rfc4514_string())