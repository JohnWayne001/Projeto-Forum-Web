from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


posts = [
    {
        "id": 1,
        "titulo": "Meu primeiro post",
        "resumo": "Resumo inicial do blog.",
        "conteudo": "Este é o conteúdo completo do meu primeiro post usando FastAPI!",
        "autor": "Carlos"
    }
]
id_counter = 2



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "posts": posts})

@app.get("/post/{id}", response_class=HTMLResponse)
async def view_post(request: Request, id: int):
    post = None
    
    for p in posts:
        if p["id"] == id:
            post = p
            break

    return templates.TemplateResponse(request=request, name="post.html", context={"request": request, "post": post})

@app.get("/create", response_class=HTMLResponse)
async def create_form(request: Request):
    return templates.TemplateResponse(request=request, name="create.html", context={"request": request})

@app.post("/create")
async def create_post(request: Request):
    global id_counter
    form_data = await request.form()
    
    novo_post = {
        "id": id_counter,
        "titulo": form_data["titulo"],
        "resumo": form_data["resumo"],
        "conteudo": form_data["conteudo"],
        "autor": form_data["autor"]
    }
    posts.append(novo_post)
    id_counter += 1
    return RedirectResponse(url="/", status_code=303)

@app.get("/edit/{id}", response_class=HTMLResponse)
async def edit_form(request: Request, id: int):
    post = None
    
    for p in posts:
        if p["id"] == id:
            post = p
            break
        
    return templates.TemplateResponse(request=request, name="edit.html", context={"request": request, "post": post})

@app.post("/edit/{id}")
async def edit_post(request: Request, id: int):
    form_data = await request.form()
    for post in posts:
        if post["id"] == id:
            post["titulo"] = form_data["titulo"]
            post["resumo"] = form_data["resumo"]
            post["conteudo"] = form_data["conteudo"]
            post["autor"] = form_data["autor"]
            break
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{id}")
async def delete_post(id: int):
    global posts
    posts = [p for p in posts if p["id"] != id]
    return RedirectResponse(url="/", status_code=303)