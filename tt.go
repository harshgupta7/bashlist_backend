package main
import "github.com/dchest/uniuri"
import "fmt"
func main(){
	s := uniuri.NewLen(32)
	fmt.Println(s)

}	