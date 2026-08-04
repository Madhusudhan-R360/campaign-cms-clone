from fastapi import FastAPI


app = FastAPI(
    title="Campaign CMS Clone"
)


@app.get("/health")
async def health():

    return {
        "success": True,
        "message": "Campaign CMS Running"
    }