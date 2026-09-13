from fastapi import FastAPI,HTTPException,Path
from pydantic import BaseModel,Field
from typing import Annotated,Optional
import json

Niaj=FastAPI()

class Expense(BaseModel):
    id  : Annotated[str,Field(...,description="Id of the expenses",example="E001")]
    name: Annotated[str,Field(...,description="Name of the expense",example="Lunch")]
    amount: Annotated[int,Field(...,description="Amount of the expense",example="500")]
    category: Annotated[str,Field(...,description="Category of the expense",example="Food")]
    date: Annotated[str,Field(...,description="Date of the expense",example="2026-08-01")]
    description: Annotated[str,Field(...,description="Description of the expense",example="Lunch at restaurent")]

class Expenseupdate(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    amount: Annotated[Optional[int],Field(default=None)]
    category: Annotated[Optional[str],Field(default=None)]
    date: Annotated[Optional[str],Field(default=None)]
    description: Annotated[Optional[str],Field(default=None)]

def load_data():
    with open('expenses.json',"r")as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("expenses.json","w")as f:
        json.dump(data,f)

@Niaj.get("/")
def goat():
    return "GOAT"

@Niaj.get("/about")
def about():
    return "Lionel Messi"

@Niaj.get("/view")
def view_expenses():
    data=load_data()
    return data

@Niaj.get("/view/{expenses_id}")
def view_expenses_specific(expenses_id:str= Path(...,description="Id of the expenses",example="E001")):
    data=load_data()
    if expenses_id in data:
        return data[expenses_id]
    else:
        raise HTTPException(status_code=404,detail="Expense not found.")

@Niaj.get("/sort")
def view_sorted_expenses(sorted_by:str,order:str):
    data=load_data()

    sorted_data=list(data.values())
    if order=="asc":
        sorted_data.sort(key=lambda x: x[sorted_by])
    else:
        sorted_data.sort(key=lambda x: x[sorted_by],reverse=True)
    return sorted_data

@Niaj.post("/create")
def create_expense(expense:Expense):
    data=load_data()
    if expense.id in data:
        raise HTTPException(status_code=400,detail="Expense id already exist")
    data[expense.id]=expense.model_dump(exclude=["id"])
    save_data(data)

@Niaj.put("/edit/{expense_id}")
def update_expense(expense:Expenseupdate, expense_id:str):
    data=load_data()
    if expense_id not in data:
        raise HTTPException(status_code=400,detail="Expense not found")
    data[expense_id].update(expense.model_dump(exclude_unset=True))
    save_data(data)

@Niaj.delete("/delete/{expense_id}")
def delete_expense(expense_id:str):
    data=load_data()
    if expense_id not in data:
        raise HTTPException(status_code=400,detail="Expense not found")
    del data[expense_id]
    save_data(data)