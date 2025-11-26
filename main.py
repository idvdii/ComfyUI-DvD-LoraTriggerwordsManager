"""
ComfyUI-DvD-LoraTriggerwordsManager
Author: DvD
Description: A powerful LoRA loader with automatic trigger word management, 
WebUI-compatible JSON editing, and stackable text concatenation.
"""

import os
import json
import folder_paths
import comfy.utils
import comfy.sd

# ============================
# Core Helper: JSON Handler (WebUI Compatible)
# ============================
class DvD_JsonHandler:
    @staticmethod
    def get_json_path(lora_path):
        base_path = os.path.splitext(lora_path)[0]
        json_path = base_path + ".json"
        txt_path = base_path + ".txt"
        return json_path, txt_path

    @staticmethod
    def read_trigger_text(lora_name):
        lora_path = folder_paths.get_full_path("loras", lora_name)
        if not lora_path: return ""
        json_path, txt_path = DvD_JsonHandler.get_json_path(lora_path)
        
        target_file = json_path if os.path.exists(json_path) else (txt_path if os.path.exists(txt_path) else None)
        
        if not target_file: return ""
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content.startswith("{"):
                    try:
                        data = json.loads(content)
                        # Compatibility Check: WebUI (Space) -> Plugins (Underscore) -> Civitai
                        if "activation text" in data: return str(data["activation text"])
                        if "activation_text" in data: return str(data["activation_text"])
                        if "trigger_words" in data: 
                            return ", ".join(data["trigger_words"]) if isinstance(data["trigger_words"], list) else str(data["trigger_words"])
                        if "trigger words" in data:
                            return ", ".join(data["trigger words"]) if isinstance(data["trigger words"], list) else str(data["trigger words"])
                        return content 
                    except: return content 
                return content 
        except: return ""

    @staticmethod
    def save_trigger_text(lora_name, text):
        lora_path = folder_paths.get_full_path("loras", lora_name)
        if not lora_path: return False
        json_path, _ = DvD_JsonHandler.get_json_path(lora_path)
        
        # Standard WebUI Template
        final_data = {
            "description": "",
            "sd version": "",
            "activation text": text.strip(),
            "preferred weight": 1.0,
            "notes": ""
        }

        # Try to update existing file without destroying other fields
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                if isinstance(existing_data, dict):
                    if "activation text" in existing_data:
                        existing_data["activation text"] = text.strip()
                    elif "activation_text" in existing_data:
                        existing_data["activation_text"] = text.strip()
                    else:
                        existing_data["activation text"] = text.strip()
                    final_data = existing_data
            except:
                pass

        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=4, ensure_ascii=False)
            return True
        except: 
            return False

# ============================
# Node 1: Standard Loader
# ============================
class DvD_LoraLoader_Standard:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_name": (folder_paths.get_filename_list("loras"), ),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "mode": (["Read (只读)", "Save (保存修改)"], ), 
                "edit_text": ("STRING", {"multiline": True, "default": "", "placeholder": "Modify trigger words here (Save mode only)..."}),
            },
            "optional": {
                "pre_text": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "trigger_text", "info_log")
    FUNCTION = "process"
    CATEGORY = "DvD Nodes"

    def process(self, model, clip, lora_name, strength_model, strength_clip, mode, edit_text, pre_text=""):
        final_text = ""
        msg = ""
        
        if mode == "Save (保存修改)" and edit_text.strip():
            if DvD_JsonHandler.save_trigger_text(lora_name, edit_text):
                final_text = edit_text.strip()
                msg = f"Update Saved (WebUI Compatible)"
            else:
                final_text = "Error Saving"
                msg = f"Save Failed"
        else:
            final_text = DvD_JsonHandler.read_trigger_text(lora_name)
            msg = "Read from file"

        combined_parts = []
        if pre_text and pre_text.strip(): combined_parts.append(pre_text.strip())
        if final_text and final_text.strip(): combined_parts.append(final_text.strip())
        combined_output = ", ".join(combined_parts)

        log_parts = [f"=== DvD Standard Loader ===", f"File: {lora_name}", f"Status: {msg}"]
        if pre_text: log_parts.append(f"🔗 [Pre_text Added]: Yes")
        log_parts.append("--- Triggers ---")
        log_parts.append(final_text if final_text else "(None)")
        log_parts.append("=======================")

        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)

        return (model_lora, clip_lora, combined_output, "\n".join(log_parts))

# ============================
# Node 2: Model Only Loader
# ============================
class DvD_LoraLoader_ModelOnly:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "lora_name": (folder_paths.get_filename_list("loras"), ),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "mode": (["Read (只读)", "Save (保存修改)"], ), 
                "edit_text": ("STRING", {"multiline": True, "default": "", "placeholder": "Modify trigger words here (Save mode only)..."}),
            },
            "optional": {
                "pre_text": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "STRING", "STRING")
    RETURN_NAMES = ("MODEL", "trigger_text", "info_log")
    FUNCTION = "process"
    CATEGORY = "DvD Nodes"

    def process(self, model, lora_name, strength_model, mode, edit_text, pre_text=""):
        final_text = ""
        msg = ""
        if mode == "Save (保存修改)" and edit_text.strip():
            if DvD_JsonHandler.save_trigger_text(lora_name, edit_text):
                final_text = edit_text.strip()
                msg = "Update Saved (WebUI Compatible)"
            else:
                msg = "Save Failed"
        else:
            final_text = DvD_JsonHandler.read_trigger_text(lora_name)
            msg = "Read from file"

        combined_parts = []
        if pre_text and pre_text.strip(): combined_parts.append(pre_text.strip())
        if final_text and final_text.strip(): combined_parts.append(final_text.strip())
        combined_output = ", ".join(combined_parts)

        log_parts = [f"=== DvD Model Only Loader ===", f"File: {lora_name}"]
        if pre_text: log_parts.append(f"🔗 [Pre_text Added]")
        log_parts.append("--- Triggers ---")
        log_parts.append(final_text)
        log_parts.append("========================")

        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
        model_lora, _ = comfy.sd.load_lora_for_models(model, None, lora, strength_model, 0)

        return (model_lora, combined_output, "\n".join(log_parts))

# ============================
# Node 3: LoRA Stack
# ============================
class DvD_LoraLoader_Stack:
    @classmethod
    def INPUT_TYPES(s):
        lora_list = ["None"] + folder_paths.get_filename_list("loras")
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_1": (lora_list, ),
                "strength_1": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_2": (lora_list, ),
                "strength_2": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_3": (lora_list, ),
                "strength_3": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "mode": (["Read (只读)", "Save (保存修改)"], ),
                "save_target": (["None (不保存)", "Lora 1", "Lora 2", "Lora 3"], ),
                "edit_text": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter new trigger words here..."}),
            },
            "optional": {
                "pre_text": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "trigger_text", "info_log")
    FUNCTION = "process_stack"
    CATEGORY = "DvD Nodes"

    def process_stack(self, model, clip, lora_1, strength_1, lora_2, strength_2, lora_3, strength_3, 
                      mode, save_target, edit_text, pre_text=""):
        
        save_msg = ""
        if mode == "Save (保存修改)" and save_target != "None (不保存)" and edit_text.strip():
            target_map = {"Lora 1": lora_1, "Lora 2": lora_2, "Lora 3": lora_3}
            t_name = target_map.get(save_target)
            if t_name and t_name != "None":
                if DvD_JsonHandler.save_trigger_text(t_name, edit_text):
                    save_msg = f"✅ Saved to {save_target} (WebUI Format)"
                else:
                    save_msg = f"❌ Failed to save"

        current_model = model
        current_clip = clip
        text_list = []
        log_lines = ["╔══════════ DvD LoRA Stack ══════════╗"]
        if save_msg: log_lines.append(f"║ {save_msg}")

        if pre_text and pre_text.strip():
            text_list.append(pre_text.strip())
            log_lines.append("║ 🔗 [Pre_text Added]")
            log_lines.append("╟────────────────────────────────────╢")

        def process_one(m, c, name, strength, label):
            if name == "None":
                log_lines.append(f"║ [{label}] None")
                log_lines.append("╟────────────────────────────────────╢")
                return m, c, ""
            
            t_text = DvD_JsonHandler.read_trigger_text(name)
            log_lines.append(f"║ [{label}] {name}")
            log_lines.append(f"║ ► {t_text if t_text else '(No triggers)'}")
            log_lines.append("╟────────────────────────────────────╢")

            path = folder_paths.get_full_path("loras", name)
            if path:
                loaded_lora = comfy.utils.load_torch_file(path, safe_load=True)
                m_out, c_out = comfy.sd.load_lora_for_models(m, c, loaded_lora, strength, strength)
                return m_out, c_out, t_text
            return m, c, ""

        current_model, current_clip, txt1 = process_one(current_model, current_clip, lora_1, strength_1, "1")
        if txt1: text_list.append(txt1)
        current_model, current_clip, txt2 = process_one(current_model, current_clip, lora_2, strength_2, "2")
        if txt2: text_list.append(txt2)
        current_model, current_clip, txt3 = process_one(current_model, current_clip, lora_3, strength_3, "3")
        if txt3: text_list.append(txt3)

        if log_lines[-1].startswith("╟"): log_lines.pop()
        log_lines.append("╚════════════════════════════════════╝")

        return (current_model, current_clip, ", ".join(filter(None, text_list)), "\n".join(log_lines))