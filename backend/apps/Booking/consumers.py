from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from apps.User.models import Doctor,Patient
from .models import ConnectDoctor
from .views import receive_order
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from apps.User.references import REVERSE_USER_TYPE
from channels.layers import get_channel_layer
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
        has_permission=False
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
            await database_sync_to_async(lambda:ConnectDoctor.objects.filter(doctor=self.user).delete())()
            await database_sync_to_async(lambda:ConnectDoctor.objects.create(
                doctor=self.user,
                doctor_channel=self.channel_name
            ))()
            has_permission=True

        elif self.user_type == REVERSE_USER_TYPE['Patient']:
            self.user= await database_sync_to_async(lambda:self.base_user.user_patient)()
            has_permission=True
        
        if has_permission:
            
            await self.send(json.dumps(
                {
                    'data':{
                        'message':'Access successfully!',
                        'channel':self.channel_name,
                        'status':200,
                        'flag':True
                    }     
                }  
            ))
        else:
            self.close()

    
    async def websocket_disconnect(self,*agrs,**kwagrs):
        # if isinstance(self.user,AnonymousUser): 
        if  self.user_type is not  None:
            if self.user_type==REVERSE_USER_TYPE['Doctor']:
                
                await database_sync_to_async(lambda:ConnectDoctor.objects.filter(doctor=self.user).delete())()
                await self.disconnect(code=None)
                
                # turn off receving order signal 
                self.user.is_receive=True
                await database_sync_to_async(lambda:self.user.save())()

            if self.user_type==REVERSE_USER_TYPE['Patient']:
                
                await database_sync_to_async(lambda:ConnectDoctor.objects.filter(patient=self.user).delete())()
                await self.disconnect(code=None)
                

            

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
            
            doctor_id=data['doctor']
            connect=await database_sync_to_async(lambda:ConnectDoctor.objects.get(doctor__doctor_id=doctor_id))()
            
            doctor_target_channel=await database_sync_to_async(lambda:connect.doctor_channel)()

            # send to doctor interface a message about confirmings
            await self.send_message_to_channel(doctor_target_channel,{
                'type':'doctor-confirm-order',
                'message':'Confirming Order!',
                'patient_id':await database_sync_to_async(lambda:self.user.patient_id)(),
                'patient_name':await database_sync_to_async(lambda:self.user.base_user.get_full_name)(),
                "patient_channel":self.channel_name
            })
            
        elif data['type']=='doctor-confirm-order':
            is_receive_odrder=data.get('is_receive_odrder')
            patient_channel=data.get('patient_channel')
            
            if is_receive_odrder:
                connect=await database_sync_to_async(lambda:ConnectDoctor.objects.get(doctor=self.user))()
                patient=await database_sync_to_async(Patient.objects.get)(patient_id=data.get('patient_id'))
                connect.patient=patient
                connect.patient_channel=data.get('patient_channel')
                connect.is_confirm=True
                await database_sync_to_async(lambda:connect.save())()
                
                # send the message to client interface
                await self.send_message_to_channel(patient_channel,
                    {
                        'type':'doctor-confirm-order',
                        'flag':True,
                        'status':200,
                        'message':'The doctor has received order',
                        'doctor_id':await database_sync_to_async(lambda:self.user.doctor_id)(),
                        'doctor_name':await database_sync_to_async(lambda:self.user.base_user.get_full_name)()
                    }               
                )    
            else:
                await self.send_message_to_channel(patient_channel,
                    {
                        'type':'doctor-confirm-order',
                        'flag':False,
                        'status':200,
                        'message':'The doctor has not received order',
                        'doctor_id':await database_sync_to_async(lambda:self.user.doctor_id)(),
                        'doctor_name':await database_sync_to_async(lambda:self.user.base_user.get_full_name)()
                    }               
                )    


            
            # await self.send(json.dumps({
            #     "data": {
            #         "message:":"Confirming Order!",
            #         "patient_id":
            #         "status":200
            #     },
            # }))   
        print(data)

    async def send_message_to_channel(self,channel_name, data):
      
        channel_layer = get_channel_layer()
        await channel_layer.send(channel_name, {
            'type': 'chat',
            'data':{**data},
        })
        

        
        
    async def chat(self,event):
        
        data = event["data"]
        
        await self.send(text_data=json.dumps(data))

def get_channel_from_connect_table(user_id,flag):
    if flag=='doctor':
        return ConnectDoctor.objects.get(doctor__doctor_id=user_id).doctor_channel
    else:
        return ConnectDoctor.objects.get(patient__patient_id=user_id).patient_channel
