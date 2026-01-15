# 如何安装helm

- 下载 `helm` 二进制包：下载 Helm 客户端的二进制版本。 [官方发布页面](https://github.com/helm/helm/releases) 。

- 使用 `tar` 命令解压压缩包

- 移动helm可执行二进制文件：`mv linux-amd64/helm /usr/local/bin/helm`

# 什么是helm

Helm 是 Kubernetes 的**包管理器**，你可以把它想象成 Kubernetes 生态里的 “yum” 或 “apt-get”。它的核心价值在于，将复杂的 Kubernetes 应用及其依赖打包成一个标准化的单元（称为 **Chart**），让你能够像安装普通软件一样，轻松地部署、升级和管理运行在 Kubernetes 上的应用程序。

下面这个表格能帮你快速抓住 Helm 的核心要点。

|特性维度|核心概念|要解决的核心问题|
|---|---|---|
|**打包与分发**​|**Chart (图表)**：一个预先配置好的应用包，内含所有Kubernetes资源文件的模板和默认配置。|解决“部署文件太多太散”的问题。它将一个应用所需的所有YAML文件组织在一起，便于分享和版本化管理。|
|**部署与实例**​|**Release (发布)**：每次用Chart在集群中安装应用，都会创建一个唯一的Release。同一个Chart可以多次安装，形成多个独立的实例。|解决“一套配置多环境部署”的问题。你可以用同一个Chart，通过不同的配置（如测试环境、生产环境），生成多个互不干扰的应用实例。|
|**定制与复用**​|**Values (值)**：一个YAML格式的配置文件（`values.yaml`），用于在安装时覆盖Chart中的默认参数（如镜像版本、副本数等）。|解决“配置与模板耦合”的问题。实现了应用配置和Kubernetes资源模板的分离，使一份模板能灵活适配不同场景。|
|**生命周期管理**​|**模板引擎与版本历史**：Helm使用Go模板引擎动态生成最终的Kubernetes清单文件，并保存每次发布的版本历史。|解决“应用升级回滚复杂”的问题。支持一键升级和回滚到任意历史版本，为应用发布提供了可靠的安全网。|
## 三大概念

**chart** 是 Helm 包。它包含在 Kubernetes 集群中运行应用程序、工具或服务所需的所有资源定义。这就像 Homebrew 的公式、Apt 的 dpkg 或 Yum 的 RPM 文件的 Kubernetes 等价物。

**Repository** 是收集和共享图表的地方。它类似于 Perl 的 CPAN 存储库 或 Fedora 软件包数据库 ，但针对 Kubernetes 软件包。

**Release** 是在 Kubernetes 集群中运行的 **chart** 实例。一个chart通常可以安装多次到同一个集群。每次安装，都会创建一个新的 Release 。

Helm 在 Kubernetes 中安装了 _charts_，为每个安装创建了一个新的 _release_。要查找新的 _chart_，可以搜索 Helm 图表的 _repositories_。

## 查找Charts

**Charts** 查找的命令如下：

|命令类别|命令示例|核心功能与运行机制|
|---|---|---|
|**从仓库搜索**​|`helm search repo [关键词]`|在你**已添加到本地的仓库**中搜索。它查询的是本地缓存的仓库索引文件（`index.yaml`），速度极快，无需联网。|
|**从中心搜索**​|`helm search hub [关键词]`|从 **Artifact Hub**（Helm 的官方图表中心）搜索。该命令会联网查询这个公共平台，发现所有已注册的公开 Charts。|
|**查看可用配置**​|`helm show values [仓库名/Chart名]`|查看某个 Chart **所有可配置的默认参数**。这能让你在安装前清晰了解如何定制化部署。|

### 本地仓库搜索

```bash
helm search repo [关键词] [选项]
```

这个命令是你最常用、最高效的查找方式，因为它基于你已经配置好的本地仓库数据。

- **命令如何运行**：当你使用 `helm repo add`添加一个仓库后，Helm 会将该仓库的索引文件（`index.yaml`）下载到本地缓存中。`helm search repo`就是在这个本地缓存中进行查询的，因此速度非常快，且不依赖网络。

> 使用技巧

- **支持模糊匹配**：你不需要输入完整的 Chart 名称，Helm 会进行模糊匹配。例如，想找 MySQL，输入 `helm search repo mysql`即可，它会列出所有包含 "mysql" 的 Charts。
    
- **查看所有版本**：想安装特定版本时，可以使用 `--versions`选项来列出该 Chart 的所有历史版本。

```bash
helm search repo prometheus/kube-prometheus-stack --versions
```

- **搜索特定仓库**：如果你添加了多个仓库，可以在关键词前指定仓库名来缩小搜索范围。

```bash
helm search repo bitnami/
```
### 从中心仓库搜索

```bash
helm search hub [关键词] [选项]
```

当你想探索新的、未被添加到本地的 Chart 时，这个命令是你的好帮手。

- **命令如何运行**：该命令会直接访问 **Artifact Hub**​ 的 API 进行搜索。Artifact Hub 是一个聚合了大量公有 Helm 仓库的中心化平台，你可以在这里找到几乎所有的公开 Charts。

- `helm search hub` 显示了在 [artifacthub.io](https://artifacthub.io/) 上的位置的 URL，但不显示实际的 Helm 仓库。 `helm search hub --list-repo-url` 显示了实际的 Helm 仓库 URL，当您想要添加新的仓库时，这非常有用：`helm repo add [NAME] [URL]`。
### 深入查看Chart详情

```bash
helm show values [仓库名/Chart名] [选项]
```

找到心仪的 Chart 后，安装前最重要的一步是查看它的可配置选项。

- **命令如何运行**：此命令会从仓库下载 Chart 的压缩包，并解析其中的 `values.yaml`文件，将其内容输出到终端。

> 使用技巧

- **重定向到文件**：默认输出内容可能很长，你可以将其保存到一个文件中，作为自定义配置的起点。
    
    ```bash
    helm show values bitnami/wordpress > my-values.yaml
    ```
    
    然后你就可以编辑 `my-values.yaml`文件，在安装时通过 `-f my-values.yaml`参数来使用你的自定义配置。

- **查看特定版本**：同样可以使用 `--version`选项来查看某个历史版本的默认值。

```bash
helm show values bitnami/wordpress --version 15.0.0
```
## 安装Charts

helm install的基本格式如下：

```bash
helm install [RELEASE_NAME] [CHART] [flags]
```

下面的表格详细解释了各个部分.

| 参数/选项                    | 说明与技巧                                                                                                                   | 示例                                                                            |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **`[RELEASE_NAME]`**​    | 为你这次安装的实例起个名字。如果不指定，可使用 `--generate-name`让 Helm 自动生成一个。**技巧**：建议起一个有意义的名字，如 `frontend-dev`，便于后续管理。                      | `helm install my-app ./my-chart`                                              |
| **`[CHART]`**​           | 指定要安装的 Chart 来源，非常灵活。                                                                                                   | - 从仓库：`bitnami/nginx`  <br>- 本地目录：`./my-chart`  <br>- 压缩包：`./nginx-1.0.0.tgz` |

你可以组合使用多种方式来为 Chart 提供配置，它们的优先级从低到高如下 ：

1. Chart 内部的 `values.yaml`文件（默认值）。
    
2. 用户提供的通过 `-f`指定的 Values 文件。如果指定了多个文件，**最右边文件的值优先级最高**。
    
3. 通过 `--set`传递的参数（优先级最高）。

如果 Chart 依赖其他子 Chart（在 `Chart.yaml`的 `dependencies`字段定义），在安装前记得运行 `helm dependency update [CHART的路径]`来下载这些依赖 。

- 常用选项：

|**选项**|**简写**|**说明**|
|---|---|---|
|`--values`|`-f`|指定一个 YAML 文件覆盖默认配置（支持多个，右侧优先）|
|`--set`|无|通过命令行直接设置变量，如 `--set service.port=80`|
|`--namespace`|`-n`|指定安装的命名空间|
|`--create-namespace`|无|如果指定的命名空间不存在，则自动创建|
|`--version`|无|指定 Chart 的版本|
|`--dry-run`|无|**模拟执行**，打印出生成的清单但不真正安装|
|`--debug`|无|打印详细的调试信息，包括渲染后的 YAML|
|`--wait`|无|等待所有资源（如 Pod）变为 Ready 状态才返回成功|
|`--atomic`|无|如果安装失败，自动回滚（通常配合 `--wait` 使用）|
|`--timeout`|无|设置等待资源就绪的超时时间（默认 5m0s）|

### 常见的 Chart 来源形式：

- **仓库引用**：`bitnami/mysql`（需先 `helm repo add`）
    
- **本地目录**：`./my-chart`
    
- **压缩包**：`./my-chart-0.1.0.tgz`
    
- **完整 URL**：`https://example.com/charts/my-chart-0.1.0.tgz`
### 命令是如何运行的?

当你执行 `helm install` 时，Helm 内部会经历以下几个关键阶段：

1. **本地模板渲染**：Helm 客户端读取本地或远程的 Chart 文件，将 `values.yaml` 中的变量注入到 `templates/` 目录下的 YAML 模板中。
    
2. **依赖检查**：检查 Chart 声明的依赖项是否已下载并满足版本要求。
    
3. **发送到 API Server**：Helm 将生成的完整 Kubernetes 资源清单（Manifests）发送给 Kubernetes API Server。
    
4. **创建 Release 记录**：Helm 在集群中（通常以 Secret 形式）记录这次安装的状态，称为一个 **Release**（发行版本）。
    
5. **资源执行**：Kubernetes 按照清单创建具体的 Pod、Service、ConfigMap 等资源。
## 更新和回滚

在 Helm 的版本管理中，`upgrade` 和 `rollback` 是实现持续交付和故障恢复的双板斧。它们的核心逻辑都围绕着 **修订版本（Revision）** 展开。

### Helm Upgrade：平滑升级

> 命令是如何运行的？

1. **三方合并（Three-way Merge Patch）**：这是 Helm 3 的核心逻辑。Helm 会对比 **上一次的清单**、**集群内的实时状态** 和 **你刚提交的新清单**。
    
    - 即使你手动用 `kubectl edit` 改了某个参数，`helm upgrade` 也能识别并决定是否保留或覆盖。
        
2. **版本递增**：每次成功或失败的 upgrade 都会产生一个新的 `REVISION` 编号（1, 2, 3...）。
    
3. **状态存储**：将新的配置和元数据打包成一个 Secret（默认）存在集群中。

```bash
helm upgrade [RELEASE_NAME] [CHART] [flags]
```

**常用选项与技巧**

- **`--install` (最推荐)**：如果 Release 不存在则安装，存在则升级。这是 CI/CD 流水的标准写法。
    
- **`--reuse-values`**：沿用上一个版本的变量配置，只更新 Chart 或少量指定的 `--set` 变量。
    
- **`--reset-values`**：舍弃之前所有的自定义变量，完全恢复到 Chart 默认的 `values.yaml`。
    
- **`--atomic`**：升级过程如果失败（如 Pod 无法启动），自动执行回滚操作。
    
- **`--wait`**：命令会阻塞，直到所有的 Pod 都 Ready 才会返回成功。
### Helm Rollback：一键回滚

> 命令是如何运行的？

1. **快照恢复**：Helm 并不生成“新”代码，而是从集群存储的历史 Secret 中提取指定修订版的清单。
    
2. **生成新版本**：**注意！** 回滚动作本身会产生一个新的修订版。
    
    - 例如：你当前是 V3，回滚到 V1，那么集群的状态会变成 V1 的样子，但版本号会变为 **V4**。
        
3. **触发 K8s 更新**：将提取的清单推送到 API Server，触发 Kubernetes 原生的滚动更新（Rolling Update）。

```bash
# 回滚到上一个版本
helm rollback [RELEASE_NAME]

# 回滚到指定的修订版本
# 可以使用helm history [release] 查看修订号历史
helm rollback [RELEASE_NAME] [REVISION] [flags]
```

**常用选项与技巧**

- **`--cleanup-on-fail`**：如果在回滚过程中创建了新资源但失败了，自动清理掉这些多余资源。
    
- **查看历史**：在回滚前，务必先运行 `helm history [RELEASE_NAME]` 查看版本列表和对应的描述。
    
- **回滚逻辑限制**：Rollback 只能恢复 Kubernetes 的资源定义，无法恢复外部数据（如数据库里的旧数据）。
## 卸载

在 Helm 的包管理流程中，`uninstall`（在 Helm 2 中称为 `delete`）负责清理 Release 及其相关的 Kubernetes 资源。了解它的运行机制能帮助你更彻底地回收资源，避免留下“僵尸”配置。

### 命令是如何运行的？（原理分析）

当你执行 `helm uninstall` 时，Helm 会执行以下逻辑：

1. **查找 Release 历史**：Helm 首先在集群中（通常是指定 Namespace 下的 Secret）查找该 Release 的最后一次记录。
    
2. **生成删除清单**：根据该 Release 存储的清单（Manifest），识别出当时创建的所有 Kubernetes 资源（如 Deployment, Service, ConfigMap 等）。
    
3. **调用 API 执行删除**：向 Kubernetes API Server 发送删除请求。
    
4. **触发 Hooks**：如果 Chart 中定义了 `pre-delete` 或 `post-delete` 的 Hooks（钩子），Helm 会按顺序执行这些任务（例如删除前备份数据库）。
    
5. **更新/清除记录**：默认情况下，Helm 会从集群中删除该 Release 的所有历史记录。可以使用 `helm list`查看当前部署的所有版本。

```bash
# 标准格式
helm uninstall RELEASE_NAME [flags]

# 别名（兼容习惯）
helm delete RELEASE_NAME [flags]
```

**常用选项：**

| **选项**               | **说明**                                              |
| -------------------- | --------------------------------------------------- |
| `--namespace` / `-n` | 指定 Release 所在的命名空间（必须与安装时一致）                        |
| `--keep-history`     | **关键选项**：卸载资源但保留该 Release 的历史记录（状态变为 `uninstalled`） |
| `--dry-run`          | 模拟卸载：列出将被删除的资源，但并不真正执行删除                            |
| `--no-hooks`         | 删除时不运行 Chart 中定义的任何钩子（Hooks）                        |
| `--timeout`          | 等待删除完成的超时时间（默认 5m0s）                                |
| `--cascade`          | 设置删除级联策略，默认为 `background`（由 K8s 控制控制器和 Pod 的删除顺序）   |
| `--wait`             | 等待所有资源被物理删除后才返回命令成功                                 |
## repo命令

在 Helm 的体系中，`repo`（Repository）命令组就像是配置 Linux 的 `yum` 源或 `apt` 源。它负责管理本地客户端与远程 Chart 仓库之间的连接信息。

### 命令是如何运行的？（原理分析）

当你操作 `helm repo` 相关命令时，Helm 实际上是在维护一个**本地索引映射表**：

1. **配置文件存储**：Helm 将所有添加的仓库地址、凭据存储在本地的 `repositories.yaml` 文件中（通常位于 `~/.config/helm/`）。
    
2. **索引缓存**：当你执行 `update` 时，Helm 会从远程仓库下载一个名为 `index.yaml` 的文件。这个文件包含了该仓库中所有 Chart 的名称、版本、创建时间及下载链接。
    
3. **本地搜索**：当你执行 `helm search repo` 时，Helm 并不联网，而是直接检索这些本地缓存的 `index.yaml` 文件，从而实现极快的查询响应。

> 添加仓库 (Add)

将远程仓库注册到本地。

- **格式**：`helm repo add [NAME] [URL] [flags]`
    
- **示例**：
    
    ```
    helm repo add bitnami https://charts.bitnami.com/bitnami
    ```
    

> 更新仓库 (Update)

同步远程仓库的最新的 Chart 列表和版本信息到本地。

- **格式**：`helm repo update [REPO_NAME...] [flags]`
    
- **使用技巧**：不带参数会更新所有仓库；带参数则只更新特定仓库，速度更快。
    
    Bash
    
    ```
    helm repo update bitnami
    ```
    

> 列出仓库 (List)

查看当前已配置的所有仓库及其 URL。

- **格式**：`helm repo list [flags]`
    

> 移除仓库 (Remove)

从本地配置中删除某个仓库。

- **格式**：`helm repo remove [REPO_NAME...] [flags]`
    

> 生成索引 (Index)

这是**开发 Chart** 时使用的。为包含打包好的 Chart 的目录生成 `index.yaml`。

- **格式**：`helm repo index [DIR] [flags]`

**常用选项**：

| **选项**                                     | **说明**                           | **适用命令**         |
| ------------------------------------------ | -------------------------------- | ---------------- |
| `--username` / `--password`                | 用于访问需要认证的私有仓库                    | `add`            |
| `--force-update`                           | 即使本地已有同名仓库，也强制替换                 | `add`            |
| `--ca-file` / `--insecure-skip-tls-verify` | 处理私有证书或跳过 TLS 验证                 | `add` / `update` |
| `-o` (output)                              | 指定输出格式（table, json, yaml），方便脚本处理 | `list`           |
## 自定义chart

### 方法一：使用脚手架

> `helm create`：从零开始构建

`helm create` 不是创建一个空文件夹，而是生成一个**脚手架（Scaffold）**。它会按照 Helm 官方的最佳实践，自动生成一套符合规范的目录结构和基础模板文件（包括一个示例性的 Nginx 部署）。

```bash
helm create NAME [flags]
```

**常用选项与技巧**

- **技巧 1**：生成的默认模板非常全（包含 Deployment, Service, Ingress, HPA），初学者可以直接修改 `values.yaml` 观察效果，专家则会删掉不需要的部分。
    
- **技巧 2**：`NAME` 不仅是目录名，还会被自动填充到 `Chart.yaml` 的 `name` 字段中。

> `helm lint`：代码的“质检员”

`lint` 命令会扫描你的 Chart 目录，检查其是否符合 Helm 的最佳实践和语法规范。它主要检查：

1. **YAML 语法**：模板渲染后是否是合法的 YAML。
    
2. **文件结构**：是否缺少必选文件（如 `Chart.yaml`）。
    
3. **变量一致性**：`values.yaml` 中的变量是否被模板正确引用。
    
4. **最佳实践**：例如是否设置了资源限制（Resources Quotas）、图标是否有效等。

```bash
helm lint [PATH] [flags]
```

|**选项**|**说明**|
|---|---|
|`--strict`|**严格模式**：任何警告（Warning）都会被视为错误（Error），导致命令失败。|
|`--with-subcharts`|同时检查目录下所有的子 Chart。|
|`--values` / `-f`|指定额外的 values 文件来参与 lint 过程中的模板渲染。|

> `helm package`：打包发布

该命令将 Chart 目录打包成一个版本化的压缩包（`.tgz` 格式）。

1. **版本校验**：检查 `Chart.yaml` 中的 `version` 字段。
    
2. **依赖处理**：如果使用了 `-u` 参数，会先同步并下载依赖。
    
3. **压缩**：排除 `.helmignore` 中定义的文件，将其余内容打包。

```bash
helm package [CHART_PATH] [flags]
```

| **选项**                       | **说明**                                     |
| ---------------------------- | ------------------------------------------ |
| `--dependency-update` / `-u` | 在打包前自动执行 `helm dependency update`。         |
| `--destination` / `-d`       | 指定生成的 `.tgz` 包存放目录（默认为当前目录）。               |
| `--version`                  | 覆盖 `Chart.yaml` 中的版本号，方便在 CI 中动态命名版本。      |
| `--app-version`              | 覆盖 `Chart.yaml` 中的应用版本号（通常对应 Docker 镜像标签）。 |
| `--sign`                     | 使用 GnuPG 密钥对包进行数字签名，增强安全性。                 |

> 使用技巧 

- **技巧 1：排除干扰**：在打包前，确保 `.helmignore` 文件配置正确。类似于 `.gitignore`，它可以防止像 `node_modules` 或本地测试配置被打包进去，减小包体积。
    
- **技巧 2：动态版本控制**：在自动构建流水线中，可以使用 Git 的 Commit ID 作为版本：

```bash
helm package ./my-chart --version "0.1.0-$(git rev-parse --short HEAD)"
```
### 方法二：自定义

一个标准的Helm Chart包含以下核心文件：

|文件/目录|核心作用|
|---|---|
|**`Chart.yaml`**​|Chart的“身份证”，记录名称、版本、描述、依赖等**元数据**。|
|**`values.yaml`**​|所有可配置参数的**默认值**所在地，是定制化部署的“控制中心”。|
|**`templates/`**​|包含Kubernetes资源（如Deployment、Service）的**模板文件**，使用Go模板语法。|
|**`charts/`**​|存放此Chart所**依赖的其他子Chart**。|
|**`crds/`**​|存放**自定义资源定义（Custom Resource Definitions）**​ 的YAML文件。|
|**`templates/NOTES.txt`**​|应用安装成功后，在终端显示的**使用指南和提示信息**。|
|**`values.schema.json`**​|（可选）用于对`values.yaml`文件的结构进行**校验和约束**。|
|**`LICENSE`**​|（可选）此Chart的**许可证文本**。WordPress本身使用GPL许可证。|
|**`README.md`**​|（可选）Chart的**详细说明文档**，包括介绍、安装步骤、配置说明等。|

> Chart.yaml

```yaml
# apiVersion: 定义Chart规范的API版本。对于Helm 3，应使用v2。此字段是必需的。
# 可选值: "v1" (Helm 2), "v2" (Helm 3+)
apiVersion: v2

# name: Chart的名称。此字段是必需的。
# 命名规则：只能包含小写字母、数字和连字符(-)，必须以字母开头和结尾。
name: my-awesome-app

# version: Chart本身的版本，必须遵循语义化版本规范（SemVer 2.0）。此字段是必需的。
# 格式: 主版本.次版本.修订号 (例如：1.2.3, 0.1.0-alpha.1)
version: 1.2.3

# description: 对Chart功能或用途的单句描述。此字段是可选的。
description: A Helm chart for deploying a sample web application on Kubernetes.

# type: 定义Chart的类型。此字段是可选的，默认为 "application"。
# 可选值: "application" (可部署的应用), "library" (提供公用函数或定义的库Chart，不能被安装)
type: application

# appVersion: 此Chart所包含的应用程序的版本。与Chart的version字段无直接关联。此字段是可选的。
# 注意：它不必是SemVer格式，但建议用引号括起来。
appVersion: "v3.4.2"

# kubeVersion: 指定此Chart兼容的Kubernetes版本范围（语义化版本范围）。此字段是可选的。
# 示例: ">= 1.19.0-0", "~1.20.0", ">=1.13.0 <1.15.0"
kubeVersion: ">=1.20.0-0"

# keywords: 与Chart相关的关键字列表，有助于在仓库中被搜索和分类。此字段是可选的。
keywords:
  - web
  - application
  - nginx
  - database

# home: 项目主页的URL地址。此字段是可选的。
home: https://github.com/myorg/my-awesome-app

# sources: 项目源代码URL地址的列表。此字段是可选的。
sources:
  - https://github.com/myorg/my-awesome-app/src

# icon: 一个指向SVG或PNG格式图标的URL，该图标将代表此Chart。此字段是可选的。
icon: https://my-org.github.io/my-awesome-app/icon.png

# dependencies: 定义此Chart所依赖的其他子Chart列表。此字段是可选的。
dependencies:
  - name: redis
    # version: 依赖Chart的版本约束。此字段是必需的。
    version: "~6.2.0"
    # repository: 依赖Chart所在的仓库URL，或使用通过 `helm repo add` 添加的仓库别名（格式为 "@repo-name"）。此字段是必需的。
    repository: "https://charts.bitnami.com/bitnami"
    # condition: 用于控制是否启用此依赖的条件的YAML路径（例如：redis.enabled）。此字段是可选的。
    # 如果该路径在父Chart的values中解析为false，则不会安装此依赖。
    condition: redis.enabled
    # tags: 与此依赖关联的标签列表。可以通过在父Chart的values中设置顶级tags键来批量启用/禁用一组依赖。此字段是可选的。
    tags:
      - cache
      - database
    # alias: 为依赖的Chart设置一个别名。这允许你将同一个Chart以不同的名称和配置多次添加到依赖中。此字段是可选的。
    # alias: custom-redis-name
    # import-values: 用于将子Chart中的值导入到父Chart的指定路径。此字段是可选的。
    # 支持两种格式：1. 直接指定子Chart的exports字段下的键名；2. 使用child-parent格式指定源路径和目标路径。
    # import-values:
    #   - data

# maintainers: Chart维护者的信息列表。此字段是可选的。
maintainers:
  - name: Jane Doe
    # email: 维护者的电子邮件地址。此字段是可选的。
    email: jane.doe@example.com
    # url: 维护者的个人主页URL。此字段是可选的。
    url: https://example.com/jane-doe
  - name: John Smith
    email: john.smith@example.com

# deprecated: 标记此Chart是否已被弃用（不推荐使用）。此字段是可选的，值为布尔值。
# 可选值: true, false (默认)
deprecated: false

# annotations: 可以添加任意的元数据键值对，供其他工具使用。此字段是可选的。
annotations:
  category: Web Application
  license: Apache-2.0
  supported-arch: "amd64"

# engine: 指定用于渲染templates/目录中模板的模板引擎。此字段是可选的，默认值为 "gotpl"。
# 默认值: "gotpl" (Go template engine)
# engine: gotpl

# tillerVersion: 此字段在Helm 2中用于指定所需的Tiller版本，在Helm 3中已不再使用。
# tillerVersion: ">2.0.0"
```

自 v3.3.2 开始，不允许添加额外的字段。建议的做法是添加自定义元数据在 `annotations`。