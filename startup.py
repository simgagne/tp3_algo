import main
import localsearch 
import asyncio

async def well():
    await asyncio.gather(*(localsearch.start() for i in range (3)))
    
asyncio.run(well())

