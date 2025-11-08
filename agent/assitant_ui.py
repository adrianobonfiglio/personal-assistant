import subprocess

def open_assisent_page(page_name: str, params: str = None):
    command = f"open assistant://{page_name}"
    if params:
        command += f"/param={params}"
    print(f"--- Opening assistant page with command: {command} ---")
    subprocess.call(command, shell=True)