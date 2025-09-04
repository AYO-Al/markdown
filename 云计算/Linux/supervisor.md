[Supervisor](https://github.com/Supervisor/supervisor) 是一个用 Python 写的进程管理工具，可以很方便的用来在 UNIX-like 系统（不支持 Windows）下启动、重启（自动重启程序）、关闭进程（不仅仅是 Python 进程）。

- 安装：`apt-get install supervisor` / `pip install supervisor`

Supervisor 是一个用 Python 编写的​**​进程管理工具​**​，用于在类 Unix 系统上监控和控制应用程序进程。它能在进程异常退出时自动重启，确保关键服务持续运行，并提供了集中式的管理方式

它的核心价值在于：​**​将你需要手动维护的进程，转变为由守护进程自动监控和管理的服务​**​。

Supervisor 系统主要由以下四个部分组成

1. ​**​supervisord​**​：​**​服务端守护进程​**​。这是 Supervisor 的核心，负责启动所管理的子进程，响应客户端的命令，并在子进程异常退出时自动重启。它是所有被管理进程的父进程。
2. ​**​supervisorctl​**​：​**​命令行客户端​**​。为用户提供一个与 `supervisord` 交互的界面（类似 shell），通过它可以查看进程状态、启动、停止、重启进程。
3. ​**​Web Server​**​：​**​Web 管理界面​**​。提供了一个通过浏览器访问的 GUI，通常运行在 `9001` 端口，功能与 `supervisorctl` 类似。
4. ​**​XML-RPC Interface​**​：​**​编程接口​**​。提供了 XML-RPC API，允许开发者通过编程方式查询和控制进程，便于集成到其他运维工具或自动化脚本中。

`supervisord` 作为核心守护进程，通过 `fork/exec` 的方式启动和管理所有配置好的子进程，并时刻监视它们的状态。
# 配置

- ​**​主配置文件​**​：`/etc/supervisord.conf`
- **​子进程配置目录​**​：`/etc/supervisord.d/` 或 `/etc/supervisor/conf.d/`。通常在主配置文件中通过 `[include]` 节引入此目录下的所有 `*.conf` 文件，便于管理多个应用

`supervisor`启动时未指定`-c`选项时，会按照以下顺序查看配置文件。

1. `../etc/supervisord.conf` (Relative to the executable)
    
2. `../supervisord.conf` (Relative to the executable)
    
3. `$CWD/supervisord.conf`
    
4. `$CWD/etc/supervisord.conf`
    
5. `/etc/supervisord.conf`
    
6. `/etc/supervisor/supervisord.conf` (since Supervisor 3.3.0)
## 应用配置

| **配置块​**​                           | ​**​主要作用​**​                                                          | ​**​常用配置项及说明​**​                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                         |
| ----------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| ​**​`[unix_http_server]`​**​        | 配置本地 UNIX Socket 通信，供 `supervisorctl` 命令行工具使用<br><br>。                | • `file=/var/run/supervisor.sock`: Socket 文件路径<br><br>。  <br>• `chmod=0700`: Socket 文件权限<br><br>。  <br>• `chown=nobody:nogroup`: Socket 文件属主和属组<br><br>。  <br>• `username` & `password`: 连接认证（可选）<br><br>。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                         |
| ​**​`[inet_http_server]`​**​        | 启用 Web 管理界面，可通过浏览器查看和管理进程<br><br>。                                    | • `port=127.0.0.1:9001`: 监听IP和端口（设置为 `0.0.0.0:9001` 可从网络访问）<br><br>。  <br>• `username=admin`: 登录用户名<br><br>。  <br>• `password=your_password`: 登录密码<br><br>。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                         |
| ​**​`[supervisord]`​**​             | `supervisord` ​**​主进程​**​ 的全局配置，如日志、PID文件等<br><br>。                   | • `logfile=/var/log/supervisor/supervisord.log`: 主进程日志路径<br><br>。  <br>• `logfile_maxbytes=50MB`: 单个日志文件最大容量<br><br>。  <br>• `logfile_backups=10`: 日志备份数量<br><br>。  <br>• `pidfile=/var/run/supervisord.pid`: PID 文件路径<br><br>。  <br>• `nodaemon=false`: 以守护进程方式运行<br><br>。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                         |
| ​**​`[supervisorctl]`​**​           | 配置 `supervisorctl` ​**​客户端​**​ 如何连接到服务端<br><br>。                      | • `serverurl=unix:///var/run/supervisor.sock`: 通过 UNIX socket 连接（默认方式）<br><br>。  <br>• `serverurl=http://127.0.0.1:9001`: 通过 HTTP 连接（需与 `[inet_http_server]` 配置一致）<br><br>。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                         |
| ​**​`[program:*]`​**​  <br>_(最重要)_  | 定义要管理的​**​应用程序​**​，这是最常用的配置块。`*`代表程序名，如 `[program:myapp]`<br><br>。    | • `command=/path/to/your/command`: ​**​启动命令​**​（必须为​**​前台​**​非守护模式）<br><br>。  <br>• `directory=/path/to/workdir`: 命令执行时的工作目录<br><br>。  <br>• `user=www-data`: 以指定用户身份运行进程<br><br>。  <br>• `autostart=true`: Supervisor 启动时，该程序是否自动启动<br><br>。  <br>• `autorestart=true/unexpected`: 程序退出后是否自动重启（推荐 `unexpected`，仅在非预期退出时重启）<br><br>。  <br>• `startsecs=5`: 进程启动后持续运行5秒则认为成功<br><br>。  <br>• `startretries=3`: 启动失败后的重试次数<br><br>。  <br>• `stopsignal=TERM`: 停止进程时发送的信号<br><br>。  <br>• `stopwaitsecs=10`: 发送停止信号后等待强制杀死的秒数<br><br>。  <br>• `stdout_logfile=/path/to/logfile.log`: 标准输出日志路径<br><br>。  <br>• `stderr_logfile=/path/to/error.log`: 标准错误日志路径<br><br>。  <br>• `redirect_stderr=true`: 将 stderr 重定向到 stdout，便于日志统一管理<br><br>。  <br>• `environment=KEY="value"`: 设置环境变量（如 `PATH="/usr/bin"`）<br><br>。 |                                                         |
| ​**​`[group:*]`​**​                 | 将多个 `[program]` 合并成一个组，方便统一管理（启动、停止）<br><br>。                         | • `programs=progname1,progname2`: 包含的程序名称列表<br><br>。  <br>• `priority=999`: 组启动的优先级（值越小优先级越高）<br><br>。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                         |
| ​**​`[include]`​**​                 | 包含其他配置文件，实现配置的模块化管理，是​**​最佳实践​**​<br><br>。                            | • `files = /etc/supervisor/conf.d/*.conf`: 包含指定目录下的所有 `.conf` 文件。通常将每个程序的配置单独放在此目录下<br><br>。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                         |
| ​**​`[rpcinterface:supervisor]`​**​ | 定义 RPC（远程过程调用）接口，供 Web 界面和 `supervisorctl` 使用，​**​通常无需修改​**​<br><br>。 | • `supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface`: 标准配置，保持默认即可<br><br>。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                         |
| 配置块 (Section)                       | 是否必须                                                                  | 主要作用                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 备注                                                      |
| ​**​`[unix_http_server]`​**​        | ​**​否​**​                                                             | 配置用于本地通信的 UNIX Socket，供 `supervisorctl` 命令行工具使用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 禁用后，`supervisorctl` 将无法连接，但 `supervisord` 仍可运行。         |
| ​**​`[inet_http_server]`​**​        | ​**​否​**​                                                             | 启用 Web 管理界面，可通过浏览器查看和管理进程。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 默认不开启，需取消注释并配置才生效。                                      |
| ​**​`[supervisord]`​**​             | ​**​是​**​                                                             | ​**​全局配置核心​**​。定义 `supervisord` ​**​主进程​**​ 自身的参数，如日志、PID 文件等。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 如果没有该块，`supervisord` 将无法正常运行或无法确定其行为。                   |
| ​**​`[rpcinterface:supervisor]`​**​ | ​**​是​**​                                                             | 定义 RPC（远程过程调用）接口，是 ​**​Web 界面和 `supervisorctl` 能够工作的基础​**​。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 官方注明必须保留此部分。                                            |
| ​**​`[supervisorctl]`​**​           | 否                                                                     | 配置 `supervisorctl` ​**​客户端​**​ 如何连接到 `supervisord` 服务端。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 不配置时会尝试使用默认连接方式。                                        |
| ​**​`[program:*]`​**​               | 功能上必需                                                                 | 定义要管理的​**​应用程序​**​。这是你添加需要被监控和管理服务的地方。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | 没有 `[program:*]` 或 `[group:*]` 块，Supervisor 就没有需要管理的进程。 |
| ​**​`[group:*]`​**​                 | 否                                                                     | 将多个 `[program]` 归为一个组，方便统一管理。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 用于逻辑管理，非必需。                                             |
| ​**​`[include]`​**​                 | ​**​强烈推荐​**​                                                          | 包含其他配置文件（如 `/etc/supervisor/conf.d/*.conf`），实现配置的模块化管理。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | ​**​最佳实践​**​。将每个程序的配置放在单独文件中，便于管理。                      |

- 识别所有 `[program:*]` 块 → 转换为 ​**​ProcessConfig​**​ 对象
- 识别所有 `[group:*]` 块 → 转换为 ​**​GroupConfig​**​ 对象
- 建立 program 与 group 的映射关系

在 `/etc/supervisord.d/` 目录下为你的应用创建一个配置文件，例如 `my_app.conf`：

```ini
; 定义一个名为 my_app 的程序
[program:my_app]
; 最重要的配置：要执行的命令
command=/usr/bin/python /path/to/your/app.py

; 程序运行所在目录
directory=/path/to/your

; 是否随 supervisord 启动而自动启动
autostart=true

; 程序退出后是否自动重启。可选：false, true, unexpected（仅在意外退出时重启）
autorestart=true

; 启动后持续多少秒不退出则认为启动成功（默认 1）
startsecs=5

; 启动失败重试次数（默认 3）
startretries=3

; 运行程序的用户
user=www-data

; 标准输出和错误输出的日志文件
stdout_logfile=/var/log/my_app.stdout.log
stderr_logfile=/var/log/my_app.stderr.log

; 环境变量
environment=PATH="/usr/bin",LANG="en_US.UTF-8"
```

- `command`：必须​**​非后台运行​**​。Supervisor 需要通过管理前台进程来跟踪状态。若命令本身有 `&` 或类似 `-d` 的参数，需去除。
- `autorestart`：设为 `true` 或 `unexpected` 是实现“自动重启”核心功能的关键。
- `stdout_logfile`, `stderr_logfile`：Supervisor 会捕获并重定向子进程的输出到这些日志文件，并支持日志轮转（`maxbytes`, `backups`）。
# 命令行

|命令|作用|示例|
|---|---|---|
|​**​`supervisorctl status`​**​|​**​查看所有进程状态​**​（最常用）|`supervisorctl status`|
|​**​`supervisorctl start <name>`​**​|启动某个进程|`supervisorctl start celery_worker`|
|​**​`supervisorctl stop <name>`​**​|停止某个进程|`supervisorctl stop web_app`|
|​**​`supervisorctl restart <name>`​**​|重启某个进程|`supervisorctl restart nginx`|
|​**​`supervisorctl signal <name>`​**​|向进程发送信号|`supervisorctl signal nginx STOP`|
## 状态解读

`supervisorctl status` 的输出结果通常如下：

```bash
celery_worker                 RUNNING   pid 2935, uptime 1:05:34
web_app                       STARTING   # 正在启动
async_io                      STOPPED    Nov 30 04:00 PM  # 已停止
redis_cache                   BACKOFF    Exited too quickly; see log  # 启动失败
nginx                         FATAL      Exited too quickly; see log  # 致命错误
```

常见状态：

- `RUNNING`: 进程正常运行中。
- `STARTING`: 进程正在启动。
- `STOPPED`: 进程已停止。
- `BACKOFF`: 进程启动失败，正在重试（检查 `startretries` 配置）。
- `FATAL`: 进程启动失败，且重试次数已用尽。
- `EXITED`: 进程正常退出（但 `autorestart` 可能又会把它拉起来）。
## 批量管理

当配置了 `[group:*]` 块时，可以对整个组进行操作。

| 命令                                        | 作用         | 示例                                   |
| ----------------------------------------- | ---------- | ------------------------------------ |
| ​**​`supervisorctl start <group>:*`​**​   | 启动组内所有进程   | `supervisorctl start web_services:*` |
| ​**​`supervisorctl stop <group>:*`​**​    | 停止组内所有进程   | `supervisorctl stop workers:*`       |
| ​**​`supervisorctl restart <group>:*`​**​ | 重启组内所有进程   | `supervisorctl restart all:*`        |
| ​**​`supervisorctl status <group>:*`​**​  | 查看组内所有进程状态 | `supervisorctl status data_sync:*`   |
| ​**​`supervisorctl start all`​**​         | 启动所有进程     | `supervisorctl start all`            |
| ​**​`supervisorctl stop all`​**​          | 停止所有进程     | `supervisorctl stop all`             |
| ​**​`supervisorctl restart all`​**​       | 重启所有进程     | `supervisorctl restart all`          |
## 配置更新与重载

修改任何配置文件后，必须使用这些命令使更改生效。

| 命令                             | 作用                                                                                   | 示例                     |     |
| ------------------------------ | ------------------------------------------------------------------------------------ | ---------------------- | --- |
| ​**​`supervisorctl reread`​**​ | ​**​重新读取配置​**​文件。检测是否有新增或修改的进程配置，但​**​不会重启​**​任何已有进程。                                | `supervisorctl reread` |     |
| ​**​`supervisorctl update`​**​ | ​**​更新进程​**​。根据 `reread` 的结果，启动​**​新添加​**​的进程，​**​重启​**​配置有变动的进程。对无变动的进程无影响。         | `supervisorctl update` |     |
| ​**​`supervisorctl reload`​**​ | ​**​重启 supervisord 主进程​**​本身，并重新加载整个配置文件。这会中断所有现有连接，并重新启动所有配置为 `autostart=true` 的进程。 | `supervisorctl reload` |     |
**可以结合reread和update更新修改过配置的进程**。
## 日志查看

用于实时监控或排查进程问题。

| 命令                                            | 作用                                | 示例                                     |
| --------------------------------------------- | --------------------------------- | -------------------------------------- |
| ​**​`supervisorctl tail <name>`​**​           | 查看进程的最后日志（默认 stdout）              | `supervisorctl tail redis`             |
| ​**​`supervisorctl tail -f <name>`​**​        | ​**​持续跟踪​**​（follow）进程的 stdout 日志 | `supervisorctl tail -f web_app`        |
| ​**​`supervisorctl tail -f <name> stderr`​**​ | 持续跟踪进程的 stderr（错误）日志              | `supervisorctl tail -f web_app stderr` |
| ​**​`supervisorctl tail -f <name> stdout`​**​ | 明确指定持续跟踪 stdout（标准输出）日志           | `supervisorctl tail -f celery stdout`  |