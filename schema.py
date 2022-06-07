# quickstart.schema.py

import graphene

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from graphql_jwt.decorators import login_required
from accounts.models import CustomUser
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()
   verify_account = mutations.VerifyAccount.Field()
   token_auth = mutations.ObtainJSONWebToken.Field()
   revoke_token = mutations.RevokeToken.Field()
   
class DisableUser(graphene.Mutation):
       
            
       class Arguments:
              
              user_id = graphene.Int()

       user_type = graphene.Field(UserType)

       @staticmethod
       def mutate(root, info, user_id):
             print("im mutation")
             user_obj = CustomUser.objects.get(id=user_id)
             print(user_obj.status.verified)
             user_obj.isactive = False
             user_obj.save()
             return DisableUser(user_type=user_obj)



class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
      disableuser = DisableUser.Field() 
      

schema = graphene.Schema(query=Query, mutation=Mutation)