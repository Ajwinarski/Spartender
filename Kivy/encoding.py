import base64

data = "1130"

# Standard Base64 Encoding
encodedBytes = base64.b64encode(data.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")

print("Encoded String: ", encodedStr)


decodedBytes = base64.decodebytes(encodedBytes)

print("Decoded Bytes: ", decodedBytes)


decodedString = str(decodedBytes, "utf-8")

print("Decoded String: ", decodedString)
