# 这里的 .main 指的是同级目录下的 main.py 文件
from .main import DvD_LoraLoader_Standard, DvD_LoraLoader_ModelOnly, DvD_LoraLoader_Stack

# 内部类名映射 (ComfyUI 识别用)
NODE_CLASS_MAPPINGS = {
    "DvD_LoraLoader_Standard": DvD_LoraLoader_Standard,
    "DvD_LoraLoader_ModelOnly": DvD_LoraLoader_ModelOnly,
    "DvD_LoraLoader_Stack": DvD_LoraLoader_Stack
}

# 界面显示名称映射 (用户在菜单里看到的)
NODE_DISPLAY_NAME_MAPPINGS = {
    "DvD_LoraLoader_Standard": "DvD LoRA Loader (Trigger Words)",
    "DvD_LoraLoader_ModelOnly": "DvD LoRA Loader (Model Only)",
    "DvD_LoraLoader_Stack": "DvD LoRA Stack (Multi-Merge)"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]