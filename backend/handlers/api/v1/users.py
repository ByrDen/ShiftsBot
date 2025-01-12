from fastapi import APIRouter, Path, HTTPException, Query
from fastapi.responses import RedirectResponse
from starlette import status


from app.schemas.user import UserDetail, UserCreateForm, UserEditForm
from app.services.user_service import UserService
from src.database import DBSession

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(path="", name="create_user", response_model=UserDetail, status_code=201)
async def create_user(
        session: DBSession,
        form: UserCreateForm
):
    res = await UserService(session=session).save(form=form)
    return res


@router.get(path="", name="get_all_users", response_model=list[UserDetail])
async def get_list_user(
        session: DBSession,
):
    objs = await UserService(session=session).list()
    return objs


@router.get(path="/{pk}", name="get_user", response_model=UserDetail)
async def get_user(
        session: DBSession,
        pk: int = Path(gt=0, examples=[42])
):
    obj = await UserService(session=session).get(pk=pk)
    return obj


@router.put(path="/{pk}", name="update_user", response_model=UserDetail)
async def update_user(
        session: DBSession,
        form: UserEditForm,
        pk: int = Path(gt=0)
):
    obj = await UserService(session=session).update(pk=pk, form=form)
    return obj


@router.delete(path="/{pk}", name="delete_one_user")
async def delete_user(
        session: DBSession,
        pk: int = Path(gt=0)
):
    await UserService(session=session).delete(pk=pk)
    return "OK"


@router.get(path="/bambam/", response_class=RedirectResponse)
async def get_user_by_tg_id(
        session: DBSession,
        tg_id: int = Query(default=2)
):
    if not tg_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Need tg_id!")
    pk = await UserService(session=session).get_pk_by_tg_id(tg_id=tg_id)
    return RedirectResponse(f"/api/v1/users/{pk}")
