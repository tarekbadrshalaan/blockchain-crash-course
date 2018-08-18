package main

import (
	"crypto/sha256"
	"encoding/hex"
	"flag"
	"fmt"
)

var text = flag.String("t", " ", "text need to hash")

func main() {
	flag.Parse()
	data := []byte(*text)
	hashresult := sha256.Sum256(data)
	encodeString := hex.EncodeToString(hashresult[:])
	fmt.Println(encodeString)
}

/*
How TO USE:
>>go run Gohash.go -t HelloWorld
	res:872e4e50ce9990d8b041330c47c9ddd11bec6b503ae9386a99da8584e9bb12c4

*/
