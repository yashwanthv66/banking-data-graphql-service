from fastapi import FastAPI, Depends
# Replace starlette.graphql import with graphene_fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from graphene import Schema
from sqlalchemy.orm import Session
import csv
import os

from app.database import engine, get_db, Base
from app.schema.schema import schema
from app.models.bank import Bank, Branch

app = FastAPI(title="Bank API Service")

# Create tables
Base.metadata.create_all(bind=engine)

# Add GraphQL endpoint using FastAPI's route handlers
@app.post("/gql")
@app.get("/gql")
async def graphql_endpoint(request: Request, db: Session = Depends(get_db)):
    # Get the request data
    if request.method == "POST":
        data = await request.json()
        query = data.get("query")
        variables = data.get("variables", {})
    else:
        query = request.query_params.get("query")
        variables = {}
    
    # Execute the query with context containing the session
    context = {"session": db}
    result = schema.execute(query, variable_values=variables, context=context)
    
    # Return the result
    return {"data": result.data, "errors": [str(err) for err in result.errors] if result.errors else None}

# Add a simple GraphiQL interface with updated React version
@app.get("/graphiql", response_class=HTMLResponse)
async def graphiql():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GraphiQL</title>
        <link href="https://unpkg.com/graphiql@2.0.9/graphiql.min.css" rel="stylesheet" />
    </head>
    <body style="margin: 0;">
        <div id="graphiql" style="height: 100vh;"></div>
        <script src="https://unpkg.com/react@17.0.2/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@17.0.2/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/graphiql@2.0.9/graphiql.min.js"></script>
        <script>
            const fetcher = graphQLParams => {
                return fetch('/gql', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(graphQLParams),
                    credentials: 'same-origin',
                })
                .then(response => response.json())
                .catch(error => {
                    return { errors: [error.message] };
                });
            };

            ReactDOM.render(
                React.createElement(GraphiQL, { fetcher }),
                document.getElementById('graphiql')
            );
        </script>
    </body>
    </html>
    """

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    
    # Check if data already exists
    if db.query(Bank).count() == 0:
        # Load data from CSV
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "..", "data", "bank_branches.csv")
        
        # Create a dictionary to store banks
        banks = {}
        
        # Read CSV file using the csv module instead of pandas
        with open(csv_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                # Check if bank already exists
                bank_name = row.get('bank_name')
                if bank_name not in banks:
                    bank = Bank(name=bank_name)
                    db.add(bank)
                    db.flush()  # Flush to get the ID
                    banks[bank_name] = bank.id
                
                # Create branch
                branch = Branch(
                    ifsc=row.get('ifsc'),
                    branch=row.get('branch'),
                    address=row.get('address'),
                    city=row.get('city'),
                    district=row.get('district'),
                    state=row.get('state'),
                    bank_id=banks[bank_name]
                )
                db.add(branch)
        
        db.commit()

@app.get("/")
def read_root():
    return {"message": "Welcome to Bank API Service. Access GraphQL at /gql or GraphiQL interface at /graphiql"}