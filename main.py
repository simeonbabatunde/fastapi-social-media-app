from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# In memory posts
my_posts = [{"title": "Title of post 1", "content": "Post 1 content", "id": 1}, {"title": "Best foods", "content": "I enjoy pizza", "id": 2}]

# Util functions
def find_post_by_id(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_post_index(id):
    for idx, post in enumerate(my_posts):
        if post['id'] == id:
            return idx



@app.get("/")
async def root():
    return {"message": "Hello World!!!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(1, 10000000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return {"detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found')
    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)