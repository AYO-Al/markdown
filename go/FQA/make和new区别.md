- `make` 的作用是初始化内置的数据结构，也就是我们在前面提到的切片、哈希表和 Channel
- `new` 的作用是根据传入的类型分配一片内存空间并返回指向这片内存空间的指针

### 内存分配和初始化

- **内存分配**：为变量分配内存空间，使其能够存储数据。
- **初始化**：为分配的内存空间赋予初始值。

### `new` 函数的行为

`new` 函数用于分配内存，并返回指向该内存的指针。它分配的内存会被置零（即所有字节都被设置为零值），但不会进行进一步的初始化。

#### 使用 `new` 分配内存


```go
package main  
import "fmt"  
func main() {     
// 使用 new 分配内存     
    p := new(int)     
    fmt.Println(*p) // 输出: 0      
    // 修改指针指向的值     
    *p = 10     
    fmt.Println(*p) // 输出: 10 
}
```

在这个例子中，`new(int)` 分配了一个 `int` 类型的内存，并返回一个指向该内存的指针。初始值是 `0`，因为 `new` 分配的内存会被置零。

### `make` 函数的行为

与 `new` 不同，`make` 函数不仅分配内存，还会对内建类型（slice、map 和 channel）进行初始化，使其可以正常使用。

#### 使用 `make` 初始化 `map`


```go
package main  
import "fmt"  
func main() {     
    // 使用 make 初始化 map     
    m := make(map[string]int)     
    m["key"] = 1     
    fmt.Println(m) // 输出: map[key:1] 
    }
```

在这个例子中，`make(map[string]int)` 不仅分配了内存，还初始化了 `map`，使其可以存储键值对。

### `new` 和 `make` 的区别

1. **用途**：
    
    - `new`：用于分配任意类型的内存，并返回指向该内存的指针。
    - `make`：用于分配和初始化内建类型（slice、map 和 channel）。
2. **返回值**：
    
    - `new`：返回指向分配内存的指针。
    - `make`：返回初始化后的类型本身（不是指针）。
3. **初始化**：
    
    - `new`：只做内存分配，分配的内存会被置零，但不进行进一步的初始化。
    - `make`：分配内存并进行初始化，使内建类型可以正常使用。

### 示例对比

#### 使用 `new` 分配内存

```go
package main  
import "fmt"  
type Person struct {     
    Name string     
    Age  int }  
func main() {     
    // 使用 new 分配内存     
    p := new(Person)     
    fmt.Println(*p) // 输出: { 0}      
    // 修改指针指向的值     
    p.Name = "Alice"     
    p.Age = 30     
    fmt.Println(*p) // 输出: {Alice 30} 
    }
```

#### 使用 `make` 初始化 `map`


```go
package main  
import "fmt"  
func main() {     
    // 使用 make 初始化 map     
    m := make(map[string]int)     
    m["key"] = 1     
    fmt.Println(m) // 输出: map[key:1] 
    }
```

### 总结

- **`new`**：分配内存并返回指向该内存的指针，分配的内存会被置该类型零值，但不进行进一步的初始化。
- **`make`**：分配内存并初始化内建类型（slice、map 和 channel），使其可以正常使用。