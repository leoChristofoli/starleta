import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse, UJSONResponse
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.responses import HTMLResponse
import uvicorn
import ujson

# Configuration from environment variables or '.env' file.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')

# Database table definitions.
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Integer),
    sqlalchemy.Column("valid", sqlalchemy.Integer),
)

# Main application code.
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
app = Starlette(debug=False)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8003/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.route("/chat")
class Homepage(HTTPEndpoint):
    async def get(self, request):
        return HTMLResponse(html)

@app.websocket_route("/ws")
class Echo(WebSocketEndpoint):

    encoding = "text"

    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Message text was: {data}")

@app.on_event("startup")
async def startup():
    
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.route("/hello/{name}", methods=["GET"])
async def hello(request) -> str:
    body = await request.body()
    form = await request.form()
    print(body, form)
    name = request.path_params['name']
    return UJSONResponse({"hello": name})

@app.route("/notes", methods=["GET"])
async def list_notes(request):
    query = notes.select()
    results = await database.fetch_all(query)
    content = [
        {
            "id": result["id"],
            "text": result["text"],
            "completed": result["completed"],
            "valid": result["valid"]
        }
        for result in results
    ]
    return UJSONResponse(content)

@app.route("/notes", methods=["POST"])
async def add_note(request):
    data = await request.json()
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print(data)
    query = notes.insert().values(
       text=data["text"],
       completed=data["completed"],
       valid=data["valid"]
    )
    await database.execute(query)
    return JSONResponse({
        "text": data["text"],
        "completed": data["completed"]
    })

if __name__ == "__main__":
    uvicorn.run(app,  http='h11', loop='asyncio', host='0.0.0.0', port=8003)