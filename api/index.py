from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

def calculate_meeting_cost(participants: int, hourly_rate: int, meeting_length: int) -> float:
    return (participants * hourly_rate * meeting_length) / 60

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Arbeitsbesprechungen - Kostenrechner</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f0f0f0;
            }
            .calculator {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            input, button {
                width: 100%;
                padding: 8px;
                margin: 8px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            button {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            #result {
                margin-top: 20px;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                color: #4CAF50;
            }
        </style>
    </head>
    <body>
        <div class="calculator">
            <h1>Arbeitsbesprechungen - Kostenrechner</h1>
            <form id="calculatorForm">
                <label for="participants">Anzahl der Teilnehmer:</label>
                <input type="number" id="participants" min="1" value="1" required>
                
                <label for="hourlyRate">Stundensatz pro Person (€):</label>
                <input type="number" id="hourlyRate" min="0" value="50" required>
                
                <label for="meetingLength">Besprechungsdauer (Minuten):</label>
                <input type="number" id="meetingLength" min="1" value="60" required>
                
                <button type="submit">Kosten berechnen</button>
            </form>
            <div id="result"></div>
        </div>

        <script>
            document.getElementById('calculatorForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const participants = document.getElementById('participants').value;
                const hourlyRate = document.getElementById('hourlyRate').value;
                const meetingLength = document.getElementById('meetingLength').value;
                
                const response = await fetch(`/calculate?participants=${participants}&hourly_rate=${hourlyRate}&meeting_length=${meetingLength}`);
                const data = await response.json();
                
                document.getElementById('result').innerHTML = `<h2>Besprechungskosten: €${data.cost.toFixed(2)}</h2>`;
            });
        </script>
    </body>
    </html>
    """

@app.get("/calculate")
async def calculate(participants: int, hourly_rate: int, meeting_length: int):
    cost = calculate_meeting_cost(participants, hourly_rate, meeting_length)
    return {"cost": cost}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 