## Enable GPU by going to Runtime menu -> Change runtime type -> select T4 GPU under Hardware accelerator
!curl -fsSL https://ollama.com/install.sh | sh
!pip install litellm
!pip install aiohttp pyngrok
# !pip install pandasai
# !pip install python-dotenv
!pip install 'litellm[proxy]'
# !pip install openai
import os
import asyncio
# from dotenv import load_dotenv
# import openai
# import ollama
import litellm
from litellm import completion
# load_dotenv()
# api_key = os.getenv("OPEN_API_KEY")
# openai.api_base = 'http://localhost:8000/v1'

# Set LD_LIBRARY_PATH so the system NVIDIA library 
# os.environ.update({'LD_LIBRARY_PATH': '/usr/lib64-nvidia'})

async def run_process(cmd):
  print('>>> starting', *cmd)
  p = await asyncio.subprocess.create_subprocess_exec(
      *cmd,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE,
  )

  async def pipe(lines):
    async for line in lines:
      print(line.strip().decode('utf-8'))

  await asyncio.gather(
      pipe(p.stdout),
      pipe(p.stderr),
  )

## register an account at ngrok.com and create an authtoken and place it here
# await asyncio.gather(
#     run_process(['ngrok', 'config', 'add-authtoken','your-auth-token'])
# )

await asyncio.gather(
    run_process(['ollama', 'pull', 'phi']),
    run_process(['ollama', 'serve']),
    run_process(['litellm', '--model', 'ollama/phi']),
    # run_process(['ngrok', 'http', '--log', 'stderr', '11434']),
)
  
# await asyncio.gather(
#     # run_process(['ollama', 'pull', 'phi']),
#     run_process(['ollama', 'serve']),
#     run_process(['litellm', '--model', 'ollama/phi']),
#     # run_process(['ngrok', 'http', '--log', 'stderr', '11434']),
# )

response = completion(
            model="ollama/phi", 
            messages = [{ "content": "Hello, how are you?","role": "user"}], 
            api_base="http://localhost:11434"
)

print(response)

# # import openai # openai v1.0.0+
# client = litellm.Ollama(api_key="anything",base_url="http://0.0.0.0:11434") # set proxy to base_url
# # request sent to model set on litellm proxy, `litellm --model`
# response = client.chat.completions.create(model="ollama/phi", messages = [
#     {
#         "role": "user",
#         "content": "this is a test request, write a short poem"
#     }
# ])

# print(response)
