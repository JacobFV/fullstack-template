from app.api.deps import (
    get_current_active_superuser,
    get_current_user,
    get_current_user_or_none,
    get_current_verifiable_identity,
    get_db,
)
from app.schema import (
    User,
    VerifiableIdentity,
    VerificationRequestSessionBase,
    VerificationRequestSessionCreate,
    VerificationRequestSessionUpdate,
    VerificationRequestSessionPublic,
    VerificationRequestSession,
    VerificationRequestStatus,
)
from fastapi import APIRouter, Depends, HTTPException, WebSocket, Request
from sqlalchemy.orm import Session
from sqlmodel import select
import aio_pika
import os

router = APIRouter()


@router.get("/", response_model=list[VerificationRequestSessionPublic])
def get_my_verification_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(VerificationRequestSession)
        .filter(VerificationRequestSession.user_id == current_user.id)
        .all()
    )


@router.post("/", response_model=VerificationRequestSessionPublic)
def create_verification_request(
    verification_request_in: VerificationRequestSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verification_request = VerificationRequestSession(**verification_request_in.dict())
    db.add(verification_request)
    db.commit()
    return verification_request


@router.put(
    "/{verification_request_id}", response_model=VerificationRequestSessionPublic
)
def update_verification_request(
    verification_request_id: int,
    verification_request_in: VerificationRequestSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verification_request = (
        db.query(VerificationRequestSession)
        .filter(VerificationRequestSession.id == verification_request_id)
        .first()
    )
    if not verification_request:
        raise HTTPException(status_code=404, detail="Verification request not found")
    verification_request.update(verification_request_in.dict(exclude_unset=True))
    db.commit()
    return verification_request


@router.get("/{verification_request_id}", response_model=VerificationRequestStatus)
def check_verification_request_status(
    verification_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verification_request = (
        db.query(VerificationRequestSession)
        .filter(VerificationRequestSession.id == verification_request_id)
        .first()
    )
    if not verification_request:
        raise HTTPException(status_code=404, detail="Verification request not found")
    return verification_request


@router.websocket("/ws/{verification_request_id}")
async def verify_me_websocket_endpoint(
    websocket: WebSocket,
    verification_request_id: int,
    db: Session = Depends(get_db),
    current_identity: VerifiableIdentity = Depends(get_current_verifiable_identity),
):
    await websocket.accept()

    verification_request = (
        db.query(VerificationRequestSession)
        .filter(VerificationRequestSession.id == verification_request_id)
        .first()
    )
    if not verification_request:
        raise HTTPException(status_code=404, detail="Verification request not found")

    async def consumer(message: aio_pika.IncomingMessage):
        async with message.process():
            # Echo message back to WebSocket
            await websocket.send_text(f"Message received: {message.body.decode()}")

    # Start consuming messages
    await verification_request.amqp_queue().consume(consumer)

    try:
        while True:
            text_data = await websocket.receive_text()
            # Publish messages to the queue
            await verification_request.amqp_queue().default_exchange.publish(
                aio_pika.Message(body=text_data.encode()),
                routing_key=verification_request.queue_name,
            )

    except Exception as e:
        await websocket.close()
        print(f"WebSocket connection closed with exception: {e}")
    finally:
        pass

#incomplete route
# @router.post("/video/{verification_request_id}")
# async def stream_video(request: Request, verification_request_id: int):
#     async for chunk in request.stream():
#         # Process each chunk of video data
#         process_video_chunk(chunk)
