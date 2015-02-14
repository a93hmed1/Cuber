dd if=emmc_appsboot.mbn of=unlock.der skip=230528 bs=1 count=1198
#openssl x509 -outform der -in unlock.pem -out unlock.der
openssl x509 -inform der -in unlock.der -out unlock.pem

openssl x509 -noout -modulus -in unlock.pem