import os
from fastapi import APIRouter,Form,File,UploadFile,HTTPException,status
from starlette.responses import FileResponse
from backend import api
from fastapi.responses import JSONResponse
app=APIRouter()

@app.post('/Login')
def login(email: str=Form(...),password : str=Form(...)):
    try:
        res=api.login(email,password)
    except Exception as e:
        raise HTTPException(status_code=422,detail=str(e))

    return JSONResponse(content={"response": res}, status_code=status.HTTP_200_OK)


@app.post('/Register')
def register(email: str=Form(...),password : str=Form(...)):
    try:
        res=api.signup(email,password)
    except Exception as e:
        raise HTTPException(status_code=422,detail=str(e))

    return JSONResponse(content={"response": res}, status_code=status.HTTP_200_OK)


@app.post('/Get_Fund_Houses')
def get_fund_houses():
    try:
        res=api.unique_fund_family_details()
        
    except Exception as e:
        raise HTTPException(status_code=422,detail=str(e))

    return JSONResponse(content={"response": res}, status_code=status.HTTP_200_OK)

@app.post('/Get_schemes')
def get_schemes(fund_house:str=Form(...)):

    try:
        res=api.get_different_schemes(fund_house)
        
    except Exception as e:
        raise HTTPException(status_code=422,detail=str(e))

    return JSONResponse(content={"response": res}, status_code=status.HTTP_200_OK)


@app.post('/Invest')
def invest(email : str=Form(...),scheme_code : str=Form(...),scheme_name : str=Form(...),price :int=Form(...),quantity : int=Form(...)):
    try:
        res=api.invest(email,scheme_code,scheme_name,price,quantity)
    except Exception as e:
        raise HTTPException(status_code=422,detail=str(e))
    
    return JSONResponse(content={"response": res}, status_code=status.HTTP_200_OK)


@app.post('/My_profile')
def my_profile(email :str=Form(...)):
    try:
        res1,res2=api.my_profle(email)

    except Exception as e:
        raise HTTPException(status_code=422,detail=str(e))
    
    return JSONResponse(content={"response1": res1,"response2":res2}, status_code=status.HTTP_200_OK)
