# 基于Python的东晟校园生活充电方式

## 背景

学校内有一批老旧充电桩由东晟校园生活 APP 运营，但自从该公司倒闭，无力支付库克的 99 刀而被 AppStore 下架以来，如何充电就变成了老大难，**苹果用户只要到处借账号下载就好了，而安卓用户直接侧载要考虑的可就多了**. 虽然学校声称将在[五月完成电动车充电桩的全部更换](https://shuiyuan.sjtu.edu.cn/t/topic/224032/28)，但鉴于学校一贯拖工期的作风，哥们决定自己动手，丰衣足食，作为过渡时期的下位替代.

## 使用方法

0. 将项目下载到本地并安装依赖

    ```shell
    git clone
    cd campuslife
    pip install -r requirements.txt
    ```

1. 登录

    执行
    ```shell
    python main.py login
    ```
    输入手机号和密码，登录成功后会保存用户信息到本地.

2. 充电

    执行
    ```shell
    python main.py charge
    ```
    输入充电桩编号 (后8位或全16位)，即可开始充电.

3. 通知推送

    通知推送基于 [Bark APP](https://bark.day.app/)，使用方式:

    1. 在 iPhone 上下载 [Bark APP][] 并获取设备密钥.

        [Bark APP]: https://apps.apple.com/us/app/bark-%E7%BB%99%E4%BD%A0%E7%9A%84%E6%89%8B%E6%9C%BA%E5%8F%91%E6%8E%A8%E9%80%81/id1403753865?l=zh-Hans-CN
        ![Bark APP](./assets/images/bark.png)
        
    2. 将设备密钥保存到 `configs.json` 文件中.
        ```json
        {"bark": {"device_key": "YOUR_DEVICE_KEY"}}
        ```
    3. 执行脚本即可将消息推送到 iPhone.
        ```shell
        python bark.py
        ```
    4. 可以通过创建定时任务实现自动推送.

> ?: 如何在 iPhone 上使用脚本？
> a: 可以下载 python shell 类 APP (eg. a-Shell)，将脚本拷贝到文件目录中执行.

### to do list

1. 历史记录查询
    - [] 充值记录
    - [] 充电记录
2. 氪金接口：支付宝
    - [] 充值
    - [] 退费
3. 用户信息
    - ~~注册 & jAccount 绑定~~ (目测因为服务器无法发送验证码而再也无法实现)
    - ~~账户安全 (修改密码、绑定手机)~~
    - [] 修改个人信息 (头像、用户名、性别)

## 原理解析

通过网络抓包与对 APK 逆向解包分析，东晟校园生活 APP 主要通过 HTTP POST 请求与服务器进行通信. 通过模拟请求，我们可以借助脚本实现充电、查看充电桩状态、查看充电状态等功能.

### 加密算法

东晟校园生活 APP 会对请求 body 进行加密，加密算法如下：

1. 将明文字符串转换为 GBK 编码的字节.
2. 填充数据以匹配 DES 块大小.
3. 使用 CBC 模式的 DES 加密数据.
4. 执行 Base64 编码.
5. 对数据进行 URL 编码以进行数据传输.

## 致谢

感谢 ChatGPT、GitHub Copilot 对本项目的大力支持
