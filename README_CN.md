# ComfyUI-DvD-LoraTriggerwordsManager

[English Readme](README.md)

一款专业的 ComfyUI 自定义节点，用于高效管理 LoRA 触发词。
支持读取、编辑并保存 **WebUI (Automatic1111) 兼容的 JSON 格式** 触发词文件。

## ✨ 功能特性

*   📖 **自动读取 (Auto-Read)**: 自动识别并加载 LoRA 同级目录下的与 LoRA 同名 .json, .txt文件中的触发词。
*   🌐 **智能联网 (Smart Lookup)**: **(New!)** 当本地没有触发词文件时，自动计算模型哈希值 (AutoV3/V2) 并从 Civitai 获取触发词，自动生成配置文件。
*   ✍️ **双向读写 (Read & Edit)**: 不仅能读取，还能直接在节点内修改触发词并保存。
*   🔄 **WebUI 格式对齐 (WebUI Alignment)**: 写入文件时严格遵循 A1111 WebUI 的标准 JSON 格式（如 "activation text", "sd version"），确保跨软件兼容性，不破坏原有数据。
*   🔗 **智能合并 (Auto-Merge)**: 支持单体串联或堆栈式加载，所有 LoRA 的触发词会自动以逗号分隔进行合并输出，无需额外的文本拼接节点。
*   🐍 **纯后端实现 (Pure Python)**: 零前端依赖，运行稳定，无需复杂的安装步骤。

![Example Workflow](assets/example_workflow.png)

## 📦 节点介绍

### 1. DvD LoRA Loader (触发词版)
带有 `MODEL` 和 `CLIP` 连接的标准 LoRA 加载器。
*   **Inputs**: 模型、CLIP、LoRA 名称、强度。
*   **Mode (模式)**: `Read` (读取/默认) 或 `Save` (保存)。
*   **Edit Text**: 仅在 `Save` 模式下生效，在此输入要保存的触发词。
*   **Pre_text (可选)**: 连接上一个节点的字符串输出，实现自动拼接。

### 2. DvD LoRA Loader (仅模型版)
专为 FLUX/SD3 或其他不需要处理 CLIP（或单独处理 CLIP）的工作流优化，仅修改模型权重。

### 3. DvD LoRA Stack (多重堆栈)
一次性加载 3 个 LoRA。
*   **Merge Logic**: 自动合并所有 3 个 LoRA 以及 `pre_text` 的触发词。
*   **Save Target**: 指定在保存模式下要修改哪一个 LoRA (1, 2, 或 3) 的文件。

## 🚀 安装方法

1.  进入你的 ComfyUI custom_nodes 目录:
    ```bash
    cd ComfyUI/custom_nodes/
    ```

2.  克隆本仓库:
    ```bash
    git clone https://github.com/idvdii/ComfyUI-DvD-LoraTriggerwordsManager.git
    ```

3.  重启 ComfyUI。

## 🛠 使用说明

### 1. 读取模式 (Read Mode)
选择 LoRA 后，节点会自动读取关联的触发词。
![Read Mode](assets/demo_01_read.png)

### 2. 保存/修改模式 (Save Mode)
*   将 `mode` 切换为 **Save**。
*   在 `edit_text` 中输入新的触发词。
*   运行一次提示词（Queue Prompt）。
*   **结果:** JSON 文件会被即时创建或更新。
![Save Mode](assets/demo_02_save.png)

### 3. 堆栈与合并 (Stack Mode)
多重 LoRA 堆栈，自动合并触发词。可以通过 `save_target` 指定要修改哪一个 LoRA 的文件。
![Stack Mode](assets/demo_03_stack.png)

### 4. 兼容性 (Compatibility)
生成的 JSON 文件采用 WebUI 标准格式，确保跨软件兼容。

| WebUI 格式 vs 插件格式 | 智能更新 (保留原数据) |
| :---: | :---: |
| ![Format](assets/demo_04_format.png) | ![Update](assets/demo_05_update.png) |

### 5. 自动抓取演示 (Automatic Discovery)
**场景**：你下载了一个只有 `.safetensors` 的 LoRA，没有元数据文件，不知道触发词是啥。

**1. 初始状态无JSON:**
![Initial Folder](assets/auto_01_folder.png)

**2. 自动计算哈希并联网查询:**
直接运行节点，它会自动通过哈希值从 Civitai 找到正确的触发词 (例如 "MMD, 3D")。
![Console Log](assets/auto_03_log.png)

**3. 生成结果:**
触发词自动填入提示词并生成图像。
![Result](assets/auto_04_image.png)

**4. 自动保存文件:**
标准的 `.json` 文件会自动生成并保存在目录下，下次使用无需再联网。
![JSON Created](assets/auto_05_json_file.png)

---

**License**: MIT
