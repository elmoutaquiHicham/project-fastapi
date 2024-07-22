from fastapi import FastAPI, Response, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel  ## Library to define schema 
from typing import Optional
from random import randrange

class Post(BaseModel) : 
    title : str
    content : str 
    published : bool = True ## if the user doesnt give a value it will be true by default 
    rating : Optional[int] = None 



my_posts = []
app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "becoming the best"}


@app.get("/posts")

def get_posts():
    return {"data": my_posts}


@app.post("/posts")

def create_post(new_post : Post):
    post_dic = new_post.dict()
    post_dic["id"] = randrange(0,1000000)
    my_posts.append(post_dic)
    return {"data": post_dic}

def find_post(id) : 
    for p in my_posts : 
        if p["id"] == id : 
            return p 


@app.get("/posts/{id}")
def get_post(id : int, response : Response):
    post = find_post(id)
    if not post : 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    else : 
        return {"postt" : post}

    
def find_idex_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 
        
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    # deleting a post 
    # find the index in the array that has the required id
    index = find_idex_post(id)
    if not index : 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    del(my_posts[index])
    return Response(status_code= status.HTTP_204_NO_CONTENT)
