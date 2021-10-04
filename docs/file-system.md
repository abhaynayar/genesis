## File System

- The file system is stored in `disk.img`.
- The file system will store the files one after the other.
- The files are separated by `---`.
- File starts with file headers.
- Then after a line gap we get the contents.
- The contents of weird files are base64 encoded.


An example file system snapshot:

```
name: zero.ch8
encoding: base64

YAplBWYKZw9oFGEBYgFjAWQBYAqieNBWcAqiftBmcAqihNB2cAqiitCGagP6FWAKonjQVkUUYf9F
AWEBhRTQVnAKon7QZkYUYv9GAWIBhiTQZnAKooTQdkcUY/9HAWMBhzTQdnAKoorQhkgUZP9IAWQB
iETQhhIq/wMMMMD//8DA/MD/8MzM8MzDPMPDw8M8

---

name: hello.txt
encoding: ascii

this is a text file.
```


