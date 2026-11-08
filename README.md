# NyistAuthSrunBypass

> ## ⚠️ 本项目已归档
>
> **功能已合并到 [ilylty/AuthingNYIST](https://github.com/ilylty/AuthingNYIST)，请改用新项目。**
>
> 本仓库不再维护，代码保留仅供存档。

南阳理工学院（NYIST）校园网 srun 认证。原来的 Python 脚本依赖 `execjs` 在运行时执行 `a.js` 来生成加密参数，部署麻烦；现在这部分已经用 Go 重写，编译成单文件二进制，没有运行时依赖，可以在路由器、树莓派、NAS、手机 Magisk 模块上跑。

## 为什么迁移

| | 本仓库（Python） | [AuthingNYIST](https://github.com/ilylty/AuthingNYIST)（Go） |
| --- | --- | --- |
| 依赖 | Python 3 + `requests` + `pyexecjs2` + Node.js | 无，单个静态二进制 |
| 加密参数 | 运行时 `execjs` 调 `a.js` | 原生 Go 实现，无需 JS 引擎 |
| 平台 | 有 Python 的机器 | Linux / Windows / macOS，13 种架构 |
| 掉线检测 | 单一线程轮询 `122.207.209.6:8080` | 可配置 HTTP/TCP 探测 + 失败重试 + 自动重连 |
| 代理共存 | 不处理 | 可绑定校园网卡，绕开 TUN 全局代理的误判 |
| 开机自启 | 自己写 | systemd / OpenWrt init.d / Magisk 模块 |
| 设备名伪装 | 硬编码 `os=不想996&name=Windows` | `--os` / `--device-name` 可配置 |

## 新版用法

### 直接下载

从 [Releases](https://github.com/ilylty/AuthingNYIST/releases) 下载对应平台的二进制。

### 简单认证

```bash
./auth-nyist -u 学号 -p 密码
```

### 保持在线

```bash
./auth-nyist -u 学号 -p 密码 keepalive
```

### 配置文件

写到 `~/.config/auth-nyist` 或 `~/.auth-nyist`：

```json
{
  "username": "你的学号",
  "password": "你的密码",
  "keepOnline": true
}
```

### 挂了代理（Clash / Hiddify / sing-box 开了 TUN）

这时全局路由被 TUN 接管，普通的 TCP 探测会被代理在本地应答，导致掉线检测永远显示"在线"。新版支持绑定网卡绕开：

```json
{
  "adapter": "wlan0",
  "dns": "59.69.128.96",
  "keepOnline": true
}
```

`adapter` 也可以写 `auto` 自动选默认路由上的无线网卡。`dns` 是为了避免 fake-ip 模式把 `auth.nyist.edu.cn` 解析成 `198.18.x.x` 后绑网卡就不可达。

### 原来的 `os` / `name` 参数

旧脚本第 123 行硬编码的 `os=不想996&name=Windows`，新版变成参数：

```bash
./auth-nyist --os "不想996" --device-name "Windows" -u 学号 -p 密码
```

默认发送 `auth-nyist-cli`。愚人节（4 月 1 日）会自动换成一个随机设备名，可用 `--no-egg` 关闭。

## 迁移对照表

| 旧脚本 | 新版 |
| --- | --- |
| `python enc.py` | `auth-nyist keepalive` |
| 改 `enc.py` 第 9-10 行填账号密码 | `-u` / `-p` 参数或配置文件 |
| `connectAuth()` 递归重认证 | 内置失败重试 |
| `check_connection1()` 单线程轮询 | 可配置 `interval` / `timeout` / `retries` |
| `os=不想996&name=Windows` | `--os` / `--device-name` |
| 需要常驻后台 | systemd / init.d / Magisk `service.sh` |

## 完整文档

安装、配置、自启动、代理共存、故障排查都在新仓库：

**<https://github.com/ilylty/AuthingNYIST>**

## 许可证

本仓库原内容保留在此仅供存档。新项目使用 GPLv3。
