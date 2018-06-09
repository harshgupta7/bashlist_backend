package main 


import "path/filepath"
import "os"
import "fmt"
// import "runtime"
// import "bufio"
import "github.com/howeyc/gopass"



func DirSize(path string) (int64, error) {
    var size int64
    err := filepath.Walk(path, func(_ string, info os.FileInfo, err error) error {
        if !info.IsDir() {
            size += info.Size()
        }
        return err
    })
    return size, err
}

func Exists(name string) bool {
    if _, err := os.Stat(name); err != nil {
    if os.IsNotExist(err) {
                return false
            }
    }
    return true
    """dsds"""
}

func main() {
	// var s string="pr_per_day.csv"
	// c,e:=DirSize(s)
	// if e!=nil{
	// 	fmt.Println("kkr")
	// }
	// fmt.Println(c)

	// var s string="pr_per_day.csv"
	// var t string="velocitysdsd"
	// a:=Exists(s)
	// b:=Exists(t)
	// fmt.Println(a)
	// fmt.Println(b)

	// if runtime.GOOS == "darwin" {
	//     fmt.Println("Mac OS detected")
	//  }
	// reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter text: ")
	pass, _ := gopass.GetPasswd()
	var s string=pass
	fmt.Println(pass)
}
