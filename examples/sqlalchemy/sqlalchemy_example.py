import json
from pathlib import Path
from typing import Optional

from sqlalchemy import Float, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# Define the base class for declarative models
class Base(DeclarativeBase):
    pass


# Define the Bearing model
class Bearing(Base):
    __tablename__ = "bearings"

    id: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str] = mapped_column(String(50))  # e.g., "6205", "NU308"
    bearing_type: Mapped[str] = mapped_column(String(30))  # e.g., "Deep Groove Ball"
    bore_diameter: Mapped[float] = mapped_column(Float)  # Inner diameter in mm
    outer_diameter: Mapped[float] = mapped_column(Float)  # Outer diameter in mm
    width: Mapped[float] = mapped_column(Float)  # Width in mm
    load_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Load rating in kN

    def __repr__(self) -> str:
        return (
            f"Bearing(id={self.id}, designation='{self.designation}', type='{self.bearing_type}')"
        )


def main():
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///bearings.db", echo=False)

    # Create all tables
    Base.metadata.create_all(engine)

    # Load bearing data from JSON file
    data_file = Path(__file__).parent / "bearings_data.json"
    with open(data_file) as f:
        bearings_data = json.load(f)

    # CREATE - Insert new bearing records
    print("\n=== CREATE Operation ===")
    with Session(engine) as session:
        bearings = [Bearing(**bearing_data) for bearing_data in bearings_data]
        session.add_all(bearings)
        session.commit()
        print(f"Added {len(bearings)} bearings from JSON file")
        for bearing in bearings:
            print(f"  {bearing}")

    # READ - Query bearing records
    print("\n=== READ Operation ===")
    with Session(engine) as session:
        # Read all bearings
        stmt = select(Bearing)
        bearings = session.scalars(stmt).all()
        print("\nAll bearings:")
        for bearing in bearings:
            print(f"  {bearing}")

        # Read specific bearing by designation
        stmt = select(Bearing).where(Bearing.designation == "NU308")
        bearing = session.scalar(stmt)
        print(f"\nBearing with designation 'NU308': {bearing}")

        # Read bearings with bore diameter >= 25mm
        stmt = select(Bearing).where(Bearing.bore_diameter >= 25.0)
        large_bore_bearings = session.scalars(stmt).all()
        print("\nBearings with bore diameter >= 25mm:")
        for bearing in large_bore_bearings:
            print(f"  {bearing.designation}: {bearing.bore_diameter}mm")

    # UPDATE - Modify bearing records
    print("\n=== UPDATE Operation ===")
    with Session(engine) as session:
        # Find the bearing to update
        stmt = select(Bearing).where(Bearing.designation == "6205")
        bearing = session.scalar(stmt)

        if bearing:
            print(f"Before update: {bearing}, load_rating={bearing.load_rating} kN")
            # Update the load rating
            bearing.load_rating = 15.3
            session.commit()
            print(f"After update: {bearing}, load_rating={bearing.load_rating} kN")

    # DELETE - Remove bearing records
    print("\n=== DELETE Operation ===")
    with Session(engine) as session:
        # Find and delete a specific bearing
        stmt = select(Bearing).where(Bearing.designation == "51105")
        bearing = session.scalar(stmt)

        if bearing:
            print(f"Deleting: {bearing}")
            session.delete(bearing)
            session.commit()

        # Verify deletion
        stmt = select(Bearing)
        remaining_bearings = session.scalars(stmt).all()
        print("\nRemaining bearings after deletion:")
        for bearing in remaining_bearings:
            print(f"  {bearing}")


if __name__ == "__main__":
    main()
