from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from lib.models import Dev, Company, Freebie, Base 

# Setup
engine = create_engine('sqlite:///freebies.db')

# Create tables in the database (important!)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Clear old data
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()

# Add new data
dev1 = Dev(name="Edwin")
dev2 = Dev(name="Bieko")

company1 = Company(name="Google", founding_year=1998)
company2 = Company(name="Moringa", founding_year=2015)

freebie1 = Freebie(item_name="T-shirt", value=20, dev=dev1, company=company1)
freebie2 = Freebie(item_name="Sticker", value=5, dev=dev2, company=company2)

session.add_all([dev1, dev2, company1, company2, freebie1, freebie2])
session.commit()

print("✅ Database seeded successfully!")
