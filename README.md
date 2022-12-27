# Python에서 rust 사용하기 

rust로 모듈을 만들고 python에서 모듈을 사용하는 예제이다. 원문은 [Rust in Python](https://weeklyit.code.blog/2020/01/03/2020-1%EC%9B%94-1%EC%A3%BC-rust-in-python/)을 참고한다. 

## 프로젝트 생성
다음과 같이 프로젝트를 생성한다. 
```shell
cargo new from-python --lib
```

이 프로젝트의 소스는 [여기](https://github.com/latteonterrace/rust-python.git)를 참고한다. 




## no_mangle

컴파일러는 컴파일을 할 때 함수명을 일정한 규칙에 따라 바꿔주는 작업을 하며 이를 Name Mangling이라고 한다. 그런데 우리는 이 함수를 Rust가 아닌 Python에서 실행해야 하므로 Rust 스타일의 함수명이 아닌 C 스타일의 함수명이 필요하다. 왜냐하면 우리가 나중에 Python에서 Rust 라이브러리를 로드하기 위해 사용할 도구(FFI)는 C로 작성된 라이브러리를 로드할 때 사용하는 도구이기 때문이다. 따라서 #[no_mangle]이라는 flag를 붙이면 일단 우리가 작성한 함수를 Rust 스타일의 함수명으로 바꾸는 작업을 생략한다. 

```rust
// lib.rs
#[no_mangle]
extern fn hello() {
    println!("Hello from rust");
}
```
extern 키워드는 Rust에서 이 함수가 외부 언어에서 호출될 수 있음을 알려주는 키워드이다. 
> extern 키워드는 두 곳에서 사용된다. 하나는 crate 키워드 와 함께 사용하여 Rust 코드가 프로젝트의 다른 Rust 상자를 인식하도록한다. 다른 용도는 FFI (외부 함수 인터페이스)이다. 

## 컴파일하기 

lib.rs를 컴파일하면 되는데, 이 코드를 그냥 컴파일하면 확장자가 *.rlib이라는 파일이 생긴다.  *.rlib은 Rust Static 라이브러리 파일을 뜻하는 확장자이며 이 라이브러리는 Rust에서만! 사용할 수 있다.  이 라이브러리를 다른 언어에서 사용할 수 있도록 Dynamic 라이브러리 파일로 컴파일해야 한다. 그래야 이 라이브러리를 Python의 외부 함수 인터페이스(FFI)가 인식하도록 하여 Python에서 Import할 수 있다. 


> Foreign Function Interface의 앞머리 알파벳을 딴 약자다.**한 프로그래밍 언어(이하 A)에서 다른 프로그래밍 언어(이하 B)의 코드를 호출하기 위한 인터페이스**를 말한다. A로는 불가능한 일이 B로는 가능한 경우, A로는 비효율적인 일이 B로는 효율적인 경우, B로 쓰여진 코드가 이미 제공하는 기능을 A로의 번역없이 그대로 사용하고 싶은 경우 등에서 A는 FFI를 통해 B의 코드를 이용할 수 있다. C언어는 역사가 오래 되었을 뿐만 아니라 그 동안 축적된 코드베이스(code base)가 풍부하므로 많은 언어들이 C언어로 작성한 코드를 사용하기 위한 FFI를 가지고 있다.


lib.rs를 Dynamic 라이브러리로 컴파일하려면 Cargo.toml 파일에 다음을 추가한다. 
```toml
[lib]
crate-type = ["dylib"]
```

이제, cargo를 통해 이 코드를 컴파일한다. 
```shell
cargo build --release
```

## main.py 

main.py를 생성하고 다음과 같이 작성한다. 
```python
# main.py
from ctypes import CDLL
 
# linux 
# lib = CDLL("target/release/librust_in_python.dylib")
# windows
lib = CDLL("target/release/librust_in_python.dll")
lib.hello()
```

파이썬의 ctypes 라이브러리가 바로 파이썬의 외부 함수 인터페이스(FFI) 중 하나이다. 이 라이브러리는 CDLL이라는 클래스를 통해 사용자가 C로 작성된 라이브러리를 파이썬에 로드할 수 있게 한다. 

## 프로젝트 구조
프로젝트 구조는 다음과 같을 것이다. 
```shell
📂from-python
  📂src 
    📄lib.rs
  📄Cargo.toml
  📄main.py 
```



