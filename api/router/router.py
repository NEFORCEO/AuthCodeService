from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from api.broker import broker
from db.models import User, PendingUser
from db.session import SessionDep
from function.generate_code import generate_code
from schemas.schema import ParamSchema, GetSchema


router = APIRouter(prefix="/auth", tags=["Верификация"])



@router.post("/send_code")
async def send_code_bot(param: ParamSchema, db: SessionDep):
    while True:
        code = await generate_code(db)
        existing_user = await db.execute(select(User).where(User.code == code))
        if not existing_user.scalar_one_or_none():  
            break
        
    new_user = User(username=param.username, code=code)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    await broker.publish(
        param.model_dump(),
        queue="code"
    )
    return {"status_code": 200, "message": "Сообщение было отправлено"}


@router.post('/verify_code')
async def verify_code(param: GetSchema,db: SessionDep):
    get_user = await db.execute(select(User).where(User.username == param.username))
    result = get_user.scalar_one_or_none()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверные данные")
    if param.code == result.code:
        await broker.publish(
            {"username": param.username, "message": "Вы успешно прошли регистрацию, поздравляем"},
            queue="success"
        )
        
        peding_user = await db.execute(select(PendingUser).where(PendingUser.username == param.username))
        res = peding_user.scalar_one_or_none()
        if res:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой пользователь уже существует")
        
        new_user = PendingUser(username=param.username)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        await db.delete(result)
        await db.commit()

        return {"status_code": 200, "message": "Успешная регистрация"}
    return {"status_code": 400, "message": "Неверный код"}

    
    