import PyInstaller.__main__
import os

# We want the output to go into desktop-app/resources/backend
output_dir = os.path.abspath(os.path.join('desktop-app', 'resources'))
os.makedirs(output_dir, exist_ok=True)

PyInstaller.__main__.run([
    'bg_remover/api.py',
    '-y',                # Overwrite output directory without asking
    '--name=backend',
    '--onedir',          # Use onedir instead of onefile for better compatibility with large AI libs
    '--noconsole',       # Hide console window
    '--hidden-import=uvicorn.logging',
    '--hidden-import=uvicorn.loops',
    '--hidden-import=uvicorn.loops.auto',
    '--hidden-import=uvicorn.protocols',
    '--hidden-import=uvicorn.protocols.http',
    '--hidden-import=uvicorn.protocols.http.auto',
    '--hidden-import=uvicorn.protocols.websockets',
    '--hidden-import=uvicorn.protocols.websockets.auto',
    '--hidden-import=uvicorn.lifespan',
    '--hidden-import=uvicorn.lifespan.on',
    '--hidden-import=uvicorn.lifespan.off',
    '--hidden-import=rembg',
    '--hidden-import=onnxruntime',
    '--hidden-import=scipy.spatial.transform._rotation_groups',
    '--distpath=' + output_dir,
    '--workpath=build_temp',
    '--specpath=build_temp'
])
print(f"Build complete! Executable is in {output_dir}/backend/backend.exe")
