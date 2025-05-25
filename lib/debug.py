#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie, Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Fetch some data for live testing
    devs = session.query(Dev).all()
    companies = session.query(Company).all()
    freebies = session.query(Freebie).all()

    import ipdb; ipdb.set_trace()  # 👈 Move this here

    print(f"\nDevs: {devs}")
    print(f"Companies: {companies}")
    print(f"Freebies: {freebies}")

