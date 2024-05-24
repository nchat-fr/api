from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def logged_as():
    ...


@router.post('/login')
def login():
    ...


@router.post('/register')
def register():
    ...


@router.delete('/')
def logout():
    ...