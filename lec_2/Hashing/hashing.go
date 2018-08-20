package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"syscall"
)

//BestZero :
type BestZero struct {
	Nonce      int
	zerosCount int
	Zeros      string
	Checksum   string
}

//HashTextNonce :
func HashTextNonce(bytetext []byte, nonce int) [32]byte {
	dataToHash := append(bytetext, []byte(strconv.Itoa(nonce))...)
	return sha256.Sum256(dataToHash)
}

//ChackHexadecimalZeros :
func ChackHexadecimalZeros(hexadecimal []byte, ze string) (bool, string) {
	encodeString := hex.EncodeToString(hexadecimal)
	if !strings.HasPrefix(encodeString, ze) {
		return false, ""
	}
	result := ze
	triesZeros := ze
	for {
		if strings.HasPrefix(encodeString, triesZeros) {
			result = triesZeros
		} else {
			return true, result
		}
		triesZeros += "0"
	}
}

//GetBestZeros :
func GetBestZeros(data []byte) {
	bestZero := BestZero{}
	guard := make(chan struct{}, 4)
	start := 0
	end := 1000000

	for {
		guard <- struct{}{}
		go func(start, end int) {
			fmt.Printf("start:%d %d\n", start, end)
			for i := start; i < end; i++ {
				c1 := HashTextNonce(data, i)
				if hasZeros, zerosinString := ChackHexadecimalZeros(c1[:], bestZero.Zeros); hasZeros {
					if bestZero.zerosCount < len(zerosinString) {
						bestZero.zerosCount = len(zerosinString)
						bestZero.Zeros = strings.Repeat("0", bestZero.zerosCount)
						bestZero.Nonce = i
						bestZero.Checksum = hex.EncodeToString(c1[:])
						fmt.Printf("%d\n%v\n%d\n%v\n===\n", bestZero.zerosCount, bestZero.Zeros, bestZero.Nonce, bestZero.Checksum)
					}
				}
			}
			<-guard
		}(start, end)
		start = end
		end += 1000000
	}

}

func main() {

	data, err := ioutil.ReadFile("block.txt")
	if err != nil {
		panic(err)
	}
	GetBestZeros(data)

	// Wait for SIGINT and SIGTERM (HIT CTRL-C)
	ch := make(chan os.Signal)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	log.Println(<-ch)

	fmt.Println()
	fmt.Println("Stop Hashing...")
}

//build
//env GOOS=windows go build .
//env GOOS=windows GOARCH=386 go build .
