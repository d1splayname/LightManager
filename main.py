from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import HTTPException
from kasa import SmartPlug

import os
import uvicorn


load_dotenv()
app = FastAPI()

_IP = os.getenv("IP")

@app.get("/lights")
async def Lights():
    try:
        plug = SmartPlug(_IP)
        await plug.update()
        status = plug.is_on
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"is_on": status}

@app.get("/lights/toggle")
async def ToggleLights():
    try:
        plug = SmartPlug(_IP)
        await plug.update()
        if plug.is_on:
            await plug.turn_off()
        else:
            await plug.turn_on()

        await plug.update()
        status = plug.is_on
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"is_on": status}

@app.get("/lights/on")  
async def TurnOnLights():
    try:
        plug = SmartPlug(_IP)
        await plug.update()
        await plug.turn_on()
        await plug.update()
        status = plug.is_on
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"is_on": status}

@app.get("/lights/off")
async def TurnOffLights():
    try:
        plug = SmartPlug(_IP)
        await plug.update()
        await plug.turn_off()
        await plug.update()
        status = plug.is_on
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"is_on": status}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3003)