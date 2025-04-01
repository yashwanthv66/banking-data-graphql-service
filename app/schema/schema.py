import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from app.models.bank import Bank as BankModel, Branch as BranchModel

class Bank(SQLAlchemyObjectType):
    class Meta:
        model = BankModel
        interfaces = (relay.Node, )

class Branch(SQLAlchemyObjectType):
    class Meta:
        model = BranchModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    
    # Field for branches
    branches = SQLAlchemyConnectionField(Branch.connection)
    
    # Field for banks
    banks = SQLAlchemyConnectionField(Bank.connection)
    
    # Field for a specific branch by ifsc
    branch_by_ifsc = graphene.Field(Branch, ifsc=graphene.String(required=True))
    
    def resolve_branch_by_ifsc(self, info, ifsc):
        query = Branch.get_query(info)
        return query.filter(BranchModel.ifsc == ifsc).first()

schema = graphene.Schema(query=Query)