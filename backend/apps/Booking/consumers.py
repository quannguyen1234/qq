from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from apps.User.models import Doctor
from .models import ConnectDoctor
from .views import receive_order
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from apps.User.references import REVERSE_USER_TYPE

class AuthenToken:

    async def websocket_connect(self, event):
        await self.accept()
        user=self.scope['user']
        if isinstance(user,AnonymousUser):
            await self.send(json.dumps({
                'data':{
                    "message": "Token is not correct or expired",
                    'status': 401,
                    'flag': False
                }     
            }))
           
            await self.close()
            return False
        return True            
         
         
class Conversation(AuthenToken,AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_user=None
        self.user=None
        self.user_type=None

    async def websocket_connect(self, event):
        check=await super().websocket_connect(event)
        
        if not check:        
            return
        
        self.base_user=self.scope['user']
        self.user_type=await database_sync_to_async(lambda:self.base_user.user_type)()
        

        if ( await database_sync_to_async(lambda:hasattr(self.base_user,'user_doctor'))()
           and await database_sync_to_async(lambda:hasattr(self.base_user,'user_patient'))() ):
            await self.send(json.dumps({
                'data':{
                    "message": "Forbiden",
                    'status': 404,
                    'flag': False
                }     
            }))
            await self.close()
            return 
            
        elif self.user_type == REVERSE_USER_TYPE['Doctor']:
            self.user= await database_sync_to_async(lambda:self.base_user.user_doctor)()
            await database_sync_to_async(lambda:ConnectDoctor.objects.create(
                doctor=self.user,
                doctor_channel=self.channel_name
            ))()

            await self.send(json.dumps(
                {
                    'data':{
                        'message':'Access successfully!',
                        'status':200,
                        'flag':True
                    }     
                }  
            ))

    
    async def websocket_disconnect(self,*agrs,**kwagrs):
        # if isinstance(self.user,AnonymousUser): 
        if  self.user_type is not  None:
            if self.user_type==REVERSE_USER_TYPE['Doctor']:
                
                await database_sync_to_async(lambda:ConnectDoctor.objects.filter(doctor=self.user).delete())()
                await self.disconnect(code=None)
                
                # turn off receving order signal 
                self.user.is_receive=True
                await database_sync_to_async(lambda:self.user.save())()
            

    async def receive(self, text_data=None, bytes_data=None):
        data=json.loads(text_data)
        if data['type']=='doctor-set-address':
          
            await database_sync_to_async(lambda:receive_order(self.base_user,data))()  
            await self.send(json.dumps({
                "data": {
                    "message:":"turn on receiving order doctor signal ",
                    "flag":True,
                    "status":200
                },
            }))
            self.user.is_receive=True
            await database_sync_to_async(lambda:self.user.save())()

        elif data['type']=='patient-choose-doctor':
            # self.send_message_to_channel()
    
            doctor_id=data['doctor']
            connect=await database_sync_to_async(lambda:ConnectDoctor.objects.get(doctor__doctor_id=doctor_id))()
            print(connect.doctor)
            # doctor_target_channel=database_sync_to_async(lambda:connect.doctor_channel)()
            # self.send_message_to_channel(doctor_target_channel,{
                # 'patient':self.user.id
            # })

        elif data['type']=='doctor-confirm-order':
            pass    

    def send_message_to_channel(self,channel_name, data):
 
        channel_layer = self.get_channel_layer()
        async_to_sync(channel_layer.send)(channel_name, {
            'type': 'doctor-confirdm-order',
            **data,
        })

        
        
    async def chat(self,event):
        
        data = event["data"]
        await self.send(text_data=json.dumps(data))

# class Conversation(AuthenToken,AsyncWebsocketConsumer):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.user=None
    

#     async def websocket_connect(self, event):
#         check=await super().websocket_connect(event)
        
#         if not check:        
#             return
        
#         self.user=self.scope['user']
            
#         if( await database_sync_to_async(lambda:hasattr(self.user,'user_doctor'))() 
#             and await database_sync_to_async(lambda:hasattr(self.user,'user_patient'))() ):
           
#             await self.send(json.dumps({
#                 'data':{
#                     "message": "Forbiden",
#                     'status': 404,
#                     'flag': False
#                 }     
#             }))
#             await self.close()
#             return 
    
#     async def receive(self, text_data=None, bytes_data=None):
#         data=json.loads(text_data)
#         if data['type']=='make-contact':
#             doctor=data.get('doctor')
            


