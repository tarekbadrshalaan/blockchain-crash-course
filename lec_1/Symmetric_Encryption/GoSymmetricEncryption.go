package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"flag"
	"fmt"
	"io"
	"log"
)

var text = flag.String("t", "My name is foo", "text to encrypt")
var key = flag.String("k", "the-key-has-to-be-32-bytes-long!", "key to encrypt")
var ciphertext = flag.String("c", "", "cipher text")
var op = flag.String("o", "e", "opration(e:encrpyt,d:decrypt)")

func main() {
	flag.Parse()

	if *op == "e" {
		result, err := encrypt([]byte(*text), []byte(*key))
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%x\n", result)
	}
	if *op == "d" {
		data, _ := hex.DecodeString(*ciphertext)
		plaintext, err := decrypt(data, []byte(*key))
		if err != nil {
			// TODO: Properly handle error
			log.Fatal(err)
		}
		fmt.Printf("%s\n", plaintext)

	}
}

func encrypt(plaintext []byte, key []byte) ([]byte, error) {
	c, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	gcm, err := cipher.NewGCM(c)
	if err != nil {
		return nil, err
	}

	nonce := make([]byte, gcm.NonceSize())
	if _, err = io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, err
	}

	return gcm.Seal(nonce, nonce, plaintext, nil), nil
}

func decrypt(ciphertext []byte, key []byte) ([]byte, error) {
	c, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	gcm, err := cipher.NewGCM(c)
	if err != nil {
		return nil, err
	}

	nonceSize := gcm.NonceSize()
	if len(ciphertext) < nonceSize {
		return nil, errors.New("ciphertext too short")
	}

	nonce, ciphertext := ciphertext[:nonceSize], ciphertext[nonceSize:]
	return gcm.Open(nil, nonce, ciphertext, nil)
}

/*
How To Use:
>>go run GoSymmetricEncryption.go -t foo
	res:85b6278dac2f89602f30144515f3809852f83990544495902426bae3e6cffc
>>go run GoSymmetricEncryption.go -o d -c 85b6278dac2f89602f30144515f3809852f83990544495902426bae3e6cffc
	res:foo
*/
