import sys, bpy
sys.path.insert(0, r'E:\TCA_F\TCA_WorldPrototype\tools\blender')
import blender_mcp
blender_mcp.register()
bpy.context.scene.blendermcp_auto_start_server = True
bpy.context.scene.blendermcp_port = 9877
blender_mcp._blendermcp_ensure_server_running()
print('TCA Blender MCP bridge registered on localhost:9877', flush=True)
