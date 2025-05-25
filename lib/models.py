from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship('Freebie', back_populates='company')
    devs = relationship('Dev', secondary='freebies', back_populates='companies', overlaps='freebies')


    def __repr__(self):
        return f"<Company(name={self.name}, founding_year={self.founding_year})>"

    def give_freebie(self, dev, item_name, value):
        """Creates a new Freebie and associates it with this company and the provided dev."""
        return Freebie(item_name=item_name, value=value, dev=dev, company=self)

    def total_giveaways(self):
        return len(self.freebies)

    def freebies_by_value(self, min_value):
        """Return freebies with value >= min_value"""
        return [f for f in self.freebies if f.value >= min_value]

    @classmethod
    def oldest_company(cls, session: Session):
        """Return the oldest company by founding_year"""
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs', overlaps='freebies')


    def __repr__(self):
        return f"<Dev(name={self.name})>"

    def total_freebies(self):
        return len(self.freebies)

    def most_valuable_freebie(self):
        if not self.freebies:
            return None
        return max(self.freebies, key=lambda f: f.value)

    def total_value(self):
        return sum(f.value for f in self.freebies)

    def received_one(self, item_name):
        """Returns True if this dev has received a freebie with the given item_name"""
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        """Transfers a freebie to another dev, if this dev owns it"""
        if freebie in self.freebies:
            freebie.dev = other_dev


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)
    company_id = Column(Integer, ForeignKey('companies.id'))
    dev_id = Column(Integer, ForeignKey('devs.id'))

    company = relationship('Company', back_populates='freebies', overlaps='devs,companies')
    dev = relationship('Dev', back_populates='freebies', overlaps='devs,companies')


    def __repr__(self):
        return f"<Freebie(item_name={self.item_name}, value={self.value})>"

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
