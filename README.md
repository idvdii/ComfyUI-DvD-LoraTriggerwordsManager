# ComfyUI-DvD-LoraTriggerwordsManager

A set of professional ComfyUI custom nodes designed to manage LoRA trigger words efficiently. 
Seamlessly read, edit, and save trigger words in **WebUI (Automatic1111) compatible JSON format**.

一款专业的 ComfyUI 自定义节点，用于高效管理 LoRA 触发词。
支持读取、编辑并保存 **WebUI (Automatic1111) 兼容的 JSON 格式** 触发词文件。

## ✨ Features (功能特性)

*   **Auto-Read Triggers**: Automatically reads `.json` or `.txt` metadata associated with your LoRA.
    *   自动读取与 LoRA 关联的元数据文件。
*   **WebUI Compatibility**: Saves edited trigger words in the standard format (`"activation text"`) used by Stable Diffusion WebUI.
    *   完美兼容 WebUI，保存格式为标准的 `"activation text"`。
*   **Chainable Workflow**: All nodes have a `pre_text` input, allowing you to chain multiple LoRA loaders together. The trigger words will be automatically concatenated with commas.
    *   支持“糖葫芦”式串联，触发词自动合并。
*   **Info Log**: Provides a clean, formatted log output for debugging or checking details.
    *   提供清晰的日志输出端口。
*   **Zero Dependencies**: Pure Python implementation, no complex JavaScript or extra pip installs required.
    *   零依赖，纯 Python 实现，无需安装额外库。

## 📦 Nodes (节点介绍)

### 1. DvD LoRA Loader (Trigger Words)
Standard LoRA loader with `MODEL` and `CLIP` connections.
*   **Inputs**: Model, Clip, LoRA Name, Strength.
*   **Mode**: `Read` (Default) or `Save`.
*   **Edit Text**: Input new trigger words here when in `Save` mode.
*   **Pre_text (Optional)**: Connect string from previous node to append.

### 2. DvD LoRA Loader (Model Only)
Optimized for FLUX/SD3 or workflows where you only need to modify the model weights without affecting CLIP directly (or handling CLIP separately).

### 3. DvD LoRA Stack (Multi-Merge)
Load 3 LoRAs at once.
*   **Merge Logic**: Automatically combines trigger words from all 3 LoRAs + `pre_text`.
*   **Save Target**: Select which LoRA (1, 2, or 3) to update when saving.

## 🚀 Installation (安装方法)

1.  Navigate to your ComfyUI custom nodes directory:
    ```bash
    cd ComfyUI/custom_nodes/
    ```
2.  Clone this repository:
    ```bash
    git clone https://github.com/YourUsername/ComfyUI-DvD-LoraTriggerwordsManager.git
    ```
3.  Restart ComfyUI.

## 🛠 Usage (使用说明)

1.  **Read Mode**: Just select a LoRA. The `trigger_text` output will output the trigger words found in the file.
2.  **Save Mode**: 
    *   Change `mode` to **Save**.
    *   Type your new tags in `edit_text`.
    *   Queue a prompt (run once).
    *   The `.json` file in your LoRA directory will be updated.
    *   Switch back to **Read** mode for normal use.

---
**License**: MIT