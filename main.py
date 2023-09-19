from fastapi import FastAPI
from fastapi.responses import FileResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import os

app = FastAPI()


chrome_options = Options()
chrome_options.add_argument("--headless")  
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1080)  

@app.get("/screenshot/")
async def get_screenshot(url: str):
    try:
        driver.get(url)

        screenshot_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        screenshot_file_path = screenshot_file.name
        driver.save_screenshot(screenshot_file_path)

        driver.quit()

        return FileResponse(screenshot_file_path, headers={"Content-Type": "image/png"})
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)