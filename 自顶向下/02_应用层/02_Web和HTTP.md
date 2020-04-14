## 1:HTTP概况
Web的应用层协议是 **超文本传输协议** (HTTP)。客户程序和服务器程序通过交换HTTP报文进行会话。

Web浏览器为HTTP的客户端，也就是平时用的Firefox，Chrome等等；Web服务器实现了HTTP的服务器端。

HTTP使用TCP作为它的支撑运输协议。
  - 客户首先发起一个与服务器的TCP连接，一旦建立成功，两个进程就可以通过套接字接口访问TCP。
  - 也就是说，应用层的HTTP协议通过套接字发送完数据之后，就交付给TCP去管理控制了，这里体现了分层的优势，就是HTTP协议发送出去就完事了，不用担心数据是不是会丢失，因为都交给TCP了

服务器向客户发送被请求的文件，而不存储任何关于该客户的状态信息。
  - 举个栗子：比如我打开www.baidu.com , 加载成功之后又刷新页面请求www.baidu.com，服务器还是会给我新的对象，而不是说第一次返回好了就不给了。
  - HTTP是一个 **无状态协议**
## 2：非持续连接和持续连接
### 2.1：非持续连接
  - 每个请求/响应对是经过一个单独的TCP连接发送
  - 非持续连接的使用过程
    举个栗子：服务器向客户传送一个Web页面，此页面内容有HTML文件和10个JPEG的图形。HTML文件地址为：http://www.test2020.wyb/home.index
    - 1：HTTP客户进程在端口号80发起一个到服务器www.test2020.wyb的TCP连接
    - 2：HTTP客户端经过它的套接字向服务器发送一个HTTP请求报文。
    - 3：HTTP服务器进程经过它的套接字接收到请求报文，根据传递过来的链接，在字节内存中找到该对象(home.index)，再在HTTP响应报文中封装对象，并通过其套接字向客户发送响应报文
    - 4：HTTP服务器进程通知TCP断开该TCP连接。（知道TCP确认客户已经完整地收到响应报文为止，才会断开）
    - 5：对每一个引用的JPEG图形对象重复上述步骤
  - 特点：
    - 每个TCP连接在服务器发送一个对象后关闭
    - 每个TCP连接只传输一个请求报文和一个相应报文
  - **往返时间** (RTT Round-Trip Time)
    - 指一个短分组从客户到服务器再返回客户所花费的时间
    - 包括：分组传播时延、分组在中间路由器和交换机上的排队时延以及分组处理时延
### 2.2：持续连接(默认)
  - 所有的请求及其响应经过相同的TCP连接发送
  - 如果一条连接经过一定时间间隔（可配置）仍未被使用，HTTP服务器就关闭该连接

## 3：HTTP报文格式
### 3.1：请求报文
```
GET /somedir/page.html HTTP/1.1
Host: www.someschool.edu
Connection: close
User-agent: Mozilla/5.0
Accept-language: fr

```
- 请求行：HTTP请求报文的第一行
  ```
  GET /somedir/page.html HTTP/1.1
  ```
  - 包含三个字段：方法字段、URL字段和HTTP版本字段
  - 方法字段：GET、POST、HEAD、PUT和DELETE，绝大多数使用GET方法
    - HEAD方法和GET类似，常用调试
    - PUT常与Web发行工具联合使用，允许用户上传对象到指定的Web服务器上的指定路径。
    - DELETE允许用户或者应用程序删除Web服务器上的对象
- 首部行：请求行的后面的行
  - Host
    ```
    Host: www.someschool.edu
    ```
    指明了对象所在的主机

  - Connection
    ```
    Connection：close
    ```
    表示浏览器告诉服务器再发送完被请求的对象之后就关闭连接
  - User-agent
    指明用户代理，即向服务器发送请求的浏览器的类型。此处是Mozilla/5.0，表示FIrefox浏览器，很有必要的，因为此行能够保证发送给不同的浏览器同一种对象的不同版本（可以理解为兼容性）
  - Accept-language
    表示用户想得到该对象的语言版本（如果有的话）
- 请求报文的通用格式

  ![](assets/markdown-img-paste-2020041415230941.png)

  - 注意上面多出来的实体主体，对于GET方法实体主体为空，对于POST方法才使用该实体。

### 3.2：HTTP响应报文
```
HTTP/1.1 200 OK
Connection：close
Date: Tue, 09 Aug 2011 15:44:04 GMT
Server: Apache/2.2.3 (CentOS)
Last-Modified: Tue, 09 Aug 2011 15:11:03 GMT
Content-Length: 6821
Content-Type: text/html

(data data data data data...)
```
- 状态行
```
HTTP/1.1 200 OK
```
  - 协议版本字段
  - 状态码
    >200 OK : 请求成功，信息在返回的响应报文中
    >301 Moved Permanently: 请求对象呗永久转义了，新的URL定义在相应报文的Location：首部行中
    >400 Bad Request: 该请求服务器不能理解，是一个通用的差错代码
    >404 Not Found: 被请求的文档不在服务器上
    >505 HTTP Version Not Supported：服务器不支持请求报文的HTTP版本协议


  - 相应状态信息
- 首部行
```
Connection：close
Date: Tue, 09 Aug 2011 15:44:04 GMT
Server: Apache/2.2.3 (CentOS)
Last-Modified: Tue, 09 Aug 2011 15:11:03 GMT
Content-Length: 6821
Content-Type: text/html
```
  - Connection
  ```
  Connection: close
  ```
  表示告诉客户，发送完报文将关闭该TCP连接
  - Date
  ```
  Date: Tue, 09 Aug 2011 15:44:04 GMT
  ```
  表示服务器产生并发送该响应报文的日期和时间，此时间指的是服务器从自身文件系统里面检索到要请求的对象，插入到响应报文，并 **发送该响应报文** 的时间
  - Server
  ```
  Server: Apache/2.2.3 (CentOS)
  ```
  服务器是Apache Web，类似于请求报文里面的User-agent
  - Last-Modified
  ```
  Last-Modified: Tue, 09 Aug 2011 15:11:03 GMT
  ```
  对象创建或者最后修改的日期和时间，此首部行在讨论缓存服务器（代理服务器）的时候很重要
  - Content-Length:
  ```
  Content-Length: 6821
  ```
  被发送对象的 **字节** 数
  - Content-Type
  ```
  Content-Type: text/html
  ```
  指示了实体体中的对象是HTML文本

- 实体体
```
(data data data data data...)
```
  包含了请求的对象本身

## 4:Cookie-用户与服务器的交互
cookie允许站点对用户进行跟踪，因为HTTP服务器是无状态的，cookie能保证内容与用户身份联系起来。

  ![](assets/markdown-img-paste-20200414154809121.png)

  
## 5：Web缓存
## 6：条件GET方法
