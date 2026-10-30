import asyncio, sys, json, os
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    env = dict(os.environ)
    env['DISABLE_TELEMETRY']='true'
    env['BLENDER_PORT']='9877'
    server = StdioServerParameters(command='uvx', args=['--from', 'mcp-for-blender', 'mcp-for-blender'], env=env)
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if sys.argv[1]=='list':
                result=await session.list_tools()
                print(json.dumps([t.model_dump() for t in result.tools],ensure_ascii=False))
            else:
                name=sys.argv[1]
                if name=='runfile':
                    name='execute_blender_code'
                    source=str(Path(sys.argv[2]).resolve())
                    args={'code': "import bpy, pathlib, traceback\ndef run_tca_script():\n    try:\n        p=pathlib.Path("+repr(source)+")\n        exec(compile(p.read_text(encoding='utf8'),str(p),'exec'),{})\n    except Exception:\n        pathlib.Path("+repr(str(Path(source).with_suffix('.error.txt')))+").write_text(traceback.format_exc(),encoding='utf8')\n    return None\nbpy.app.timers.register(run_tca_script,first_interval=1.0)\nprint('Blender script scheduled: '+"+repr(Path(source).name)+")", 'user_prompt':'你启动blender和对应mcp，帮我做一个好看的hd2d用的场景吧先，一定要好看，你可以任意去网上找资源或是自己建模，角色先不做，只做场景，一定要好看'}
                else:
                    args=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8-sig'))
                result=await session.call_tool(name,args,read_timeout_seconds=600)
                print(result.model_dump_json())

asyncio.run(main())
