from typing import Annotated
from app.api.deps import (
    get_current_active_superuser,
    get_current_user,
    get_current_user_or_none,
    get_current_verifiable_identity,
    get_db,
)
from app.ml.face_detection import FaceRecognitionHandler
from app.schema.proof_of_id_verification import (
    User,
    UserThatRequestsVerification,
    VerifiableIdentity,
    VerificationBase,
    VerificationRequestCreate,
    VerificationRequestUpdate,
    VerificationPublic,
    Verification,
    VerificationStatus,
)
from fastapi import APIRouter, Depends, HTTPException, WebSocket, Request
from sqlalchemy.orm import Session
from sqlmodel import select
import aio_pika
import os

# I think we need this import and need to add the frames function in the video route
from app.ml.face_detection import process_frame

router = APIRouter()


@router.get("/", response_model=list[VerificationPublic])
def get_my_verification_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Verification).filter(Verification.user_id == current_user.id).all()


def get_verification_request_assigned_to_meby_id(
    verification_request_id: Verification.ID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Verification | None:
    try:
        verf_request = db.exec(
            select(Verification)
            .filter(
                Verification.id == verification_request_id,
                Verification.who_to_verify_id == current_user.id,
            )
            .first()
        )
        return verf_request
    except Exception as e:
        raise HTTPException(status_code=404, detail="Verification request not found")


GetVerificationRequestDep = Annotated[
    Verification, Depends(get_verification_request_assigned_to_meby_id)
]


@router.post("/", response_model=VerificationPublic)
def create_verification_request(
    verification_request_in: VerificationRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not isinstance(current_user, UserThatRequestsVerification):
        raise HTTPException(
            status_code=403,
            detail="User must face for an other user that requests verification",
        )
    verification_request = Verification(**verification_request_in.dict())
    db.add(verification_request)
    db.commit()
    return verification_request


@router.put("/{verification_request_id}", response_model=VerificationPublic)
def update_verification_request(
    verification_request_in: VerificationRequestUpdate,
    current_verification_request: GetVerificationRequestDep = Depends(
        GetVerificationRequestDep
    ),
    db: Session = Depends(get_db),
):
    if not current_verification_request:
        raise HTTPException(status_code=404, detail="Verification request not found")
    current_verification_request.update(
        verification_request_in.dict(exclude_unset=True)
    )
    db.commit()
    return current_verification_request


@router.get("/{verification_request_id}", response_model=VerificationStatus)
def check_verification_request_status(
    verification_request_id: Verification.ID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verification_request = (
        db.query(Verification)
        .filter(Verification.id == verification_request_id)
        .first()
    )
    if not verification_request:
        raise HTTPException(status_code=404, detail="Verification request not found")
    return verification_request


@router.websocket("/ws/{verification_request_id}")
async def verify_me_websocket_endpoint(
    websocket: WebSocket,
    verification_request_id: Verification.ID,
    db: Session = Depends(get_db),
    current_identity: VerifiableIdentity = Depends(get_current_verifiable_identity),
):
    await websocket.accept()

    verification_request = (
        db.query(Verification)
        .filter(Verification.id == verification_request_id)
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


@router.post("/video/{verification_request_id}")
async def stream_video(
    request: Request, verification_request: GetVerificationRequestDep
):
    face_recognition_handler = FaceRecognitionHandler(
        verification_request=verification_request
    )
    async for chunk in request.stream():
        # Process each chunk of video data
        face_recognition_handler.process_frame(chunk)
