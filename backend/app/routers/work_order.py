from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, require_role, get_current_user
from app.models import OrderPriority, OrderStatus, UserRole
from app.schemas.work_order import ModelRatioRead, OrderStatusUpdate, OrderRead, DiscrepancyRead, OrderCreate
from app.models import Equipment, Work_Order, Technician
from app.models.user import User

router = APIRouter(prefix = "/orders", tags = ["orders"])

#Get all work orders
@router.get("", response_model=list[OrderRead])
async def list_work_orders(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    statement = select(Work_Order)
    result = await db.execute(statement)
    return list(result.scalars().all())



# Get colocation discrepancies endpoint
@router.get("/discrepancies", response_model=list[DiscrepancyRead])
async def get_colocation_discrepancies(
    db: AsyncSession = Depends(get_db),
    priority: OrderPriority | None = None,
    _: User = Depends(get_current_user),
):
    statement = (
        select (
            Work_Order.id.label("work_order_id"),
            Work_Order.title,
            Equipment.hospital_id.label("equipment_hospital_id"),
            Technician.hospital_id.label("technician_hospital_id"),
        )
        .join(Equipment, Work_Order.equipment_id == Equipment.id)
        .join(Technician, Work_Order.technician_id == Technician.id)
        .where(Equipment.hospital_id != Technician.hospital_id)
    )

    #Filter based on priority
    if priority is not None:
        statement = statement.where(Work_Order.priority == priority)

    statement = statement.order_by(Work_Order.id)

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]

# Finds completion/failure ratio by device model
@router.get("/ratios", response_model=list[ModelRatioRead])
async def get_model_ratios(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    completed = func.count(
        case((Work_Order.status == OrderStatus.COMPLETED, Work_Order.id))
    )
    failed = func.count(
        case((Work_Order.status == OrderStatus.FAILED, Work_Order.id))
    )
    pending = func.count(
        case(
            (
                Work_Order.status.notin_(
                    [OrderStatus.COMPLETED, OrderStatus.FAILED]
                ),
                Work_Order.id,
            )
        )
    )

    statement = (
        select(
            Equipment.model.label("model"),
            func.count(Work_Order.id).label("total"),
            completed.label("completed"),
            failed.label("failed"),
            pending.label("pending"),
        )
        .join(Equipment, Work_Order.equipment_id == Equipment.id)
        .group_by(Equipment.model)
        .order_by(Equipment.model)
    )

    result = await db.execute(statement)
    rows = result.all()

    payload = []
    for row in rows:
        resolved = row.completed + row.failed
        payload.append(
            {
                "model": row.model,
                "total": row.total,
                "completed": row.completed,
                "failed": row.failed,
                "pending": row.pending,
                "completion_ratio": row.completed / resolved if resolved else None,
                "failure_ratio": row.failed / resolved if resolved else None,
            }
        )
    return payload

#Get specific work order by id
@router.get("/{work_order_id}", response_model=OrderRead)
async def get_work_order(
    work_order_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    order = await db.get(Work_Order, work_order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID {work_order_id} not found",
        )
    return order

# Update order status endpoint
@router.patch("/{work_order_id}/status", response_model=OrderRead,)
async def update_order_status(
    work_order_id : int,
    payload : OrderStatusUpdate,
    db : AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN, UserRole.FIELD_TECHNICIAN)),
):
    order = await db.get(Work_Order, work_order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID {work_order_id} not found",
        )

    if payload.status == OrderStatus.COMPLETED:
        order.mark_completed()
    elif payload.status == OrderStatus.FAILED:
        order.mark_failed()
    else:
        order.status = payload.status

    await db.commit()
    await db.refresh(order)
    return order

#General update endpoint for work orders
@router.put("/{work_order_id}", response_model=OrderRead)
async def update_work_order(
    work_order_id: int,
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    order = await db.get(Work_Order, work_order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID {work_order_id} not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)

    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


#Create
@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_work_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    order = Work_Order(**payload.model_dump())
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


#Delete
@router.delete("/{work_order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_order(
    work_order_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    order = await db.get(Work_Order, work_order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID {work_order_id} not found",
        )
 
    await db.delete(order)
    await db.commit()
    return None
