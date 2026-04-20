import config
from core.logger import log_action, log_error

class PermissionGate:
    def check(self, tool_name, params=None):
        level = config.ACCESS_LEVELS.get(tool_name, "never")
        if level == "auto":
            return True
        elif level == "ask":
            print(f"\n--- PERMISSION REQUEST ---")
            print(f"Tool: {tool_name}")
            print(f"Params: {params}")
            resp = input("Allow? (y/n): ").strip().lower()
            if resp == 'y':
                return True
            else:
                log_error("PermissionGate", f"Denied tool {tool_name}")
                raise PermissionError(f"User denied permission to use {tool_name}")
        elif level == "admin":
            if config.ADMIN_MODE_ENABLED:
                return True
            else:
                log_error("PermissionGate", f"Denied admin tool {tool_name}")
                raise PermissionError(f"Admin mode not enabled for {tool_name}")
        elif level == "never":
            log_error("PermissionGate", f"Never allow tool {tool_name}")
            raise PermissionError(f"Tool {tool_name} is permanently restricted")
        
        raise PermissionError(f"Unknown permission level for {tool_name}")
